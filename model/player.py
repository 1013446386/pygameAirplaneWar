import random
from enum import Enum

from base.config import Config
import pygame


# 玩家类
class Player(pygame.sprite.Sprite):
    # 子弹类
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, centerXY, bulletImg: list):
            pygame.sprite.Sprite.__init__(self)
            self.image = random.choice(bulletImg)
            self.rect = self.image.get_rect()
            self.rect.center = centerXY

        def collide(self):
            if self.rect.bottom < 0:
                self.kill()

        def update(self):
            self.collide()
            self.rect.y -= Config.BulletSpeedY

    class PlayerState(Enum):
        Max = 1
        Injured = 2
        Seriously = 3
        Death = 4

    def __init__(self, playerImgList, sound: pygame.mixer.Sound):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(Color.GREEN)
        self.playerImgList = playerImgList
        self.image = random.choice(self.playerImgList)
        self.rect = self.image.get_rect()
        # 对象x轴中心点
        self.rect.centerx = Config.PlayerInitPos.x
        self.rect.bottom = Config.PlayerInitPos.y

        self.sound = sound

        self.HP = Config.PlayerHP
        self.state = Player.PlayerState.Max

    def reStart(self):
        # 对象x轴中心点
        self.rect.centerx = Config.PlayerInitPos.x
        self.rect.bottom = Config.PlayerInitPos.y
        self.HP = Config.PlayerHP
        self.state = Player.PlayerState.Max

    def move(self):
        # 检测按键按下
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_RIGHT] or keyPressed[pygame.K_d]:
            self.rect.x += Config.PlayerSpeed.x
        if keyPressed[pygame.K_LEFT] or keyPressed[pygame.K_a]:
            self.rect.x -= Config.PlayerSpeed.x

        if keyPressed[pygame.K_UP] or keyPressed[pygame.K_w]:
            self.rect.y -= Config.PlayerSpeed.y
            self.image = self.image = random.choice(self.playerImgList)
        if keyPressed[pygame.K_DOWN] or keyPressed[pygame.K_s]:
            self.rect.y += Config.PlayerSpeed.y

    def collide(self):
        if self.rect.centerx > Config.DisplayWH[0]:
            self.rect.centerx = Config.DisplayWH[0]
        elif self.rect.centerx < 0:
            self.rect.centerx = 0

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Config.DisplayWH[1]:
            self.rect.bottom = Config.DisplayWH[1]

    def collideEvent(self):
        self.HP -= Config.PlayerStepSubHP
        if self.HP > 0:
            self.collideMe()
        else:
            self.killMe()
        return self.state

    def collideMe(self):
        print("小心！还剩下", self.HP)
        self.state = self.PlayerState.Injured

    def killMe(self):
        print("死了！")
        self.sound.play()
        self.state = self.PlayerState.Death

    def draw(self):
        pass

    def update(self):
        self.move()
        self.collide()