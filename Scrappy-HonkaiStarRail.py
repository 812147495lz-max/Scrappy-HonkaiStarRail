from __future__ import annotations

__version__ = "2.2.1"

import random
import time
import unicodedata
from typing import Iterable, Optional

# 其实更应该使用一些像rich的第三方库来进行彩色文本的输出，毕竟真的有人能看懂ANSI吗。不过反正你说你也要做GUI了
COLORS = {
    "三月七":       "\033[38;2;100;200;255m",
    "丹恒":         "\033[38;2;80;220;130m",
    "开拓者":       "\033[38;2;170;170;170m",
    "瓦尔特杨":     "\033[38;2;243;255;50m",
    "纳努克":       "\033[38;2;237;182;18m",
    "幻胧":         "\033[38;2;45;86;77m",
}
RESET = "\033[0m"
HP_COLOR = "\033[38;2;200;0;0m"
SHIELD_COLOR = "\033[38;2;36;30;214m"
ATTACK_COLOR = "\033[38;2;214;116;30m"


def say(text, speed=0.01, pause=0.1) -> None:
    global COLORS, RESET
    for name, color in COLORS.items():
        text = text.replace(name, f"{color}{name}{RESET}")

    for char in text:
        print(char, end="", flush=True)
        time.sleep(speed)  # 每个字母之后停留speed的时间
    print()
    time.sleep(pause)


def display(movedisplay):
    if movedisplay is None:  # 如果人死了那就没有攻击
        return
    if movedisplay["type"] == "hit":  # 如果type是hit
        if movedisplay.get("splash"):
            say(f"{movedisplay['attacker']}对{movedisplay['rival']}造成了溅射")
        if movedisplay["crithit"] == True:  # 如果打出了暴击，暴击和下面的可以同时存在，所以是单独的if
            say(f"{movedisplay['attacker']}打出了暴击")
        if movedisplay["blocked"] == True:  # 如果被挡住
            say(f"{movedisplay['attacker']}的攻击被{movedisplay['rival']}挡住了")
        elif movedisplay["shutter"] == True:  # 如果盾碎是true
            say(f"{movedisplay['attacker']}对{movedisplay['rival']}打出了{ATTACK_COLOR}{movedisplay['damage']}{RESET}点攻击，打破了盾牌")
            say(f"{movedisplay['rival']}还剩{HP_COLOR}{movedisplay['hp']}{RESET}点血")
        elif movedisplay["shield"] > 0:  # 如果还有盾
            say(f"{movedisplay['attacker']}对{movedisplay['rival']}打出了{ATTACK_COLOR}{movedisplay['damage']}{RESET}点攻击，未能击穿盾")
            say(f"{movedisplay['rival']}还剩{HP_COLOR}{movedisplay['hp']}{RESET}点血{movedisplay['shield']}{RESET}点盾")
        else:  # 如果没有盾牌
            say(f"{movedisplay['attacker']}对{movedisplay['rival']}打出了{ATTACK_COLOR}{movedisplay['damage']}{RESET}点攻击")
            say(f"{movedisplay['rival']}还剩{HP_COLOR}{movedisplay['hp']}{RESET}点血")
        if movedisplay.get("killed") == True:  # 如果被杀死了
            say(f"{movedisplay['rival']}被{movedisplay['attacker']}打死了")
    elif movedisplay["type"] == "shield":
        say(f"{movedisplay['caster']}给{movedisplay['friend']}加了{movedisplay['amount']}点盾，现在有{SHIELD_COLOR}{movedisplay['shield']}{RESET}点盾")
    elif movedisplay["type"] == "march_great":  # 如果type是march_great
        targets = [t for t in [movedisplay['target1'],
                               movedisplay['target2'], movedisplay['target3']] if t]
        say(f"三月七\033[38;2;100;200;255m使出了'冰刻箭雨之时'\033[0m")
        say(f"冻结了{'、'.join(targets)}")
    elif movedisplay["type"] == "dragon_great":
        say(f"丹恒\033[38;2;80;220;130m使出了'洞天幻化，长梦一觉'\033[0m")
    elif movedisplay["type"] == "star_great":
        say("开拓者\033[38;2;196;196;196m使出了'全胜·再见安打'\033[0m")
    elif movedisplay["type"] == "yang_great":
        say("瓦尔特杨\033[38;2;243;255;50m使出了'拟似黑洞'")
        say(f"{movedisplay['target']}被加速了")
    elif movedisplay["type"] == "destroy_great":
        say("纳努克\033[38;2;237;182;18m派出了4个幻胧\033[38;2;237;182;18m作为帮手'\033[0m")
    elif movedisplay["type"] == "timebar":
        print("\n" + "—"*10 + " 行动序列 " + "—"*10)
        for item in movedisplay["data"]:
            # 使用 item 里面的键值进行排版
            name_str = cjk_ljust(item['char'], 12)
            print(f"{name_str} |{item['timebar']}| {item['time']}/200")
        print("—"*28)
        time.sleep(1)
    elif movedisplay["type"] == "dwin":
        say("星穹列车组被纳努克打死了")  # 字面意思
        say(f"纳努克一共对列车组造成了{movedisplay['allattack']}点伤害")
    elif movedisplay["type"] == "twin":
        say("星穹列车组把纳努克打死了")  # 字面意思
        say(f"列车组对纳努克造成了{movedisplay['allattack']}点伤害")
    elif movedisplay["type"] == "stats":
        for c in (characters):  # 用for循环遍历4个角色
            say(f"{c.name}的血:{c.hp}，攻:{c.attack},速:{c.speed}，防:{c.defend}")

    print("---------------")  # 画分割线


