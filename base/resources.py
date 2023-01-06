from base.config import Config
from .color import Color
import pygame
import os


# 资源
class Resources:

    def __init__(self):
        # 图片资源文件夹
        self.img_folder = os.path.join(Config.game_folder, 'resources/images')
        self.sound_folder = os.path.join(Config.game_folder, 'resources/sounds')
        self.backgroundImg = pygame.image.load(os.path.join(self.img_folder, 'background1_mini.png')).convert()

        pygame.mixer_music.load(os.path.join(self.sound_folder, 'background.wav'))

        self.biuSound = pygame.mixer.Sound(os.path.join(self.sound_folder, 'biu.wav'))
        self.boomSound = pygame.mixer.Sound(os.path.join(self.sound_folder, 'boom.wav'))
        self.killSound = pygame.mixer.Sound(os.path.join(self.sound_folder, 'kill.wav'))
        self.biuSound.set_volume(Config.BiuVolume)
        # 按钮图片
        self.resumeImgList = self.pngImgToList(["resume_nor", "resume_pressed"])

        # 按钮使用的字体
        self.btnFont = pygame.font.SysFont("仿宋", 40)

        # 玩家资源
        self.playerImgList = self.pngImgToList(["me1", "me2"])

        # 子弹资源
        self.bulletImgList = self.pngImgToList(["bullet1", "bullet2", "bomb"])

        # 障碍物资源
        self.enemyImgList = self.pngImgToList(["enemy1", "enemy2", "enemy3_n1"])

    def pngImgToList(self, ImgNameList, set_color_key=Color.BLACK):
        # 障碍物资源
        List = []
        for i in ImgNameList:
            img = pygame.image.load(os.path.join(self.img_folder, i + '.png')).convert()
            img.set_colorkey(set_color_key)
            List.append(img)
        return List
