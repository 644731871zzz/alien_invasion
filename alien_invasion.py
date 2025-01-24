import sys
from time import sleep
from pathlib import Path

import pygame

import random

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from bullet import AlienBullet
from alien import Alien
from shield import Shield

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        pygame.mixer.init()
        self.clock=pygame.time.Clock()
        self.settings=Settings()

        self.screen=pygame.display.set_mode(
        (self.settings.screen_width,self.settings.screen_height))
        #创建窗口名称
        pygame.display.set_caption("Alien Invasion")

        #加载音频
        self.sound_ship=pygame.mixer.Sound(
            '/Users/arch/Desktop/python_work/Python_Crash_Course/alien_invasion/music/ship.mp3')
        self.sound_alien=pygame.mixer.Sound(
            '/Users/arch/Desktop/python_work/Python_Crash_Course/alien_invasion/music/alien.mp3')

        self.path=Path('/Users/arch/Desktop/python_work/Python_Crash_Course/alien_invasion/high_score.txt')

        #创建用于存储游戏统计信息的实例
        self.stats=GameStats(self)
        self.sb=Scoreboard(self)

        self.ship=Ship(self)
        self.shield=Shield(self)
        self.bullets=pygame.sprite.Group()
        self.alien_bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()

        self._create_fleet()

        self.game_active=False

        #创建按钮,其中带有难度按钮
        self.play_button=Button(self,"Play")

     
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self.shield.update(self)
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """相应按键和鼠标的事件"""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.path.write_text(f'{self.stats.high_score}')
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        """玩家单机play按钮时候开始新游戏,还有更改难度,按下难度键仅仅更改难度不开始游戏"""
        #按Play
        button_chicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_chicked and not self.game_active:
            self._start_game()
            self.sb.prep_images()
        #按下难度1键
        button_chicked1=self.play_button.rect_left.collidepoint(mouse_pos)
        if button_chicked1 and not self.game_active:
            #还原游戏设置
            self.settings.initialize_dynamic_settings()
            print("1.0")

        #按下难度2
        button_chicked2=self.play_button.rect_bottom.collidepoint(mouse_pos)
        if button_chicked2 and not self.game_active:
            #还原游戏设置,然后配置游戏速率
            self.settings.initialize_dynamic_settings()
            self.settings.increase_speed()
            print("2.0")

        #按下难度4
        button_chicked3=self.play_button.rect_right.collidepoint(mouse_pos)
        if button_chicked3 and not self.game_active:
            #还原游戏设置,然后配置游戏速率
            self.settings.initialize_dynamic_settings()
            self.settings.increase_speed()
            self.settings.increase_speed()
            print("4.0")


    def _check_keydown_events(self,event):
        """响应按下"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_q:
            self.path.write_text(f'{self.stats.high_score}')
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()
        
    def _check_keyup_events(self,event):
        """响应释放"""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False
    
    def _start_game(self):
        """响应play操作,然后开始游戏"""
        #重置游戏的系统信息
        self.stats.reset_stats()
        self.game_active=True

        #清空外星人列表和子弹列表
        self.bullets.empty()
        self.aliens.empty()
        self.alien_bullets.empty()

        #创建一个新的外星人舰队,并将飞船放在屏幕底部中央
        self._create_fleet()
        self.ship.center_ship()

        #隐藏光标
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """创建一颗子弹并加入编组 然后响应声音"""
        if len(self.bullets)<self.settings.bullets_allowed:  
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
            self.sound_ship.play()

    def _alien_fire_bullet(self):
        """为每一个外星人创建一颗外星人的子弹并加入编组"""
        for alien in self.aliens.sprites():
            #创建随机数,每个外星人都有5%的几率发射子弹 并响应声音
            random_int=random.randint(1,20)
            if random_int==1:
                new_alien_bullet=AlienBullet(self,alien)
                self.alien_bullets.add(new_alien_bullet)
                self.sound_alien.play()

    def _update_bullets(self):
        """更新子弹的位置并删除已经消失的子弹"""
        #更新子弹的位置
        self.bullets.update()
        self.alien_bullets.update()

        #删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

        #处理子弹与外星人的碰撞
        self._check_bullet_alien_collisions()
        #处理盾牌和外星人子弹的碰撞
        self._check_alien_bullet_shield_collisions()
        #处理外星人子弹与飞船碰撞
        self._check_alien_bullet_ship_collisions()

    def _check_bullet_alien_collisions(self):

        #检查是否有子弹击中了外星人.如果是,就删除相应的子弹和外星人
        collisions=pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score+=(self.settings.alien_points*len(aliens))
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #删除现有子弹并创建新的外星舰队,然后增加游戏难度
            self.start_new_level()

    def _check_alien_bullet_shield_collisions(self):
        """检查外星人子弹是否击中了盾牌,如果是,这个外星人子弹将会清除"""
        #这个函数将会返回第一个碰到的精灵,然后再用精灵组删除
        alienbullet=pygame.sprite.spritecollideany(
            self.shield,self.alien_bullets)
        self.alien_bullets.remove(alienbullet)
            
    
    def _check_alien_bullet_ship_collisions(self):
        """检查是外星人子弹是否击中了飞船"""
        if pygame.sprite.spritecollideany(
            self.ship,self.alien_bullets):
            self._ship_hit()
        
        

    def start_new_level(self):
        """删除现有子弹然后增加游戏难度"""
        #删除现有子弹并创建新的外星人舰队
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        #提高当前游戏等级的记数,并且重新进行绘制
        self.stats.level+=1
        self.sb.prep_level()


    def _update_aliens(self):
        """更新外星舰队中外星人的位置"""
        #检查是否到达边缘
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom( )

    def _create_fleet(self):
        """创建一个外星人舰队"""
        #创建一个外星人,再不断添加,直到没有空间添加外星人为止
        #外星人的间距为外星人的宽度
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size

        current_x,current_y=alien_width,alien_height
        while current_y <(self.settings.screen_height-3*alien_height):
            while current_x<(self.settings.screen_width-2*alien_width):
                self._create_alien(current_x,current_y)
                current_x+=2*alien_width

            #添加第一行外星人后重置x并且递增y
            current_x=alien_width
            current_y+=2*alien_height

    def _create_alien(self,x_position,y_position):
        """创建一个外星人并将其放在当前行中"""
        new_alien=Alien(self)
        new_alien.x=x_position
        new_alien.rect.x=x_position
        new_alien.rect.y=y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                self._alien_fire_bullet()
                break

    def _change_fleet_direction(self):
        """将整个外星人舰队向下移动,并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _ship_hit(self):
        """相应飞船和外星人的碰撞"""
        if self.stats.ships_left>0:
            #将ship_left-=1 并更新飞船剩余统计
            self.stats.ships_left-=1
            self.sb.prep_ships()

            #清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            self.alien_bullets.empty()

            #创建一个新的外星舰队,并将飞船放在屏幕底部
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(0.5)
        else:
            self.game_active=False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=self.settings.screen_height:
                #像飞船被撞到一样进行处理
                self._ship_hit()
                break
    
    def _update_screen(self):
        """更新屏幕上的图像"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()
        self.ship.blitme()
        self.shield.draw_shield()
        self.aliens.draw(self.screen)
        #显示得分
        self.sb.show_score()

        #如果游戏处于非活跃状态显示Play按钮
        if not self.game_active:
            self.play_button.draw_button()

        #将画面显示到屏幕上
        pygame.display.flip()

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()