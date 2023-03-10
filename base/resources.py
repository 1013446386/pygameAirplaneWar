import os

import pygame

from base.config import Config
from .color import Color


# 资源
class Resources:
    def __init__(self):
        # 图片资源文件夹
        self.img_folder = os.path.join(Config.game_folder, 'resources/images')
        self.ico_folder = os.path.join(Config.game_folder, 'resources/icon')
        self.sound_folder = os.path.join(Config.game_folder, 'resources/sounds')
        self.font_folder = os.path.join(Config.game_folder, 'resources/fonts')
        self.backgroundImg = pygame.image.load(os.path.join(self.img_folder, 'background1_mini.png')).convert()
        self.ico = pygame.image.load(os.path.join(self.ico_folder, 'd5_128x128.ico')).convert_alpha()
        self.ico.set_colorkey(Color.BLACK)

        pygame.mixer_music.load(os.path.join(self.sound_folder, 'background.wav'))

        self.biuSound = pygame.mixer.Sound(os.path.join(self.sound_folder, 'biu.wav'))
        self.boomSound = pygame.mixer.Sound(os.path.join(self.sound_folder, 'boom.wav'))
        self.killSound = pygame.mixer.Sound(os.path.join(self.sound_folder, 'kill.wav'))
        self.reachSound = pygame.mixer.Sound(os.path.join(self.sound_folder, 'reach.wav'))
        self.biuSound.set_volume(Config.BiuVolume)
        # 按钮图片
        self.resumeImgList = self.png_add_list(["resume_nor", "resume_pressed"])

        # 按钮使用的字体
        self.enFont = pygame.font.SysFont("si", 40)
        self.chFont = pygame.font.Font(os.path.join(self.font_folder, 'zcool-gdh_Regular.ttf'), 28)

        # 玩家资源
        # self.playerImgList = self.pngImgToList(["me3"])
        self.playerImgList = self.png_add_list(["me1"])

        # 子弹资源
        self.bulletImgList = self.png_add_list(["bullet1", "bullet2", "bomb"])

        # 障碍物资源
        self.enemyImgList = self.png_add_list(["enemy1", "enemy2", "enemy3_n1"])

    def png_add_list(self, img_names, set_color_key=Color.BLACK):
        # 障碍物资源
        tmp = []
        for i in img_names:
            img = pygame.image.load(os.path.join(self.img_folder, i + '.png')).convert()
            img.set_colorkey(set_color_key)
            tmp.append(img)
        return tmp