def actionbar(char):  # 定义actionbar函数，char是参数
    # 用sorted函数，对hp>0的角色，按照time排序
    timeline = sorted([c for c in char if c.hp > 0],
                      key=lambda c: c.time, reverse=True)
    timebar = []
    for c in timeline:  # for循环
        length = 15
        box = min(length, int(c.time/200*length))
        bar = "█" * box + "—" * (length - box)
        timebar.append({
            "type": "timebar",
            "char": c.name,
            "timebar": bar,
            "box": box,
            "time": int(c.time)
        })
    result = {
        "type": "timebar",
        "data": timebar  # 这里传的是整个列表
    }
    display(result)


def character_is_wide(char: str) -> bool:
    width = unicodedata.east_asian_width(char)
    return width in ("F", "W", "A")


def cjk_ljust(text, width) -> str:
    """通过在后方补齐空格调整字符串的视觉宽度：中文字符算2个宽度"""
    count = 0
    for char in text:
        if character_is_wide(char):
            count += 1

    return text + ' '*(width - len(text) - count)


class One:
    def __init__(
            self,
            name: str,
            side: str,
            *,
            hp: Optional[int] = None,
            attack: Optional[int] = None,
            speed: Optional[int] = None,
            defend: Optional[int] = None):
        self.name = name  # 读取名字
        self.side = side  # 读取阵营

        # 血量 攻击 速度 防御
        self.hp = random.randint(40, 50) if hp is None else hp
        self.attack = random.randint(6, 10) if attack is None else attack
        self.speed = random.randint(40, 100) if speed is None else speed
        self.defend = random.randint(1, 4) if defend is None else defend

        self.shield = 0  # 初始盾都是0
        self.time = 0  # 拉条功能的time，初始都是0
        self.allattack = 0  # 输出总计
        self.energy = 0  # 攒齐能量条可以拉条
        self.power = 2
        self.summoned = False
        self.hpmax = self.hp  # 最大血量设置为开始血量（为图形化做准备）
        self.color = "\033[0m"

    def is_alive(self) -> bool:
        return self.hp > 0

    def is_dead(self) -> bool:
        return not self.is_alive()

    def get_enemy(self, characters: Iterable[One]) -> list[One]:
        enemy = [e for e in characters if e.side != self.side and e.is_alive()]
        return enemy

    def get_friend(self, characters: Iterable[One]) -> list[One]:
        friend = [f for f in characters if f.side == self.side and f.is_alive()]
        return friend

    def hit(self, target: One):
        if self.is_dead() or target.is_dead():
            return

        result = {
            "type": "hit",
            "crithit": False,  # 暴击
            "blocked": False,  # 挡住攻击
            "attacker": self.name,  # 进攻者
            "rival": target.name,  # 被攻击者
            "shutter": False,  # 打破盾牌
            "shield": target.shield,
        }
        self.damage = random.randint(0, self.attack) * self.power  # 真实攻击值是攻击值到0中的一个随机数
        self.boom = random.uniform(0, 1)  # 暴击率是通过random.uniform取的一个小数
        if self.boom > 0.8:  # 当暴击率大于0.8的时候
            result["crithit"] = True  # 输出触发了暴击
            self.damage = self.attack*2  # 真实攻击是攻击值的2倍
            result["damage"] = self.damage
        if target.defend > self.damage:  # 当防御值大于攻击值的时候
            target.energy += self.damage
            self.energy += 3
            result["blocked"] = True
        else:  # 否则（当防御值小于攻击值时）
            self.allattack = self.allattack+self.damage  # 计算总输出
            if target.shield > 0:  # 当有盾的时候
                if target.shield < self.damage:  # 如果盾的数值小于攻击值
                    # 用max函数选出0和剩余血量最高的，作为血量
                    target.hp = max(0, target.hp+target.shield-self.damage)
                    target.shield = 0  # 强制盾量归零
                    result["shutter"] = True
                    result["shield"] = target.shield
                    result["hp"] = target.hp  # 输出结算
                else:  # 盾为击破的情况下
                    target.shield = target.shield-self.damage  # 剩余盾量
                    self.energy += 3
                    target.energy += self.damage
                    result["hp"] = target.hp  # 输出结算
            else:  # 没盾的时候
                # 用max函数选出0和剩余血量最高的，作为血量
                target.hp = max(0, target.hp-self.damage)
                result["hp"] = target.hp  # 输出结算
                target.energy += self.damage
                self.energy += 3
            if target.hp == 0:  # 当对手死了的时候
                result["killed"] = True
        result["damage"] = self.damage
        return result

    def add_shield(self, target: One):  # 加盾操作，self指代自己，friend指代同阵营
        if self.is_dead():
            return

        self.amount = 7
        target.shield = target.shield+self.amount  # 一次加amount点盾
        result = {"type": "shield",  # type是盾
                  "caster": self.name,  # 自己
                  "friend": target.name,  # 加盾者
                  "amount": self.amount,  # 加盾数量
                  "shield": target.shield,
                  }
        return result  # 加盾结算

    def great_move(self, characters):
        raise NotImplementedError

    def actions(self, characters):  # 定义一次动作，只需要指代自己就行
        enemy = self.get_enemy(characters)
        friend = self.get_friend(characters)
        if len(enemy) == 0:  # enemy里面没有敌人
            return
        rival = random.choice(enemy)  # 用random.choice里面随机选敌人
        hit_result = self.hit(rival)
        display(hit_result)


