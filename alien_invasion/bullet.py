import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''
    #通过使用精灵（sprite），可将游戏中相关的元素编组，进而同时操作编组中的所有元素
    管理飞船所发射子弹的类
    为了创建子弹实例，__init__() 需要当前的 AlienInvasion 实例，因此调用 super() 来继承 Sprite。
    '''
    def __init__(self, ai_game):
        '''管理飞船发射子弹的类'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullets_color
        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullets_width, self.settings.bullets_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        # 存储用浮点数表示的子弹位置
        self.y = float(self.rect.y)

    def update(self):
        '''向上移动子弹'''
        # 更新子弹的准确位置
        self.y -= self.settings.bullets_speed
        # 更新表示子弹的 rect 的位置
        self.rect.y = self.y
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
