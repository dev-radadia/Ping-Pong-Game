import pygame
import pygame.freetype

import r

from sprites.Border import *
from sprites.Label import *
from sprites.Button import *

CB_1PLAYER = 1
CB_2PLAYERS = 2
CB_QUIT = -1
CB_ABOUT = 7

class MainMenuScreen():
    def __init__(self, screen, gamename, screen_dimen, bg_color, fg_color, fontsize = r.font_size.xxxl, bg=None):
        self.screen = screen
        self.screen_dimen = screen_dimen
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.gamename = gamename
        self.font = pygame.font.Font("r\\font_styles\Courier Italic.ttf", fontsize)
        self.bgimg = bg

    def show_menu(self):
        game_name = Label(self.screen, pygame.Rect(90, 100, 1000 ,1000), self.fg_color, self.bg_color, self.font, text=self.gamename)

        Player1_btn = Button(
            center_position=(r.game.SCREEN_WIDTH/4, 430),
            font_size=r.font_size.m,
            bg_rgb=r.colors.BLACK,
            text_rgb=r.colors.WHITE,
            text=r.main.r_1Player_txt,
            action=CB_1PLAYER,
        )
        Players2_btn = Button(
            center_position=(3*(r.game.SCREEN_WIDTH/4), 430),
            font_size=r.font_size.m,
            bg_rgb=r.colors.BLACK,
            text_rgb=r.colors.WHITE,
            text=r.main.r_2Players_txt,
            action=CB_2PLAYERS,
        )
        about_btn=Button( 
            center_position=(r.game.SCREEN_WIDTH/2, 515),
            font_size=r.font_size.m,
            bg_rgb=r.colors.BLACK,
            text_rgb=r.colors.WHITE,
            text=r.main.r_about_button_txt,
            action=CB_ABOUT,
        )
        quit_btn = Button(
            center_position=(r.game.SCREEN_WIDTH/2, 600),
            font_size=r.font_size.m,
            bg_rgb=r.colors.BLACK,
            text_rgb=r.colors.WHITE,
            text=r.main.r_quit_button_txt,
            action=CB_QUIT,
        )
        
        buttons = [Player1_btn, Players2_btn, about_btn, quit_btn]

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

            border = Border()
            border.rectangle(self.screen)
            game_name.draw()

            pygame.display.flip()
