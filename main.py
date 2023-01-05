# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import sys
import pygame
import random
import os


class Config:
    def __init__(self):
        self.Le = False  # 无敌模式
        # Colors (R, G, B)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        self.DisplayWH = None  # 窗口宽高
        self.DisplayTitle = None  # 窗口标题
        self.DisplayFPS = None  # FPS

        self.PlayerSpeed = XoY()  # 玩家移送速度
        self.PlayerInitPos = XoY()  # 玩家初始位置
        self.PlayerHP = None  # 血量
        self.PlayerStepSubHP = None  # 单次扣除血量

        self.BulletSpeedY = None  # 子弹速度
        self.BulletKill = None

        self.ObstacleCount = None  # 障碍物数量
        self.ObstacleSpeedRange = XoY()  # 障碍物移动速度区间
        self.ObstacleInitRange = XoY()  # 障碍物初始位置区间

    def readConfig(self):  # 读配置
        # todo 修改为文件内读取配置，便于修改调整
        self.DisplayWH = (480, 700)
        self.DisplayTitle = "飞机大战"
        self.DisplayFPS = 60

        self.PlayerSpeed.x = 7
        self.PlayerSpeed.y = 8
        self.PlayerInitPos.x = self.DisplayWH[0] / 2
        self.PlayerInitPos.y = self.DisplayWH[1] - 88
        self.PlayerHP = 100
        self.PlayerStepSubHP = 10
        if self.Le:
            self.PlayerStepSubHP = 0

        self.BulletSpeedY = 5
        self.BulletKill = not self.Le

        self.ObstacleCount = 10
        self.ObstacleSpeedRange.x = (-2, 2)
        self.ObstacleSpeedRange.y = (3, 7)

        self.ObstacleInitRange.x = (0, self.DisplayWH[0])
        self.ObstacleInitRange.y = (-50, -30)

        return True  # 文件可能读取失败，预留返回值


class Resources:
    def __init__(self):
        # 获取运行路径
        game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(game_folder, 'images')

        self.backgroundImg = None
        self.resumeImg = None

        # 玩家资源
        self.playerImg = None

        # 子弹资源
        self.bulletImgList = []

        # 障碍物资源
        self.enemy1Img = None
        self.enemyD1Img = None
        self.enemyD2Img = None
        self.enemyD3Img = None
        self.enemyD4Img = None
        # 按钮图片
        self.resumeBtnNormal = None
        self.resumeBtnDown = None

        # 按钮使用的字体
        self.btnFont = pygame.font.SysFont("lisu", 40)

        self.readImg()

    def readImg(self):
        self.backgroundImg = pygame.image.load(os.path.join(self.img_folder, 'background.png')).convert()
        self.resumeImg = pygame.image.load(os.path.join(self.img_folder, 'resume_nor.png')).convert()
        self.resumeImg.set_colorkey(config.BLACK)

        self.playerImg = pygame.image.load(os.path.join(self.img_folder, 'life.png')).convert()
        self.playerImg.set_colorkey(config.BLACK)
        bullet1 = pygame.image.load(os.path.join(self.img_folder, 'bullet1.png')).convert()
        bullet1.set_colorkey(config.BLACK)
        bullet2 = pygame.image.load(os.path.join(self.img_folder, 'bullet2.png')).convert()
        bullet2.set_colorkey(config.BLACK)
        self.bulletImgList.append(bullet1)
        self.bulletImgList.append(bullet2)

        self.enemy1Img = pygame.image.load(os.path.join(self.img_folder, 'enemy1.png')).convert()
        self.enemyD1Img = pygame.image.load(os.path.join(self.img_folder, 'enemy1_down1.png')).convert()
        self.enemyD2Img = pygame.image.load(os.path.join(self.img_folder, 'enemy1_down2.png')).convert()
        self.enemyD3Img = pygame.image.load(os.path.join(self.img_folder, 'enemy1_down3.png')).convert()
        self.enemyD4Img = pygame.image.load(os.path.join(self.img_folder, 'enemy1_down4.png')).convert()
        self.enemy1Img.set_colorkey(config.BLACK)
        self.enemyD1Img.set_colorkey(config.BLACK)
        self.enemyD2Img.set_colorkey(config.BLACK)
        self.enemyD3Img.set_colorkey(config.BLACK)
        self.enemyD4Img.set_colorkey(config.BLACK)

        self.resumeBtnNormal = pygame.image.load(os.path.join(self.img_folder, 'resume_nor.png')).convert_alpha()
        self.resumeBtnDown = pygame.image.load(os.path.join(self.img_folder, 'resume_pressed.png')).convert_alpha()


