import pygame

from sprites.Border import *
from sprites.Label import *
from sprites.Button import *

import r

CB_RETURN = 0
CB_PAUSE = 1
CB_ENDGAME = 2
CB_QUIT = -1
CB_PLAY = 4

class EndgameScreen():

    def __init__(self, screen, win, screen_dimen, bg_color, fontsize = r.font_size.xxl, bg=None):
        self.screen = screen
        self.screen_dimen = screen_dimen
        self.bg_color = bg_color
        self.win = win
        self.font = pygame.font.Font("r\\font_styles\Courier Bold.ttf",fontsize)
        self.winnerName = ""
        self.winnerColor = r.colors.WHITE
        self.bgimg = bg
        self.setDisplay()

    def setWinnerColor(self, winnerColor):
        self.winnerColor = winnerColor
        
        self.winner_label = Button(
            center_position=(r.game.SCREEN_WIDTH/2, 100),
            font_size=r.font_size.xxl,
            bg_rgb=r.colors.BLACK,
            text_rgb=self.winnerColor,
            text=self.winnerName,
        )
        
        self.win_label = Label(self.screen, pygame.Rect(225, 185, 1000 ,1000), self.winnerColor, self.bg_color, self.font, text=self.win)

    def setWinnerName(self, winnerName):
        self.winnerName = winnerName
        
        self.winner_label = Button(
            center_position=(r.game.SCREEN_WIDTH/2, 100),
            font_size=r.font_size.xxl,
            bg_rgb=r.colors.BLACK,
            text_rgb=self.winnerColor,
            text=self.winnerName,
        )
        
        self.win_label = Label(self.screen, pygame.Rect(225, 185, 1000 ,1000), self.winnerColor, self.bg_color, self.font, text=self.win)

    def showEndScreen(self):
        self.winner_label.setHighlightable(False)
        
        buttons = [self.winner_label, self.play_btn, self.return_to_mainmenu_btn, self.quit_btn]

        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return CB_QUIT
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True

            self.screen.fill(r.colors.BLACK)

            if self.bgimg is not None:
                self.screen.blit(self.bgimg,(0,0))
                
            for button in buttons:
                button_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if button_action is not None:
                    return button_action
                button.draw(self.screen)

            border = Border()
            border.rectangle(self.screen)

            keys=pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                return CB_QUIT
            
            self.win_label.draw()

            pygame.display.flip()

    def setDisplay(self):
        self.play_btn =  Button(
            center_position = (r.game.SCREEN_WIDTH/2, 390),
            font_size = r.font_size.m,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.WHITE,
            text = r.endgame.play_again_btn_txt,
            action = CB_PLAY
        )
        self.return_to_mainmenu_btn = Button(
            center_position = (r.game.SCREEN_WIDTH/2, 490), 
            font_size = r.font_size.m,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.WHITE,
            text = r.endgame.return_to_mainmenu_button_txt,
            action = CB_RETURN
        )
        self.quit_btn = Button(
            center_position = (r.game.SCREEN_WIDTH/2, 590),
            font_size = r.font_size.m,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.WHITE,
            text = r.endgame.quit_button_txt,
            action = CB_QUIT,
        )
