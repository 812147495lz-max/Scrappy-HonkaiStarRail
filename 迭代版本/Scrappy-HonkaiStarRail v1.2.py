import random   #引用random
import time     #引用time
import sys  #引用sys
def say(text, speed=0.02, pause=0.2):   #定义say函数，定义
    for char in text:   #for循环，在text中的每个字母
        sys.stdout.write(char)  #写出字母
        sys.stdout.flush()  #强制输出字母
        time.sleep(speed)   #每个字母之后停留speed的时间
    print() #换行
    time.sleep(pause)   #停留pause秒

class One:  #定义One类
    def __init__(self,name,side):   #class后必备的def    
        self.name=name  #读取名字
        self.side=side  #读取阵营
        self.hp=int(random.randint(40,50))  #通过random.randint来随机获得一个整数的生命值
        self.attack=int(random.randint(6,10))   #通过random.randint来随机获得一个整数的攻击值
        self.speed=int(random.randint(40,50))     #通过random.randint来随机获得一个整数的速度值
        self.defend=int(random.randint(1,4))    #通过random.randint来随机获得一个整数的防御值
        self.shield=0   #初始盾都是0
        self.time=0 #拉条功能的time，初始都是0
        self.allattack=0    #输出总计
        self.energy=0   #攒齐能量条可以拉条
        self.power=2
        self.summoned = False
        self.hpmax=self.hp  #最大血量设置为开始血量（为图形化做准备）
    def get_enemy(self,characters):
        enemy = [e for e in characters if e.side!=self.side and e.hp>0] 
        return enemy
    def get_friend(self,characters):
        friend=[f for f in characters if f.side==self.side and f.hp>0]
        return friend

    def hit(self,rival):    #定义hit函数，用来攻击，self指代自己，rival指代敌人
        #enemy = self.get_enemy(characters)
        #if len(enemy)==0:   #enemy里面没有敌人
             #pass
        if self.hp<=0:  #对于死亡角色
            pass    #直接跳过
        else :  #对于没死的角色
            self.damage=(random.randint(0,self.attack))*self.power   #真实攻击值是攻击值到0中的一个随机数
            self.boom=random.uniform(0,1)   #暴击率是通过random.uniform取的一个小数
            if self.boom>0.8:   #当暴击率大于0.8的时候
                say (f"{self.name}触发了暴击")  #输出触发了暴击
                self.damage=self.attack*2   #真实共计是攻击值的2倍
            if rival.defend>self.damage:    #当防御值大于攻击值的时候
                rival.energy +=self.damage
                self.energy +=3
                say(f"{self.name}的攻击是{self.damage}未能击破{rival.name}的防御")  #用say函数慢慢输出共计未能击破防御
            else:   #否则（当防御值小于攻击值时）
                self.allattack=self.allattack+self.damage   #计算总输出
                if rival.shield>0:  #当有盾的时候
                    if rival.shield<self.damage:  #如果盾的数值小于攻击值
                        rival.hp=max(0,rival.hp+rival.shield-self.damage)   #用max函数选出0和剩余血量最高的，作为血量
                        rival.shield=0  #强制盾量归零
                        say(f"{rival.name}遭到{self.name}{self.damage}点攻击，盾碎，血量还剩{rival.hp}")    #输出结算
                    else:   #盾为击破的情况下
                        rival.shield=rival.shield-self.damage   #剩余盾量
                        self.energy +=3
                        rival.energy+=self.damage
                        say(f"{rival.name}遭到{self.name}{self.damage}点攻击，盾还剩{rival.shield}")    #输出结算
                else:   #没盾的时候
                    rival.hp=max(0,rival.hp-self.damage)    #用max函数选出0和剩余血量最高的，作为血量
                    say(f"{rival.name}遭到{self.name}{self.damage}点攻击，血量还剩{rival.hp}")  #输出结算
                    rival.energy+=self.damage
                    self.energy +=3
                if rival.hp==0: #当对手死了的时候
                    say(f"{rival.name}被{self.name}打死了") #死亡结算
            print("---------------")    #一次攻击之后画个分割线
    def addshield(self,friend):     #加盾操作，self指代自己，friend指代同阵营
        if self.hp<=0:      #当自己死了的时候
            pass    #跳过
        friend.shield=friend.shield+7   #一次加7点盾
        say(f"{self.name}给{friend.name}加了7点盾，现在有{friend.shield}点盾")  #加盾结算
        print("---------------")    #加盾之后画个分割线
    def greatmove(self,characters):
        pass
    def actions(self,characters):  #定义一次动作，只需要指代自己就行
        enemy=self.get_enemy(characters)  
        friend=self.get_friend(characters) 
        if len(enemy)==0:   #enemy里面没有敌人
            return  
        rival=random.choice(enemy)      #用random.choice里面随机选敌人
        self.hit(rival)