class XoY:
    def __init__(self):
        self.x = None
        self.y = None


# 按钮
class Button:
    NORMAL = 0
    MOVE = 1
    DOWN = 2

    def __init__(self, x, y, text, imgNormal, imgMove=None, imgDown=None, callBackFunc=None, font=None, rgb=(0, 0, 0)):
        """
        初始化按钮的相关参数
        :param x: 按钮在窗体上的x坐标
        :param y: 按钮在窗体上的y坐标
        :param text: 按钮显示的文本
        :param imgNormal: surface类型,按钮正常情况下显示的图片
        :param imgMove: surface类型,鼠标移动到按钮上显示的图片
        :param imgDown: surface类型,鼠标按下时显示的图片
        :param callBackFunc: 按钮弹起时的回调函数
        :param font: pygame.font.Font类型,显示的字体
        :param rgb: 元组类型,文字的颜色
        """
        # 初始化按钮相关属性
        self.imgs = []
        if not imgNormal:
            raise Exception("请设置普通状态的图片")
        self.imgs.append(imgNormal)  # 普通状态显示的图片
        self.imgs.append(imgMove)  # 被选中时显示的图片
        self.imgs.append(imgDown)  # 被按下时的图片
        for i in range(2, 0, -1):
            if not self.imgs[i]:
                self.imgs[i] = self.imgs[i - 1]

        self.callBackFunc = callBackFunc  # 触发事件
        self.status = Button.NORMAL  # 按钮当前状态
        self.x = x
        self.y = y
        self.w = imgNormal.get_width()
        self.h = imgNormal.get_height()
        self.text = text
        self.font = font
        # 文字表面
        self.textSur = self.font.render(self.text, True, rgb)

    def draw(self, destSuf):
        dx = (self.w / 2) - (self.textSur.get_width() / 2)
        dy = (self.h / 2) - (self.textSur.get_height() / 2)
        # 先画按钮背景
        if self.imgs[self.status]:
            destSuf.blit(self.imgs[self.status], [self.x, self.y])
        # 再画文字
        destSuf.blit(self.textSur, [self.x + dx, self.y + dy])

    def collide(self, x, y):
        # 碰撞检测
        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            return True
        else:
            return False

    def getFocus(self, x, y):
        # 按钮获得焦点时
        if self.status == Button.DOWN:
            return
        if self.collide(x, y):
            self.status = Button.MOVE
        else:
            self.status = Button.NORMAL

    def mouseDown(self, x, y):
        """通过在这个函数里加入返回值，可以把这个函数当做判断鼠标是否按下的函数，而不仅仅是像这里只有改变按钮形态的作用"""
        if self.collide(x, y):
            self.status = Button.DOWN

    def mouseUp(self):
        if self.status == Button.DOWN:  # 如果按钮的当前状态是按下状态,才继续执行下面的代码
            self.status = Button.NORMAL  # 按钮弹起,所以还原成普通状态
            if self.callBackFunc:  # 调用回调函数
                return self.callBackFunc()


