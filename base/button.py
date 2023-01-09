# 按钮
class Button:
    NORMAL = 0
    MOVE = 1
    DOWN = 2

    def __init__(self, x, y, text, img_normal, img_move=None, img_down=None,
                 call_back_func=None, font=None, rgb=(0, 0, 0)):
        """
        初始化按钮的相关参数
        :param x: 按钮在窗体上的x坐标
        :param y: 按钮在窗体上的y坐标
        :param text: 按钮显示的文本
        :param img_normal: surface类型,按钮正常情况下显示的图片
        :param img_move: surface类型,鼠标移动到按钮上显示的图片
        :param img_down: surface类型,鼠标按下时显示的图片
        :param call_back_func: 按钮弹起时的回调函数
        :param font: pygame.font.Font类型,显示的字体
        :param rgb: 元组类型,文字的颜色
        """
        # 初始化按钮相关属性
        self.images = []
        if not img_normal:
            raise Exception("请设置普通状态的图片")
        self.images.append(img_normal)  # 普通状态显示的图片
        self.images.append(img_move)  # 被选中时显示的图片
        self.images.append(img_down)  # 被按下时的图片
        for i in range(2, 0, -1):
            if not self.images[i]:
                self.images[i] = self.images[i - 1]

        self.callBackFunc = call_back_func  # 触发事件
        self.status = Button.NORMAL  # 按钮当前状态
        self.x = x
        self.y = y
        self.w = img_normal.get_width()
        self.h = img_normal.get_height()
        self.text = text
        self.font = font
        # 文字表面
        self.textSur = self.font.render(self.text, True, rgb)

    def draw(self, suf):
        dx = (self.w / 2) - (self.textSur.get_width() / 2)
        dy = (self.h / 2) - (self.textSur.get_height() / 2)
        # 先画按钮背景
        if self.images[self.status]:
            suf.blit(self.images[self.status], [self.x, self.y])
        # 再画文字
        suf.blit(self.textSur, [self.x + dx, self.y + dy])

    def collide(self, x, y):
        # 碰撞检测
        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            return True
        else:
            return False

    def get_focus(self, x, y):
        # 按钮获得焦点时
        if self.status == Button.DOWN:
            return
        if self.collide(x, y):
            self.status = Button.MOVE
        else:
            self.status = Button.NORMAL

    def mouse_down(self, x, y):
        """通过在这个函数里加入返回值，可以把这个函数当做判断鼠标是否按下的函数，而不仅仅是像这里只有改变按钮形态的作用"""
        if self.collide(x, y):
            self.status = Button.DOWN

    def mouse_up(self):
        if self.status == Button.DOWN:  # 如果按钮的当前状态是按下状态,才继续执行下面的代码
            self.status = Button.NORMAL  # 按钮弹起,所以还原成普通状态
            if self.callBackFunc:  # 调用回调函数
                return self.callBackFunc()
