class Settings:
    """存储游戏<<外星人入侵>>的所有的类"""
    def __init__(self):
        """初始化游戏的设置"""
        #屏幕设置
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(230,230,230)

        #飞船的设置
        self.ship_limit=3
        
        #子弹设置
        self.bullet_width=10
        self.bullet_height=15
        self.bullet_color=(60,60,160)
        self.bullets_allowed=3
        self.alien_bullet_color=(250,40,40)

        #护盾设置:
        self.shield_width=60
        self.shield_height=5
        self.shield_color=(20,160,20)

        #外星人设置
        self.fleet_drop_speed=2

        #游戏加快倍数
        self.speedup_scale=2.0
        #外星人分数倍数
        self.score_scale=1.5

        #初始化游戏分数
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed=1.5
        self.bullet_speed=2.5
        self.alien_speed=2.0

        #fleet_direction 1为向右,-1向左
        self.fleet_direction=1

        #记分设置
        self.alien_points=50

    def increase_speed(self):
        """提高游戏速度设置的值"""
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*+self.speedup_scale

        #外星人背时增长
        self.alien_points=int(self.alien_points*self.score_scale)
        print(self.alien_points)