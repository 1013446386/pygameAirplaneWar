# 从配置文件读取基本参数
import os
import sys

from base.xoy import XoY  # 存基本信息的数据类


def get_dir_path():
    if getattr(sys, 'frozen', False):
        # noinspection PyProtectedMember
        cur_path = sys._MEIPASS
    else:
        cur_path = os.getcwd()
    return cur_path


class Config:
    game_folder = get_dir_path()  # 获取运行路径

    Le = False  # 无敌模式

    DisplayWH = (1024, 1280)  # 窗口宽高
    DisplayBGPos = [(0, 0)]  # 背景图位置
    DisplayTitle = "飞机大战"  # 窗口标题
    DisplayFPS = 60  # FPS

    MusicVolume = 0.33
    BiuVolume = 0.4

    PlayerSpeed = XoY()  # 玩家移送速度
    PlayerSpeed.x = 7
    PlayerSpeed.y = 8

    PlayerInitPos = XoY()  # 玩家初始位置
    PlayerInitPos.x = DisplayWH[0] / 2
    PlayerInitPos.y = DisplayWH[1] - 88

    PlayerHP = 100  # 血量
    if Le:
        PlayerStepSubHP = 0  # 单次扣除血量
        PlayerAddScoreStep = 10
        ObstacleCount = 16  # 障碍物数量

    else:
        PlayerStepSubHP = 10
        PlayerAddScoreStep = 10
        ObstacleCount = 16

    PlayerScoreMax = 13000

    BulletSpeedY = 7  # 子弹速度
    BulletKill = not Le  # 子弹击中目标后是否失效

    ObstacleSpeedRange = XoY()  # 障碍物移动速度区间
    ObstacleSpeedRange.x = (-2, 2)
    ObstacleSpeedRange.y = (3, 7)

    ObstacleInitRange = XoY()  # 障碍物初始位置区间
    ObstacleInitRange.x = (0, DisplayWH[0])
    ObstacleInitRange.y = (-50, -30)

    BtnInitPos = XoY()  # 按钮初始位置
    BtnInitPos.x = DisplayWH[0] / 2 - 30
    BtnInitPos.y = DisplayWH[1] / 2 - 22.5

    FPSPos = (0, 0)
    HPPos = (0, 30)
    ScorePos = (0, 60)
    ScoreMaxPos = (0, 90)
