import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    '''管理飞船的类'''
    #ai_game可以获取实例中产生的数据
    def __init__(self, ai_game):
        super().__init__()
        '''初始化飞船的位置'''
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像并获取外借矩形
        self.image = pygame.image.load('images/ship.bmp')
        new_width = self.image.get_width() // 2  # 缩小为原来的一半宽
        new_height = self.image.get_height() // 4  # 缩小为原来的一半高

        # 缩小图片
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect()

        #使每艘飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 解决rect只处理整数问题
        self.x = float(self.rect.x)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def blime(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        '''根据移动标志调整飞船位置'''
        #更新飞船的值而不是外接矩形属性X的值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        #根据slef.x更新rect对象
        self.rect.x = self.x

    def center_ship(self):
        """将飞船放在屏幕底部的中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)