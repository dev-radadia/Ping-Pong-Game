import pygame

import r

from sprites.Border import *
from sprites.Label import *
from sprites.Button import *

CB_RETURN = 0
CB_PLAY = 4
CB_QUIT = -1

class PauseScreen():
    def __init__(self, screen, pause, screen_dimen, bg_color, fg_color, fontsize1 = r.font_size.xxl, fontsize2 = r.font_size.m, bg=None):
        self.screen = screen
        self.screen_dimen = screen_dimen
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.pause = pause
        self.font1 = pygame.font.Font("r\\font_styles\Courier Italic.ttf", fontsize1)
        self.font2 = pygame.font.Font("r\\font_styles\Courier.ttf", fontsize2)
        self.scores = (0,0)
        self.setDisplay()
        self.bgimg = bg
        
    def pause_game(self):
        buttons = [self.resume_btn, self.quit_btn, self.return_to_mainmenu_btn]

        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
                    
            self.screen.fill(r.game.BLACK)
            
            if self.bgimg is not None:
                self.screen.blit(self.bgimg,(0,0))

            for button in buttons:
                button_action = button.update(pygame.mouse.get_pos(), mouse_up)                    
                if button_action is not None:
                    return button_action
                button.draw(self.screen)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    return CB_PLAY

            border = Border()
            border.rectangle(self.screen)
            
            self.pause_label.draw()
            self.score_label.draw()

            pygame.display.flip()

    def setDisplay(self):
        self.pause_label = Label(self.screen, pygame.Rect(230, 70, 1000 ,1000), self.fg_color, self.bg_color, self.font1, text=self.pause)

        self.score_label = Label(self.screen, pygame.Rect(360, 250, 1000 ,1000), self.fg_color, self.bg_color, self.font2, text=str(self.scores[0])+" : "+str(self.scores[1]))

        self.resume_btn = Button(
            center_position = (r.game.SCREEN_WIDTH/2, 385),
            font_size = r.font_size.m,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.WHITE,
            text = r.pause.resume_button_txt,
            action=CB_PLAY,
        )
        
        self.return_to_mainmenu_btn = Button(
            center_position = (r.game.SCREEN_WIDTH/2, 485),
            font_size = r.font_size.m,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.WHITE,
            text = r.pause.return_to_mainmenu_button_txt,
            action=CB_RETURN,
        )
        
        self.quit_btn = Button(
            center_position = (r.game.SCREEN_WIDTH/2, 585),
            font_size = r.font_size.m,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.WHITE,
            text = r.pause.quit_button_txt,
            action = CB_QUIT,
        )

    def setScores(self,a):
        self.scores=a
        self.score_label = Label(self.screen, pygame.Rect(360, 250, 1000 ,1000), self.fg_color, self.bg_color, self.font2, text=str(self.scores[0])+" : "+str(self.scores[1]))
