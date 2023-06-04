import pygame

import random

import r
from r.playernames import *
from r.game import *

from sprites.Border import *
from sprites.Label import *
from sprites.Button import *
from sprites.Textbox import *

CB_RETURN = 101
CB_PLAY = 104

BLUE=0
PINK=1
GREEN=2
YELLOW=3
RED=4
P1=0
P2=1

COLOR_BTN_ACTIONS=[BLUE*10+P1,PINK*10+P1,GREEN*10+P1,YELLOW*10+P1,RED*10+P1,BLUE*10+P2,PINK*10+P2,GREEN*10+P2,YELLOW*10+P2,RED*10+P2]

COLOR_LIST=[r.colors.BLUE,r.colors.PINK,r.colors.GREEN,r.colors.YELLOW,r.colors.RED]

_color_default=(255,255,255)

class PlayerNamesScreen():
    def __init__(self, screen, playernames, player1, player2, name, screen_dimen, bg_color, fg_color, fontsize1 = r.font_size.l, fontsize2 = r.font_size.m, fontsize3 = r.font_size.xs, bg=None):
        self.screen = screen
        self.screen_dimen = screen_dimen
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.playernames = playernames
        self.player1 = player1
        self.player2 = player2
        self.name = name
        self.font1 = pygame.font.Font("r\\font_styles\Courier Bold Italic.ttf", fontsize1)
        self.font2 = pygame.font.Font("r\\font_styles\Courier Italic.ttf", fontsize2)
        self.font3 = pygame.font.Font("r\\font_styles\Courier.ttf", fontsize3)
        self.playersReset()
        self.bgimg = bg

    def Players_Names(self):
        self.playersReset()

        Player_Names = Label(self.screen, pygame.Rect(165, 10, 1000 ,1000), self.fg_color, self.bg_color, self.font1, text=self.playernames)
        
        Player1 = Label(self.screen, pygame.Rect(80, 100, 1000 ,1000), self.fg_color, self.bg_color, self.font2, text=self.player1)

        Name1 = Label(self.screen, pygame.Rect(15, 187, 1000 ,1000), self.fg_color, self.bg_color, self.font3, text=self.name)

        Player2 = Label(self.screen, pygame.Rect(535, 100, 1000 ,1000), self.fg_color, self.bg_color, self.font2, text=self.player2)

        Name2 = Label(self.screen, pygame.Rect(465, 187, 1000 ,1000), self.fg_color, self.bg_color, self.font3, text=self.name)

        enter_btn = Button(
            center_position = (SCREEN_WIDTH/2, 550),
            font_size = r.font_size.s,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.WHITE,
            text = enter_button_txt,
            action = CB_PLAY,
        )
        
        return_to_mainmenu_btn = Button(
            center_position = (r.game.SCREEN_WIDTH/2, 620),
            font_size = r.font_size.s,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.WHITE,
            text = return_to_mainmenu_button_txt,
            action=CB_RETURN,
        )

        self.setColorButtons()

        buttons = [self.Blue1, self.Green1, self.Yellow1, self.Pink1, self.Red1, self.Blue2, self.Green2, self.Yellow2, self.Pink2, self.Red2, enter_btn, return_to_mainmenu_btn]

        P1 = Textbox(180, 190, 200, 30)
        P2 = Textbox(SCREEN_WIDTH/2+180, 190, 200, 30)

        textboxes = [P1, P2]

        while True:
            mouse_up = False
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
                    
            self.screen.fill(r.game.BLACK)

            if self.bgimg is not None:
                self.screen.blit(self.bgimg,(0,0))

            for textbox in textboxes:
                textbox.handle_event(events)
                textbox.draw(self.screen)

            for button in buttons:
                button_action = button.update(pygame.mouse.get_pos(), mouse_up)

                if button_action is not None:    
                    if button_action==CB_PLAY:
                        self.p1name=P1.getText()
                        self.p2name=P2.getText()
                        
                        if self.p1name == '' or self.p1name.isspace():
                            self.p1name = "Player1"
                        if self.p2name == '' or self.p2name.isspace():
                            self.p2name = "Player2"

                    if button_action in COLOR_BTN_ACTIONS:
                        self.handleColorClick(button_action)
                    else:
                        return button_action

                pygame.draw.line(self.screen,r.colors.WHITE,[r.game.SCREEN_WIDTH/2,95],[r.game.SCREEN_WIDTH/2,505],5)

                button.draw(self.screen)

            border = Border()
            border.rectangle(self.screen)

            Player_Names.draw()
            Player1.draw()
            Name1.draw()
            Player2.draw()
            Name2.draw()

            pygame.display.flip()

    def handleColorClick(self, clicked):
        i=P1
        for p in self.colorBtnList:
            if p[clicked//10].staysHighlighted() and i!=clicked%10:
                return
            i+=1

        for btn in self.colorBtnList[clicked%10]:
            btn.stayHighlighted(False)

        self.colorBtnList[clicked%10][clicked//10].stayHighlighted(True)
        if clicked%10==P1:
            self.color1=COLOR_LIST[clicked//10]
        elif clicked%10==P2:
            self.color2=COLOR_LIST[clicked//10]

    def getPlayer1Name(self):
        return self.p1name
    
    def getColor1(self):
        return self.color1
    
    def getPlayer2Name(self):
        return self.p2name
    
    def getColor2(self):
        return self.color2

    def setColorButtons(self):
        self.Blue1 = Button(
            center_position = (SCREEN_WIDTH/4, 270),
            font_size = r.font_size.xs,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.BLUE,
            text = color_blue_label_txt,
            action = BLUE*10+P1,
        )
        self.Pink1 = Button(
            center_position = (SCREEN_WIDTH/4, 320),
            font_size = r.font_size.xs,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.PINK,
            text = color_pink_label_txt,
            action = PINK*10+P1,
        )
        self.Green1 = Button(
            center_position = (SCREEN_WIDTH/4, 370),
            font_size = r.font_size.xs,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.GREEN,
            text = color_green_label_txt,
            action = GREEN*10+P1,
        )
        self.Yellow1 = Button(
            center_position = (SCREEN_WIDTH/4, 420),
            font_size = r.font_size.xs,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.YELLOW,
            text = color_yellow_label_txt,
            action = YELLOW*10+P1,
        )
        self.Red1 = Button(
            center_position = (SCREEN_WIDTH/4, 470),
            font_size = r.font_size.xs,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.RED,
            text = color_red_label_txt,
            action = RED*10+P1,
        )

        self.Blue2 = Button(
            center_position = (3*(SCREEN_WIDTH/4), 270),
            font_size = r.font_size.xs,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.BLUE,
            text = color_blue_label_txt,
            action = BLUE*10+P2,
        )
        self.Pink2 = Button(
            center_position = (3*(SCREEN_WIDTH/4), 320),
            font_size = r.font_size.xs,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.PINK,
            text = color_pink_label_txt,
            action = PINK*10+P2,
        )
        self.Green2 = Button(
            center_position = (3*(SCREEN_WIDTH/4), 370),
            font_size = r.font_size.xs,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.GREEN,
            text = color_green_label_txt,
            action = GREEN*10+P2,
        )
        self.Yellow2 = Button(
            center_position = (3*(SCREEN_WIDTH/4), 420),
            font_size = r.font_size.xs,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.YELLOW,
            text = color_yellow_label_txt,
            action = YELLOW*10+P2,
        )
        self.Red2 = Button(
            center_position = (3*(SCREEN_WIDTH/4), 470),
            font_size = r.font_size.xs,
            bg_rgb = r.colors.BLACK,
            text_rgb = r.colors.RED,
            text = color_red_label_txt,
            action = RED*10+P2,
        )

        self.colorBtnList=[[self.Blue1,self.Pink1,self.Green1,self.Yellow1,self.Red1], [self.Blue2,self.Pink2,self.Green2,self.Yellow2,self.Red2]]

    def playersReset(self):
        self.p1name="Player1"
        self.p2name="Player2"
        self.color1=_color_default
        self.color2=_color_default