class March(One):
    def __init__(self):
        super().__init__("三月七", "列车", attack=random.randint(1, 5))
        self.color = "\033[38;2;100;200;255m"

    def great_move(self, characters):
        enemy = self.get_enemy(characters)
        friend = self.get_friend(characters)
        if len(enemy) == 0:  # enemy里面没有敌人
            return
        boss = max(enemy, key=lambda char: char.attack)

        count = min(2, len(enemy))
        others = [e for e in enemy if e != boss]
        stop = random.sample(others, min(count, len(others)))

        result = {"char": self.name,
                  "type": "march_great",
                  "target1": boss.name,
                  "target2": stop[0].name if len(stop) > 0 else None,
                  "target3": stop[1].name if len(stop) > 1 else None,

                  }
        display(result)
        boss.time = 0
        for a in stop:
            a.time = 0
        return result

    def actions(self, characters):
        enemy = self.get_enemy(characters)
        friend = self.get_friend(characters)
        if len(enemy) == 0:  # enemy里面没有敌人
            return  # 结束
        # 这个比较难，用lambda函数调用enemy里面的attack数值，再用max函数选出attack数值最高的数
        boss = max(enemy, key=lambda char: char.attack)
        dying_list = [char for char in friend if char.hp < 4 *
                      boss.attack]  # 选出friend中血量小于boss攻击力的，挑选在数组dying_list中
        if len(dying_list) > 0:  # 假如有人快死了
            # 用lambda函数调出hp数值，再用max函数选出hp最低的数，记为dying
            dying = min(dying_list, key=lambda char: char.hp)
            addshield = self.add_shield(dying)
            display(addshield)  # 给dying加盾
        else:  # 假如没人快死
            # 用lambda和min函数选出敌人里面血量最小的，记为weak
            weak = min(enemy, key=lambda char: char.hp)
            hitresult = self.hit(weak)
            display(hitresult)  # 打weak


class Dragon(One):
    def __init__(self):
        super().__init__("丹恒", "列车")

    def great_move(self, characters):
        enemy = self.get_enemy(characters)
        if len(enemy) == 0:    # 加上这个检查
            return
        boss = max(enemy, key=lambda char: char.attack)
        result = {"char": self.name,
                  "type": "dragon_great",
                  }
        display(result)
        self.power = 6
        hitresult = self.hit(boss)
        display(hitresult)
        self.power = 2  # 重击
        return result


