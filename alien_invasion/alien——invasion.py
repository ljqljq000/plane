import  sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
class AlienInavasion:
    '''管理游戏资源和行为'''
    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        #控制帧率
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # self.screen = pygame.display.set_mode((1200, 800))
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Inavasion')
        #信息统计
        self.stats = GameStats(self)
        #设置背景色
        # self.bg_color = (230, 230, 230)
        self.bg_color = self.settings.bg_color
        #创建飞船实例，同时把游戏的一些数据传递给ship
        self.ship = Ship(self)
        #Group类类似于列表，但提供了有助于开发游戏的额外功能
        self.bullets = pygame.sprite.Group()
        #外星人实例
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # 游戏启动后处于关闭状态，为了添加游戏开始按钮
        self.game_active = False
        #创建play按钮
        self.play_button = Button(self,'play')
        #创建的得分实例
        self.sb = Scoreboard(self)

    def run_game(self):
        '''开始游戏主循环'''
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)
    #重构监听事务
    def _check_events(self):
        # 侦听键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    #重构键盘检测
    def _check_keydown_events(self, event):
        '''响应按下'''
        # 飞船向右移动
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 飞船向左移动
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        #按P键值使游戏开始
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        '''响应释放'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''子弹射击
        创建一颗子弹，并将其加入编组bullets'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    #重构更新屏幕
    def _update_screen(self):
        '''更新屏幕上的图像，并切换到新屏幕'''
        # 每次循环式都重新绘制屏幕
        self.screen.fill(self.bg_color)
        #绘制子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # ，调用 ship.blitme() 将飞船绘制到屏幕上，确保它出现在背景的前面（
        self.ship.blime()
        #绘制外星人
        self.aliens.draw(self.screen)
        #绘制得分板
        self.sb.show_score()
        if not self.game_active:
            #如果游戏处于非活动状态就，绘制play按钮
            self.play_button.draw_button()
        # 让最近绘制的屏幕可见
        pygame.display.flip()


    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
    # 更新子弹的位置
        self.bullets.update()
    # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():#解决碰撞多个只加一个分数问题
                # 如果字典 collisions 存在，就遍历其中的所有值。别忘了，每个值都是
                # 一个列表，包含被同一颗子弹击中的所有外星人
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # 删除现有的所有子弹，并创建一个新的外星舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #提高等级
            self.stats.level += 1
            self.sb.prep_level()

    # 存储外星舰队
    def _create_fleet(self):
        """创建一个外星舰队"""
        # 创建一个外星人
        alien = Alien(self)
        alien_width, alien_height= alien.rect.size
        current_x,current_y = alien_width, alien_height + 80
        while current_y < (self.settings.screen_height -  8 * alien_height):
            while current_x < (self.settings.screen_width - 2 *alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            #添加一行外星人后，重置x值并定增y值
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """创建一个外星人并将其放在当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    #更改外星人的位置
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print('ship hit')
            self._ship_hit()
        # 检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()
    def _check_fleet_edges(self):
        '''在有外星人到达边缘时候采取相应措施'''
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_directin()
                break
    def _change_fleet_directin(self):
        '''碰触到边缘，将整个舰队向下移动，并改变他们的方向'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def _ship_hit(self):
        '''响应碰撞'''
        if self.stats.ships_left > 0:
        # 将 ships_left 减 1
            self.stats.ships_left -= 1
            #重新绘制飞船
            self.sb.prep_ships()
            #清空外星人和子弹
            self.bullets.empty()
            self.aliens.empty()

            #创建新外星战队，将飞船放在底部中央
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(0.5)
        else:
            self.game_active = False
            #重现光标
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        '''检查外星人是否到达底部'''
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #同飞船碰撞处理
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        '''在玩家单击play按钮时候开始游戏'''
        #游戏开始后再次点击该区域无效
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()
    def _start_game(self):
            # 重置命数
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            #重置游戏得分
            self.sb.prep_score()
            #重置等级
            self.sb.prep_level()
            #重置命数
            self.sb.prep_ships()
            self.game_active = True

            # 重置子弹、外星人
            self.bullets.empty()
            self.aliens.empty()

            # 创建一个新的战队,将飞船放在底部
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏光标
            pygame.mouse.set_visible(False)


if __name__ == '__main__':
    ai = AlienInavasion()
    ai.run_game()