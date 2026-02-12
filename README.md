# Scrappy-HonkaiStarRail (丐版崩坏：星穹铁道)

这是一个基于 Python 开发的纯文本版战斗引擎，试图还原《崩坏：星穹铁道》的核心战斗逻辑。

示例视频：
【Python丐版崩铁再次迭代】 https://www.bilibili.com/video/BV14KcczwExA/?share_source=copy_web&vd_source=21da6774512a26622cbbdf0f7b761959

###  核心机制
* **CTB 行动条系统**：根据角色 `speed` 属性动态计算回合顺序。
* **能量与终极技**：角色攻击或受击可回复能量（Energy），攒满后可释放强力大招。
* **Boss 多阶段变换**：绝灭大君在生命值低于 50% 时会召唤 4 个幻胧加入战场。
* **战术细节**：包含暴击判定、护盾机制以及杨叔的“拟似黑洞”拉条控制。

###  快速开始
1. 确保安装了 Python 3.6+。
2. 运行脚本：`python Scrappy-HonkaiStarRail.py`

### 版本迭代
V1.1: 修复拉条排序逻辑，解决了可能卡死的问题，解决了出大招会显示多个分隔符的问题，加快了游戏速度，优化 AI 执行流

V1.2：改掉了原本if套else的逻辑，改成了子类继承的方法，优化了代码结构

V1.3将原本的执行逻辑和输出逻辑进行解耦，为下一步ui开发做好准备

V2.0:将原本混乱的运算和输出彻底解耦，并增加时间条显示每一回合的行动顺序

### 运行图片


<img width="565" height="1500" alt="image" src="https://github.com/user-attachments/assets/2c8be46c-1a75-4559-8223-4d692ca6f10b" />