# 障碍物
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = display.resources.enemy1Img
        self.rect = self.image.get_rect()
        self.speed = XoY()
        self.reStart()

    # 对位置和速度重新分配
    def reStart(self):
        self.rect.x = random.randrange(config.ObstacleInitRange.x[0], config.ObstacleInitRange.x[1])
        self.rect.bottom = random.randrange(config.ObstacleInitRange.y[0], config.ObstacleInitRange.y[1])
        self.speed.x = random.randrange(config.ObstacleSpeedRange.x[0], config.ObstacleSpeedRange.x[1])
        self.speed.y = random.randrange(config.ObstacleSpeedRange.y[0], config.ObstacleSpeedRange.y[1])

    def boom(self):
        # todo 被击中爆炸
        self.image = display.resources.enemyD1Img
        self.image = display.resources.enemyD2Img
        self.image = display.resources.enemyD3Img
        self.image = display.resources.enemyD4Img
        self.__init__()

    # 按照预设下落
    def move(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

    # 碰撞检测
    def collide(self):
        # 超出画布底部或超出画布左右
        if self.rect.top > config.DisplayWH[1] or self.rect.right < 0 or self.rect.left > config.DisplayWH[0]:
            self.reStart()  # 障碍物消失重置

        r = pygame.sprite.spritecollide(self, display.allBullets, config.BulletKill)
        if r:
            self.boom()
            # todo 子弹耐久 在碰撞后减少子弹生命

    # 必备更新函数
    def update(self):
        self.move()
        self.collide()


# 玩家类
class Player(pygame.sprite.Sprite):
    # 子弹类（内部类）
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, playerXY, bulletImg):
            pygame.sprite.Sprite.__init__(self)
            self.image = bulletImg
            self.rect = self.image.get_rect()
            self.rect.center = playerXY

        def collide(self):
            if self.rect.bottom < 0:
                self.kill()

        def update(self):
            self.rect.y -= config.BulletSpeedY

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(config.GREEN)
        self.image = display.resources.playerImg
        self.rect = self.image.get_rect()
        # 对象x轴中心点
        self.rect.centerx = config.PlayerInitPos.x
        self.rect.bottom = config.PlayerInitPos.y

        self.HP = config.PlayerHP

    def move(self):
        # 检测按键按下
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_RIGHT] or keyPressed[pygame.K_d]:
            self.rect.x += config.PlayerSpeed.x
        if keyPressed[pygame.K_LEFT] or keyPressed[pygame.K_a]:
            self.rect.x -= config.PlayerSpeed.x

        if keyPressed[pygame.K_UP] or keyPressed[pygame.K_w]:
            self.rect.y -= config.PlayerSpeed.y
        if keyPressed[pygame.K_DOWN] or keyPressed[pygame.K_s]:
            self.rect.y += config.PlayerSpeed.y

    def collide(self):
        # todo 配置文件设置是否可穿墙
        if self.rect.centerx > config.DisplayWH[0]:
            self.rect.centerx = config.DisplayWH[0]
        elif self.rect.centerx < 0:
            self.rect.centerx = 0

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > config.DisplayWH[1]:
            self.rect.bottom = config.DisplayWH[1]

        collideList = pygame.sprite.spritecollide(self, display.allObstacles, False)
        if collideList:
            for o in collideList:
                o.reStart()
            self.collideMe()

    def collideMe(self):
        # todo 血量可视化
        self.HP -= config.PlayerStepSubHP
        if self.HP > 0:
            print("小心！")
        else:
            print("死亡！！！")
            for i in display.allObstacles:
                i.reStart()
            self.__init__()
            display.pause()

    # biu! biu! biu!!!
    def launch(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:  # 检测键盘按下了空格键
            b = self.Bullet(self.rect.center, display.resources.bulletImgList[random.randint(0, 1)])
            display.allSpritesAdd(b)
            display.allBulletsAdd(b)

    def update(self):
        self.move()
        self.collide()
        if config.Le:
            self.launch()  # 不建议启用 发射频率与帧率相关，同时打开函数内按键按下检测


# 整体控制
class Display:

    def __init__(self):

        pygame.init()  # 必须初始化！！
        # 时钟（设置FPS）
        self.clock = pygame.time.Clock()
        # 屏幕宽高
        self.screen = pygame.display.set_mode(config.DisplayWH)
        # 设置标题
        pygame.display.set_caption(config.DisplayTitle)
        # 资源加载
        self.resources = Resources()

        self.__running = True
        self.__pause = False

        self.allSprites = pygame.sprite.Group()  # 全部对象组 便于调用刷新
        self.allObstacles = pygame.sprite.Group()  # 障碍对象组 便于检测碰撞
        self.allBullets = pygame.sprite.Group()  # 子弹对象组 便于检测碰撞
        self.player = None
        self.resumeBtn = None

    def init(self):
        # 创建恢复按钮
        self.resumeBtn = Button(210, 327.5, None, self.resources.resumeBtnNormal, self.resources.resumeBtnNormal,
                                self.resources.resumeBtnDown, self.play, self.resources.btnFont, (255, 0, 0))
        # 玩家对象
        self.player = Player()
        self.allSpritesAdd(self.player)
        self.newObstacle()  # 障碍物对象

    # 塞进组里，直接写会有警告⚠
    def allSpritesAdd(self, obj):
        self.allSprites.add(obj)

    def allObstaclesAdd(self, obj):
        self.allObstacles.add(obj)

    def allBulletsAdd(self, obj):
        self.allBullets.add(obj)

    # 生成障碍物
    def newObstacle(self):

        for i in range(config.ObstacleCount):
            o = Obstacle()
            self.allSpritesAdd(o)
            self.allObstaclesAdd(o)

    # 监听按键事件
    def keyEvent(self):
        for event in pygame.event.get():  # 循环获取事件，监听事件状态
            if event.type == pygame.QUIT:  # 退出程序
                self.bey()
            elif event.type == pygame.KEYDOWN:  # 检测按键按下
                if event.key == pygame.K_SPACE:  # 按下空格键
                    if self.__pause:  # 如果是暂停状态则取消暂停
                        self.play()
                    self.player.launch()  # 发射子弹函数
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                    if self.__pause:  # 如果是暂停状态则取消暂停
                        self.play()
                    else:
                        self.pause()

            mx, my = pygame.mouse.get_pos()  # 获得鼠标坐标
            if event.type == pygame.MOUSEMOTION:  # 鼠标移动事件
                # 判断鼠标是否移动到按钮范围内
                self.resumeBtn.getFocus(mx, my)
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
                if pygame.mouse.get_pressed() == (1, 0, 0):  # 鼠标左键按下
                    self.resumeBtn.mouseDown(mx, my)
            elif event.type == pygame.MOUSEBUTTONUP:  # 鼠标弹起
                self.resumeBtn.mouseUp()

    def pause(self):
        self.__pause = True

    def play(self):
        self.__pause = False

    def pauseEvent(self):
        # self.screen.blit(display.resources.resumeImg, (210, 327.5))
        self.resumeBtn.draw(self.screen)

    # 碰撞检测
    def collide(self):
        pass

    def loop(self):
        self.init()
        # 必须循环，不然游戏就没了!
        while self.__running:
            self.clock.tick(config.DisplayFPS)  # 设置每秒刷新帧数，不大于该值 但性能不足时会小于该值
            self.keyEvent()
            if not self.__pause:
                self.collide()
                # 更新屏幕背景 （不更新会有残影）
                # self.screen.fill(color=config.WHITE)
                self.screen.blit(self.resources.backgroundImg, (0, 0))
                # 调用所有对象的update函数
                self.allSprites.update()
                self.allSprites.draw(self.screen)  # 更新结果绘制到屏幕
            else:
                self.pauseEvent()

            # 更新屏幕内容(翻转白板，将绘制完毕的界面显示至屏幕，可有效消除绘制拖影)
            pygame.display.flip()

    # 程序结束了！！
    def bey(self):
        print("程序结束了！！!")
        self.__running = False
        pygame.quit()  # 卸载所有模块
        sys.exit()  # 终止程序，确保退出程序


if __name__ == '__main__':
    # 读配置参数
    config = Config()
    if not config.readConfig():
        sys.exit()  # 读取失败
    # 开搞!
    display = Display()
    display.loop()
