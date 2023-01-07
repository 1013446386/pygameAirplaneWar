import os
import sys

import pygame

from base.button import Button
from base.color import Color
from base.config import Config
from base.resources import Resources
from model.obstacle import Obstacle
from model.player import Player
import threading

# 整体控制
class Display:

    def __init__(self):

        pygame.init()  # 必须初始化！！
        pygame.mixer.init()  # 声音初始化
        pygame.font.init()  # 文字初始化
        # 设置标题
        pygame.display.set_caption(Config.DisplayTitle)
        # 时钟（设置FPS）
        self.clock = pygame.time.Clock()
        # 屏幕宽高
        self.screen = pygame.display.set_mode(Config.DisplayWH)

        # 资源加载
        self.resources = Resources()
        pygame.display.set_icon(self.resources.ico)
        self.__running = True
        self.__pause = False

        pygame.mixer_music.play()
        pygame.mixer_music.set_volume(Config.MusicVolume)

        self.allSprites = pygame.sprite.Group()  # 全部对象组 便于调用刷新
        self.allObstacles = pygame.sprite.Group()  # 障碍对象组 便于检测碰撞
        self.allBullets = pygame.sprite.Group()  # 子弹对象组 便于检测碰撞
        # 创建继续按钮
        self.resumeBtn = Button(Config.BtnInitPos.x, Config.BtnInitPos.y, None, self.resources.resumeImgList[0],
                                self.resources.resumeImgList[0], self.resources.resumeImgList[1],
                                self.play, self.resources.enFont, (255, 0, 0))
        # 玩家对象
        self.player = Player(self.resources.playerImgList, self.resources.killSound)
        self.spritesAdd(self.allSprites, self.player)
        self.newObstacle()  # 障碍物对象

    # 生成障碍物
    def newObstacle(self):
        for i in range(Config.ObstacleCount):
            self.spritesAdd(self.allObstacles, Obstacle(self.resources.enemyImgList, self.resources.boomSound))

    # biu! biu! biu!!!
    def launch(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:  # 检测键盘按下了空格键
            threading.Thread(target=self.resources.biuSound.play).start()
            self.spritesAdd(self.allBullets, Player.Bullet(self.player.rect.center, self.resources.bulletImgList))

    # 塞进组里，直接写会有警告⚠
    def spritesAdd(self, group: pygame.sprite.Group, obj):
        """
        会自动添加到全部对象组
        :param group:被添加的组
        :param obj:被添加对象
        :return:
        """
        if group != self.allSprites:
            self.allSprites.add(obj)
        group.add(obj)

    def pause(self):
        self.__pause = True
        pygame.mixer_music.pause()

    def play(self):
        self.__pause = False
        # pygame.mixer_music.unpause()
        pygame.mixer_music.play()

    def reStart(self):
        self.pause()
        # 重新开始
        for i in self.allObstacles:
            i.reStart()
        for i in self.allBullets:
            i.kill()
        self.player.killMe()
        self.player.reStart()

    # 监听按键事件
    def keyEvent(self):
        for event in pygame.event.get():  # 循环获取事件，监听事件状态
            if event.type == pygame.QUIT:  # 退出程序
                self.bey()
            elif event.type == pygame.KEYDOWN:  # 检测按键按下
                if event.key == pygame.K_SPACE:  # 按下空格键
                    if not self.__pause:  # 如果是暂停状态则取消暂停
                        threading.Thread(target=self.launch).start()
                        # self.launch()  # 发射子弹函数
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_b or\
                        event.key == pygame.K_c or event.key == pygame.K_v:
                    if self.__pause:  # 如果是暂停状态则取消暂停
                        self.play()
                    else:
                        self.pause()

            if self.__pause:
                mx, my = pygame.mouse.get_pos()  # 获得鼠标坐标
                if event.type == pygame.MOUSEMOTION:  # 鼠标移动事件
                    # 判断鼠标是否移动到按钮范围内
                    self.resumeBtn.getFocus(mx, my)
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
                    if pygame.mouse.get_pressed() == (1, 0, 0):  # 鼠标左键按下
                        self.resumeBtn.mouseDown(mx, my)
                elif event.type == pygame.MOUSEBUTTONUP:  # 鼠标弹起
                    self.resumeBtn.mouseUp()

    # 碰撞检测
    def collide(self):
        collideDict = pygame.sprite.groupcollide(self.allObstacles, self.allBullets, False, Config.BulletKill)
        for i in collideDict:
            self.player.hitEvent()
            self.scoreListening()
            i.collideMe()

        collideList = pygame.sprite.spritecollide(self.player, self.allObstacles, False)
        for o in collideList:
            o.collideMe()
            if self.player.collideEvent() == self.player.PlayerState.Death:
                self.reStart()

    def draw(self):
        for i in Config.DisplayBGPos:
            # 更新屏幕背景 （不更新会有残影）
            self.screen.blit(self.resources.backgroundImg, i)
        self.allSprites.draw(self.screen)  # 绘制到屏幕
        self.pauseDraw()
        self.infoDraw()

    def infoDraw(self):
        img = self.resources.chFont.render("帧率:" + str(int(self.clock.get_fps())), True, Color.WHITE)
        self.screen.blit(img, Config.FPSPos)
        hpImage = self.resources.chFont.render("血量:" + str(self.player.HP), True, Color.WHITE)
        self.screen.blit(hpImage, Config.HPPos)
        scoreImage = self.resources.chFont.render("分数:" + str(self.player.score), True, Color.WHITE)
        self.screen.blit(scoreImage, Config.ScorePos)
        scoreMaxImage = self.resources.chFont.render("目标:" + str(Config.PlayerScoreMax), True, Color.WHITE)
        self.screen.blit(scoreMaxImage, Config.ScoreMaxPos)

    def pauseDraw(self):
        if self.__pause:
            # self.screen.blit(self.resources.resumeImg, (210, 327.5))
            self.resumeBtn.draw(self.screen)

    def scoreListening(self):
        if self.player.score >= Config.PlayerScoreMax and self.player.state != self.player.PlayerState.Death:
            self.reachScore()

    def loop(self):
        # 必须循环，不然游戏就没了!
        while self.__running:
            self.clock.tick(Config.DisplayFPS)  # 设置每秒刷新帧数，不大于该值 但性能不足时会小于该值
            self.keyEvent()
            if not self.__pause:
                if Config.Le:
                    self.launch()  # 不建议启用 发射频率与帧率相关，同时打开函数内按键按下检测

                # 调用所有对象的update函数
                self.allSprites.update()
                self.collide()  # 碰撞检测

            self.draw()
            # 更新屏幕内容(翻转白板，将绘制完毕的界面显示至屏幕，可有效消除绘制拖影)
            pygame.display.flip()

    # 程序结束了！！
    def bey(self):
        self.__running = False
        pygame.quit()  # 卸载所有模块
        sys.exit()  # 终止程序，确保退出程序

    def reachScore(self):
        self.player.state = self.player.PlayerState.Reach
        pygame.mixer.stop()
        threading.Thread(target=self.resources.reachSound.play).start()
        self.reStart()


if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    # 开搞!
    Display().loop()
