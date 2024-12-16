class Settings:
    """存储游戏<<外星人入侵>>的所有的类"""
    def __init__(self):
        """初始化游戏的设置"""
        #屏幕设置
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(230,230,230)

        #飞船的设置
        self.ship_speed=1.5
        self.ship_limit=3
        
        #子弹设置
        self.bullet_speed=2.5
        self.bullet_width=300
        self.bullet_height=15
        self.bullet_color=(60,60,160)
        self.bullets_allowed=3

        #外星人设置
        self.alien_speed=1.0
        self.fleet_drop_speed=100
        #fleet_direction 为1向右移动 -1为向左移动
        self.fleet_direction=1