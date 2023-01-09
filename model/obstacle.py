# 障碍物
import random
import threading
from enum import Enum

import pygame

from base.config import Config
from base.xoy import XoY


class Obstacle(pygame.sprite.Sprite):
    class ObstacleState(Enum):
        Max = 1
        Death = 2

    def __init__(self, enemy_images, sound: pygame.mixer.Sound):
        pygame.sprite.Sprite.__init__(self)
        self.enemyImgList = enemy_images
        self.image = random.choice(self.enemyImgList)
        self.rect = self.image.get_rect()
        self.speed = XoY()
        self.sound = sound
        self.state = self.ObstacleState.Max
        self.restart()

    # 对位置和速度重新分配
    def restart(self):
        self.rect.x = random.randrange(Config.ObstacleInitRange.x[0], Config.ObstacleInitRange.x[1])
        self.rect.bottom = random.randrange(Config.ObstacleInitRange.y[0], Config.ObstacleInitRange.y[1])
        self.speed.x = random.randrange(Config.ObstacleSpeedRange.x[0], Config.ObstacleSpeedRange.x[1])
        self.speed.y = random.randrange(Config.ObstacleSpeedRange.y[0], Config.ObstacleSpeedRange.y[1])

    def boom(self):
        # todo 被击中爆炸
        threading.Thread(target=self.sound.play).start()
        self.restart()

    # 按照预设下落
    def move(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

    # 碰撞检测
    def collide(self):
        # 超出画布底部或超出画布左右
        if self.rect.top > Config.DisplayWH[1] or self.rect.right < 0 or self.rect.left > Config.DisplayWH[0]:
            self.restart()  # 障碍物消失重置

    # 被碰撞
    def collide_me(self):
        self.state = self.ObstacleState.Death
        self.boom()
        return self.state

    # 必备更新函数
    def update(self):
        self.move()
        self.collide()
