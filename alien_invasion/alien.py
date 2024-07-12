import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''表示单个外星人的类
    Alien 类不需要在屏幕上绘制外星人的方法，因为我们将使用一个 Pygame
    编组方法，自动地在屏幕上绘制编组中的所有元素。
    '''

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/alien.bmp')
        new_width = self.image.get_width()   # 缩小为原来的一半宽
        new_height = self.image.get_height() // 2 # 缩小为原来的一半高

        # 缩小图片
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect()
        #位置放在左上角
        self.rect.x = self.rect.width-58
        self.rect.y = self.rect.height-70
        #存储外星人的精确水平位置
        self.x = float(self.rect.x)

    #向右移动外星人
    def update(self):
        '''向左向右移动外星人'''
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
    def check_edge(self):
        """如果外星人位于屏幕边缘，就返回 True"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)