import pygame.font
from pygame.sprite import Group
from ship import Ship
import sys

class Scoreboard:
    '''显示得分信息的类'''

    def __init__(self, ai_game):
        '''初试话得分和属性'''
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.stats = ai_game.stats

        #显示得分信息是使用的字体设置
        self.text_color = (30, 30, 30)
        #第一个None是设置字体，设置simsuns是为了支持中文
        self.font = pygame.font.SysFont('SimSun', 20)

        #准备初始化得分图像
        self.prep_score()
        #准备初始化最高分
        self.prep_high_score()
        #游戏等级
        self.prep_level()
        #剩余飞船数
        self.prep_ships()

    def prep_score(self):
        '''将得分渲染为图像'''
        #将分数设置为10的整数倍
        #round() 函数通常让浮点数（第一个实参）精确到小数点后某一位，其中的小数位数由第二个实参指定。如果将第二个实参指定为负数，round()会将第一个实参舍入到最近的 10 的整数倍，如 10、100、1000 等
        rounded_score = round(self.stats.score, -1)
        #在表示得分的 f 字符串中使用一个格式说明符。这里使用的字符序列为冒号和逗号（:,），它让 Python 在数值的合适位置插入逗号，生成的字符串类似于 1,000,000（而不是 1000000）。
        score_str = '得分: ' + f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        #在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        '''在屏幕上显示得分'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self._hight_score_image, self.hight_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = '最高分: ' + f"{high_score :,}"
        self._hight_score_image = self.font.render(high_score_str, True, self.text_color)
        self.hight_score_rect = self._hight_score_image.get_rect()
        self.hight_score_rect.center = self.screen_rect.center
        self.hight_score_rect.top = self.score_rect.top
    def check_high_score(self):
        '''检测最高分'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            #记录最高分
            self.write_high_score()



    def prep_level(self):
        """将等级渲染为图像"""
        level_str = '等级：' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True,self.text_color, self.settings.bg_color)
        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        '''显示剩余多少艘飞船'''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def write_high_score(self):
        '''记录最高分'''
        # 打开文件进行写入
        with open('highscore.txt', 'w') as file:
            file.write(str(self.stats.high_score))

