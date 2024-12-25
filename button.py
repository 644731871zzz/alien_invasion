import pygame.font

class Button:
    """创建按钮类"""

    def __init__(self,ai_game,msg):
        """初始化按钮属性"""
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()

        #设置按钮的尺寸和其他属性
        self.width,self.height=200,50
        self.button_color=(0,135,0)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont(None,48)

        #创建按钮的rect对象,主按钮居中 难度选择按钮在底部部左中右
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center

        self.rect_left=pygame.Rect(0,0,self.width,self.height)
        self.rect_left.bottomleft=self.screen_rect.bottomleft
        self.rect_bottom=pygame.Rect(0,0,self.width,self.height)
        self.rect_bottom.midbottom=self.screen_rect.midbottom
        self.rect_right=pygame.Rect(0,0,self.width,self.height)
        self.rect_right.bottomright=self.screen_rect.bottomright

        #按钮的标签只需要创建一次,msg是要被显示的文本
        self._prep_msg(msg)
        #创建难度按钮标签
        self._prep_number()

    def _prep_msg(self,msg):
        """将msg渲染为图像,并使其再按钮上居中"""
        self.msg_image=self.font.render(msg,True,self.text_color,
                                        self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center

    def _prep_number(self):
        """直接渲染难度的数字"""
        self.number_image1=self.font.render('1.0',True,self.text_color,
                                        self.button_color)
        self.number_image1_rect=self.number_image1.get_rect()
        self.number_image1_rect.center=self.rect_left.center

        self.number_image2=self.font.render('2.0',True,self.text_color,
                                        self.button_color)
        self.number_image2_rect=self.number_image2.get_rect()
        self.number_image2_rect.center=self.rect_bottom.center

        self.number_image3=self.font.render('4.0',True,self.text_color,
                                        self.button_color)
        self.number_image3_rect=self.number_image3.get_rect()
        self.number_image3_rect.center=self.rect_right.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮,再绘制文本"""

        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

        self.screen.fill(self.button_color,self.rect_left)
        self.screen.blit(self.number_image1,self.number_image1_rect)
        self.screen.fill(self.button_color,self.rect_bottom)
        self.screen.blit(self.number_image2,self.number_image2_rect)
        self.screen.fill(self.button_color,self.rect_right)
        self.screen.blit(self.number_image3,self.number_image3_rect)