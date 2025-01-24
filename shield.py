import pygame

class Shield:
    """管理护盾的类"""
    def __init__(self,ai_game):
        #读取基本信息
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.shield_color

        #在(0,0)的位置先绘制一个盾牌
        self.rect=pygame.Rect(0,0,self.settings.shield_width,
                              self.settings.shield_height)
        self.rect.midbottom=ai_game.ship.rect.midtop
        self.rect.y-=11

    def update(self,ai_game):
        #仅在飞船上方移动
        self.rect.x=ai_game.ship.rect.x

    def draw_shield(self):
        """在指定位置绘制护盾"""
        pygame.draw.rect(self.screen,self.color,self.rect)

            
