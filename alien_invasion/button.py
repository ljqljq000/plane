import pygame
from pygame import font

class Button:
    '''创建游戏按钮类'''
    def __init__(self, ai_game,msg):
        '''初始化按钮属性'''
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #设置按钮尺寸和字体
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #创建按钮rect对象，居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #按钮只需要创建一次
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        '''将msg渲染为图像，使其在按钮上组中
        font.render() 方法还接受一个布尔实参，该实参指定是否开启反锯齿功能（反锯齿让文本的边缘更平滑）。余下的两个实参分别是文本颜色和背景色'''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self):
        '''绘制一个用颜色填充的按钮，再绘制文本'''
        #绘制按钮
        self.screen.fill(self.button_color, self.rect)
        #绘制图像
        self.screen.blit(self.msg_image, self.msg_image_rect)