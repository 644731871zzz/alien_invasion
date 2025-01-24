import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船发射子弹的类"""

    def __init__(self,ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.bullet_color

        #在(0,0)处创建一个表示子弹矩形,再设置正确的位置
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,
                              self.settings.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop

        #存储用浮点数消失的子弹位置
        self.y=float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        #更新子弹准确的位置
        self.y-=self.settings.bullet_speed
        #更新表示子弹的rect的位置
        self.rect.y=self.y

    def draw_bullet(self):
        """屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)

class AlienBullet(Sprite):
    """管理外星人发射的子弹,这里只创建单个子弹"""
    def __init__(self,ai_game,alien):
        """在外星人位置创建子弹"""
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.alien_bullet_color

        #现在0,0创建矩形,然后再在外星人创建配置位置
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,
                              self.settings.bullet_height)
        self.rect.midbottom=alien.rect.midbottom

        #位置信息储存为浮点值
        self.y=self.rect.y

    def update(self):
        """向下移动外星人的子弹"""
        #更新子弹的位置
        self.y+=self.settings.bullet_speed
        #更新子弹rect位置
        self.rect.y=self.y
    
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)
        