class March(One):
    def __init__(self):
        super().__init__("三月七","列车")
        self.attack=random.randint(1,5)
    def greatmove(self, characters):
        enemy = self.get_enemy(characters)
        friend=self.get_friend(characters)
        if len(enemy)==0:   #enemy里面没有敌人
            return  
        say("三月七使出了'冰刻箭雨之时'")
        boss=max(enemy,key=lambda char:char.attack)     
        boss.time=0
        count=min(2,len(enemy))
        others=[e for e in enemy if e !=boss]
        stop=random.sample(others,min(count,len(others)))
        for a  in stop:
            a.time = 0 
        print("---------------") 

    def actions(self,characters):
        enemy=self.get_enemy(characters)
        friend=self.get_friend(characters)
        if len(enemy)==0:   #enemy里面没有敌人
            return      #结束
        boss=max(enemy,key=lambda char:char.attack)     #这个比较难，用lambda函数调用enemy里面的attack数值，再用max函数选出attack数值最高的数
        dying_list=[char for char in friend if char.hp<boss.attack]     #选出friend中血量小于boss攻击力的，挑选在数组dying_list中
        if len (dying_list)>0:          #假如有人快死了
            dying=min(dying_list,key=lambda char:char.hp)       #用lambda函数调出hp数值，再用max函数选出hp最低的数，记为dying
            self.addshield(dying)           #给dying加盾
        else:           #假如没人快死
            weak=min(enemy,key=lambda char:char.hp)     #用lambda和min函数选出敌人里面血量最小的，记为weak
            self.hit(weak)          #打weak

class Dragon(One):
    def __init__(self):
         super().__init__("丹恒","列车")
    def greatmove(self, characters):
        enemy = self.get_enemy(characters)
        friend=self.get_friend(characters)
        if len(enemy) == 0:    # 加上这个检查
            return
        say("丹恒使出了'洞天幻化，长梦—觉'")
        boss=max(enemy,key=lambda char:char.attack)
        self.power=6
        self.hit(boss)
        self.power =2     #重击

class Star(One):
    def __init__(self):
        super().__init__("开拓者","列车")
    def greatmove(self, characters):
        enemy = self.get_enemy(characters)
        friend=self.get_friend(characters)
        if len(enemy) == 0:    # 加上这个检查
            return
        say("开拓者使出了'全胜·再见安打'")
        for a in range(3):
            alive_enemy = [e for e in characters if e.side != self.side and e.hp > 0]
            if not alive_enemy: break # 没人了就别打了
            rival = random.choice(alive_enemy)
            self.hit(rival)

class Yang(One):
    def __init__(self):
        super().__init__("杨叔","列车")
    def greatmove(self, characters):
        enemy = self.get_enemy(characters)
        friend=self.get_friend(characters)
        if len(enemy) == 0:    # 加上这个检查
            return
        say("杨叔使出了'拟似黑洞'")
        buffer=max(friend,key=lambda char:char.attack)
        buffer.time*=1.3     #拉条
        print("---------------") 

class Destroy(One):
    def __init__(self):
        super().__init__("绝灭大君","毁灭")
        self.hp = 80        # 别忘了这些
        self.hpmax = 80
        self.summoned = False 
    def greatmove(self, characters):
        enemy = self.get_enemy(characters)
        friend=self.get_friend(characters)
        if len(enemy) == 0:    # 加上这个检查
            return
        say("绝灭大君派出了4个幻胧作为帮手")
        for i in range(1,5):
            helper=One(f"幻胧{i}","毁灭")
            helper.hp=10
            helper.hpmax = 20
            helper.attack=5
            helper.speed=30
            characters.append(helper)
        print("---------------") 
    def actions(self, characters):
        enemy = self.get_enemy(characters)
        friend=self.get_friend(characters)
        rival=random.choice(enemy)
        self.hit(rival)
        count=min (2,len(enemy))
        others = [e for e in enemy if e != rival]
        splash = random.sample(others, min(count, len(others)))
        for target in splash:
                say(f"{self.name}对{target.name}造成了溅射")
                self.power=1
                self.hit(target)
                self.power=2
                

star = Star()
dargon = Dragon()
destroy = Destroy()
march = March()
yang = Yang()

train=[star,dargon,march,yang]   #列车组成一个组
characters=[star,destroy,march,dargon,yang]      #建立4个角色的组

i=1         #计数器

for c in (characters):          #用for循环遍历4个角色
    say(f"{c.name}的血:{c.hp}，攻:{c.attack},速:{c.speed}，防:{c.defend}")      #用之前定义的say函数输出角色的数值

input("\n按回车键开始游戏")     #字面意思

while any(player.hp>0 for player in train) and destroy.hp>0:    #用any查看player.hp,for函数挨个调用数值，while进入循环
        i=i+1
        for c in (characters):      #for循环一次
            if c.hp>0:      #人没死
                c.time=c.time+c.speed   #时间戳加上
        if destroy.hp<destroy.hpmax*0.5 and destroy.summoned == False:
                destroy.greatmove(characters)
                destroy.summoned =True
        for t in (train):
                    if t.energy>20:
                        t.greatmove(characters)
                        t.energy=0
        if destroy.hp <= 0: 
            break
        while True:     #一直循环
                    alive=[c for c in characters if c.hp>0]
                    current=max(alive,key=lambda char:char.time)       #选出time值最大的
                    if current.time>100 and current.hp>0:   #time大于100且没死的情况下
                        current.time =current.time-100      #减100
                        current.actions(characters)       #动作一次
                        if destroy.hp <= 0 or all(player.hp <= 0 for player in train): 
                            break
                    else:       #没有time大于100的情况下
                        break      #结束循环
        if destroy.hp<=0 or all(player.hp<=0 for player in train):    #有一方死光了
                    break       #结束循环
if all(player.hp<=0 for player in train):      #列车组死光了
    say("星穹列车组被绝灭大君打死了")   #字面意思
    say(f"绝灭大君一共对列车组造成了{destroy.allattack}点伤害")     #字面意思
else:   #不是列车组死光就是绝灭大君死光
    say("星穹列车组把绝灭大君打死了")       #字面意思
    say(f"列车组对绝灭大君造成了{star.allattack+march.allattack+dargon.allattack+yang.allattack}点伤害")       #字面意思