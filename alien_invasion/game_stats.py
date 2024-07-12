import sys
class GameStats:
    """跟踪游戏的统计信息"""
    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        #任何情况下都不应该重置最高分
        try:
            with open('highscore.txt', 'r') as file:  old_socre = int(file.readline())
        except FileNotFoundError:
            old_socre = 0
        if old_socre > 0:
            self.high_score = old_socre
        else:
            self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        #还有几条命
        self.ships_left = self.settings.ship_limit
        self.score = 0
        #游戏等级
        self.level = 1