class Star(One):
    def __init__(self):
        super().__init__("开拓者", "列车")

    def great_move(self, characters):
        enemy = self.get_enemy(characters)
        if len(enemy) == 0:    # 加上这个检查
            return
        result = {"char": self.name,
                  "type": "star_great",
                  }
        display(result)
        for a in range(3):
            alive_enemy = [e for e in characters if e.side !=
                           self.side and e.hp > 0]
            if not alive_enemy:
                break  # 没人了就别打了
            rival = random.choice(alive_enemy)
            hitresult = self.hit(rival)
        display(hitresult)
        return result


class Yang(One):
    def __init__(self):
        super().__init__("瓦尔特杨", "列车")

    def great_move(self, characters):
        enemy = self.get_enemy(characters)
        friend = self.get_friend(characters)

        if len(enemy) == 0:    # 加上这个检查
            return
        buffer = max(friend, key=lambda char: char.attack)
        result = {"char": self.name,
                  "type": "yang_great",
                  "target": buffer.name,
                  }
        display(result)
        buffer.time *= 1.3  # 拉条
        return result


class Destroy(One):
    def __init__(self):
        super().__init__("纳努克", "毁灭", hp=200)

    def great_move(self, characters):
        enemy = self.get_enemy(characters)
        friend = self.get_friend(characters)
        if len(enemy) == 0:    # 加上这个检查
            return
        for i in range(1, 5):
            helper = One(f"幻胧{i}", "毁灭")
            helper.hp = 40
            helper.hpmax = helper.hp
            helper.attack = 5
            helper.speed = 50
            characters.append(helper)
        result = {"char": self.name,
                  "type": "destroy_great",
                  }
        display(result)
        return result

    def actions(self, characters):
        enemy = self.get_enemy(characters)
        friend = self.get_friend(characters)
        rival = random.choice(enemy)
        hitresult = self.hit(rival)
        display(hitresult)
        count = min(2, len(enemy))
        others = [e for e in enemy if e != rival]
        splash = random.sample(others, min(count, len(others)))
        for target in splash:
            self.power = 1
            hitresult = self.hit(target)
            hitresult["splash"] = True
            display(hitresult)
            self.power = 2


class Game:
    def __init__(self, characters: Iterable[One]):
        self.characters = characters
        self.train = [c for c in self.characters if c.side == "列车"]
        self.destroy = [c for c in self.characters if c.side == "毁灭"]
        if self.destroy:
            self.boss = self.destroy[0]

    def stats(self):  # 定义run函数，characters是参数
        result = {"type": "stats"}
        display(result)
        input("\n按回车键继续")
        return result

    def game_over(self):
        if all(t.hp <= 0 for t in self.train):
            allattack = self.boss.allattack
            result = {"type": "dwin",
                      "allattack": allattack
                      }
            return result
        for e in self.destroy:
            if isinstance(e, Destroy) and e.is_dead():  # isinstance用来判断e是否是Destroy的实例
                allattack = sum(t.allattack for t in self.train)
                result = {"type": "twin",
                          "allattack": allattack
                          }

                return result
        return None

    def tgreatmove(self):
        for t in (self.train):
            if t.energy > 20 and t.hp > 0:
                t.great_move(self.characters)
                t.energy = 0

    def dgreatmove(self):
        for e in self.destroy:
            if isinstance(e, Destroy) and not e.summoned:
                if e.hp < e.hpmax * 0.5:
                    e.great_move(self.characters)
                    e.summoned = True

    def time(self):
        for c in (self.characters):
            if c.hp > 0:
                c.time = c.time+c.speed

    def move(self):
        while True:
            alive = [c for c in self.characters if c.hp > 0]
            if not alive:
                break
            current = max(alive, key=lambda char: char.time)
            if current.time >= 200 and current.hp > 0:  # time大于200且没死的情况下
                current.time = current.time-200  # 减200
                current.actions(self.characters)
            else:  # 没有time大于100的情况下
                break

    def loop(self):
        self.stats()
        while True:
            self.time()
            actionbar(self.characters)
            self.tgreatmove()
            self.dgreatmove()
            self.move()
            result = self.game_over()
            if result:
                display(result)  # 如果有游戏结束
                break


if __name__ == "__main__":
    star = Star()
    dragon = Dragon()
    destroy = Destroy()
    march = March()
    yang = Yang()
    characters = [star, destroy, march, dragon, yang]  # 建立4个角色的组

    game = Game(characters)
    game.loop()
    input("按回车键退出")
