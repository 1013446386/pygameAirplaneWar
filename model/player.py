import random
from enum import Enum

import pygame

from base.config import Config


# 玩家类
class Player(pygame.sprite.Sprite):
    # 子弹类
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, center_pos, bullet_img: list):
            pygame.sprite.Sprite.__init__(self)
            self.image = random.choice(bullet_img)
            self.rect = self.image.get_rect()
            self.rect.center = center_pos

        def collide(self):
            if self.rect.bottom < 0:
                self.kill()

        def update(self):
            self.collide()
            self.rect.y -= Config.BulletSpeedY

    class PlayerState(Enum):
        Max = 1
        Reach = 2
        Injured = 3
        Death = 4

    def __init__(self, player_images, sound: pygame.mixer.Sound):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(Color.GREEN)
        self.playerImgList = player_images
        self.image = random.choice(self.playerImgList)
        self.rect = self.image.get_rect()
        # 对象x轴中心点
        self.rect.centerx = Config.PlayerInitPos.x
        self.rect.bottom = Config.PlayerInitPos.y

        self.sound = sound

        self.HP = Config.PlayerHP
        self.state = Player.PlayerState.Max
        self.score = 0

    def restart(self):
        # 对象x轴中心点
        self.rect.centerx = Config.PlayerInitPos.x
        self.rect.bottom = Config.PlayerInitPos.y
        self.HP = Config.PlayerHP
        self.state = Player.PlayerState.Max
        self.score = 0

    def move(self):
        # 检测按键按下
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.rect.x += Config.PlayerSpeed.x
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.rect.x -= Config.PlayerSpeed.x

        if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            self.rect.y -= Config.PlayerSpeed.y
            self.image = self.image = random.choice(self.playerImgList)
        if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
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

    def hit_event(self):
        self.score += Config.PlayerAddScoreStep

    def collide_event(self):
        self.HP -= Config.PlayerStepSubHP
        if self.HP > 0:
            self.collide_me()
        else:
            self.kill_me()
        return self.state

    def collide_me(self):
        self.state = self.PlayerState.Injured

    def kill_me(self):
        if self.state == self.PlayerState.Reach:
            return
        if self.state != self.PlayerState.Death:
            self.state = self.PlayerState.Death
            print("死亡")
            pygame.mixer.stop()
            self.sound.play()
            self.score = 0

    def draw(self):
        pass

    def update(self):
        self.move()
        self.collide()
