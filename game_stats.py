class GameStats:
    """跟踪游戏的统计信息"""
    def __init__(self,ai_game):
        """初始化系统信息"""
        self.settings=ai_game.settings
        self.path=ai_game.path
        self.reset_stats()
        #添加任何情况下都不重置的最高分
        self.high_score=int(self.path.read_text())

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left=self.settings.ship_limit
        self.score=0
        self.level=1