class Settings:
    '''存储游戏中所有设置的类'''
    def __init__(self):
        '''初始化游戏设置'''
    #静态设置
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 设置飞船命数
        self.ship_limit = 3

        #子弹设置

        self.bullets_width = 30
        self.bullets_height = 15
        self.bullets_color = (60, 60, 60)
        self.bullets_allowed = 3

        #设置外星人移动速度
        
        self.fleet_drop_speed = 20

        #设置动态外星人移动速度，来提高游戏节奏
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #这里虽然放到了另外一个方法中，但其他的类依然可以用self直接访问到
        self.ship_speed = 5
        self.bullets_speed = 2.0
        self.alien_speed = 1.5
        # fleet_direction 为1表示向右移动，为-1表示想做移动
        self.fleet_direction = 1
        #计分试着
        self.alien_points = 50
    #提高速度
    def increase_speed(self):
        #提高飞船速度、子弹速度、外星人速度、得分
        self.ship_speed *= self.speedup_scale
        self.bullets_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)