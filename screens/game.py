import pygame

from sprites.Border import *
from sprites.Paddle import *
from sprites.Ball import *
from sprites.Label import *
from sprites.Button import *
from sprites.PauseButton import *

import r

from r.main import *
from r.game import *

CB_RETURN = 0
CB_PAUSE = 1
CB_ENDGAME = 2
CB_QUIT = -1

IND_BVELX=0
IND_BVELY=1
IND_BVELXP=10
IND_BVELYP=11
IND_BPOSX=2
IND_BPOSY=3
IND_BPOSXP=6
IND_BPOSYP=7
IND_PPOSX=4
IND_PPOSY=5
IND_PPOSXP=8
IND_PPOSYP=9

I_UP=1
I_DOWN=0

fg_color_default=(255,255,255)

class GameScreen():
    def __init__(self, screen, screen_dimen, bg_color, fg_color, score_margin, fps):
        self.screen=screen
        self.screen_dimen = screen_dimen
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.score_margin=score_margin

        self.fps=fps

        self.border = Border()

        self.p1Name = "Player1"
        self.p2Name = "Player2"

        self.winnerName = "Winner"
        self.winnerColor = fg_color_default

        self.loserName = "Loser"

        self.winnerScore = 0
        self.loserScore = 0

        self.color1=fg_color_default
        self.color2=fg_color_default

        self.game_obj = ""

        self.bounce_acceleration = 1
        
        self.font1 = pygame.font.Font("r\\font_styles\Courier.ttf", r.font_size.xxxxl)
        self.font2 = pygame.font.Font("r\\font_styles\Courier Bold Italic.ttf", r.font_size.xl)
        self.font3 = pygame.font.Font(None,r.font_size.l)

        self.collideSound = pygame.mixer.Sound('sound/bounce1.wav')
        self.crossedSound = pygame.mixer.Sound('sound/bounce2.wav')

    def gameReset(self):
        self.score1 = 0
        self.score2 = 0

        self.paddle1.rect.x = self.paddle_margin
        self.paddle1.rect.y = self.screen_dimen[1]//2 - self.paddle_dimen[1]//2 + self.score_margin//2

        self.paddle2.rect.x = SCREEN_WIDTH - PADDLE_WIDTH - PADDLE_MARGIN
        self.paddle2.rect.y = self.screen_dimen[1]//2 - self.paddle_dimen[1]//2 + self.score_margin//2

        self.ball.ballReset()

    def collides(self):
        if (self.ball.x <= self.paddle1.rect.x + self.paddle_dimen[0] and self.ball.x >= self.paddle1.rect.x + self.paddle_dimen[0] - self.ball.speed*3) and (self.ball.y + self.ball_dimen[1] >= self.paddle1.rect.y and self.ball.y <=self.paddle1.rect.y + self.paddle_dimen[1]):
            return 1
        if (self.ball.x >= self.paddle2.rect.x - self.ball.ball_dimen[0] and self.ball.x <= self.paddle2.rect.x - self.ball.ball_dimen[0] + self.ball.speed*3) and (self.ball.y + self.ball_dimen[1] >= self.paddle2.rect.y and self.ball.y <=self.paddle2.rect.y + self.paddle_dimen[1]):
            return 2
        return 0

    def play(self):
        clock = pygame.time.Clock()

        self.ball.setResetMargin(self.ball_reset_margin)
        self.ball.setBounceBias(self.bounce_bias)
        self.ball.update()

        movingsprites = pygame.sprite.Group()
        movingsprites.add(self.paddle1)
        movingsprites.add(self.paddle2)
        movingsprites.add(self.ball)

        pausebtn = PauseButton(action = CB_PAUSE)
        buttons = [pausebtn]

        self.countdown()
        
        exit_window = False

        while not exit_window:
            mouse_up=False
            self.screen.fill(self.bg_color)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_window = True
                    return CB_QUIT
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True

            for button in buttons:
                button_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if button_action is not None:
                    return button_action
                
                button.draw(self.screen)

            self.border.rectangle(self.screen)

            self.ball.update()
            
            if self.collides() == 1:
                self.collideSound.play()
                diff = (self.paddle1.rect.y + self.paddle_dimen[1]/2) - (self.ball.rect.y+self.ball_dimen[1]/2)
                self.ball.x = self.paddle_margin+self.paddle_dimen[0] + 2
                self.ball.bounce(diff)
                self.ball.speed = self.ball.speed*self.bounce_acceleration
                
            if self.collides() == 2:
                self.collideSound.play()
                diff = (self.paddle2.rect.y + self.paddle_dimen[1]/2) - (self.ball.rect.y+self.ball_dimen[1]/2) 
                self.ball.x = self.screen_dimen[0] - (self.paddle_margin+self.ball_dimen[0]+self.paddle_dimen[0]+2)
                self.ball.bounce(-diff)
                self.ball.speed = self.ball.speed*self.bounce_acceleration

            if self.ball.crossed(self.paddle_margin//2):
                self.score2+=1
            if self.ball.crossed(self.screen_dimen[0]-self.paddle_margin//2):
                self.score1+=1

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.paddle1.moveUp(self.paddle_speed)
            if keys[pygame.K_s]:
                self.paddle1.moveDown(self.paddle_speed)

            if keys[pygame.K_UP]:
                    self.paddle2.moveUp(self.paddle_speed)
            if keys[pygame.K_DOWN]:
                    self.paddle2.moveDown(self.paddle_speed)

            if keys[pygame.K_ESCAPE]:
                exit_window = True
                self.gameReset()
                return CB_RETURN

            if keys[pygame.K_p]:
                return CB_PAUSE

            movingsprites.update()

            pygame.draw.line(self.screen,r.colors.WHITE,[self.screen_dimen[0]//2,self.score_margin],[self.screen_dimen[0]//2,self.screen_dimen[1]],5)

            pygame.draw.line(self.screen,r.colors.WHITE,[0,self.score_margin],[self.screen_dimen[0],self.score_margin],5)

            movingsprites.draw(self.screen)

            text1 = self.font3.render(str(self.score1),1,r.colors.WHITE)
            self.screen.blit(text1,(int(self.screen_dimen[0]/4),10))
            
            text2 = self.font3.render(str(self.score2),1,r.colors.WHITE)
            self.screen.blit(text2,(3*int(self.screen_dimen[0]/4),10))

            if self.score1 == 10 or self.score2 == 10:
                self.crossedSound.play()
                if self.score1 == 10:
                    self.winnerName = self.p1Name
                    self.winnerScore = self.score1
                    self.loserName = self.p2Name
                    self.loserScore = self.score2
                    self.winnerColor = self.color1
                if self.score2 == 10:
                    self.winnerName = self.p2Name
                    self.winnerScore = self.score2
                    self.loserName = self.p1Name
                    self.loserScore = self.score1
                    self.winnerColor = self.color2
                    
                self.gameReset()
                                
                return CB_ENDGAME

            pygame.display.flip()

            clock.tick(self.fps)

    def countdown(self):
        clock = pygame.time.Clock()
        
        three = Label(self.screen, pygame.Rect(380, 240, 1000 ,1000), self.fg_color, self.bg_color, self.font1, text="3")

        two = Label(self.screen, pygame.Rect(380, 240, 1000 ,1000), self.fg_color, self.bg_color, self.font1, text="2")

        one = Label(self.screen, pygame.Rect(380, 240, 1000 ,1000), self.fg_color, self.bg_color, self.font1, text="1")

        go = Label(self.screen, pygame.Rect(285, 240, 1000 ,1000), self.fg_color, self.bg_color, self.font1, text="GO!")

        game_objective = Label(self.screen, pygame.Rect(145, 490, 1000 ,1000), self.fg_color, self.bg_color, self.font2, text=self.game_obj)

        for i in range(1,self.fps*4+1):
            self.screen.fill(self.bg_color)

            self.border.rectangle(self.screen)

            game_objective.draw()
            
            num = 4 - i//self.fps
            
            if num == 1:
                go.draw()
            elif num == 2:
                one.draw()
            elif num == 3:
                two.draw()
            elif num == 4:
                three.draw()

            pygame.display.flip()
            
            clock.tick(self.fps)     

    def setGameObjective(self, game_obj):
        self.game_obj=game_obj

    def setMovables(self, ball_radius, paddle_dimen, color1, color2):
        self.paddle_dimen=paddle_dimen
        self.color1=color1
        self.color2=color2
        
        self.ball_dimen=(ball_radius,ball_radius)
        
        self.ball=Ball(self.ball_dimen, self.screen_dimen, self.paddle_dimen, self.score_margin)
        self.ball_group=pygame.sprite.Group()
        self.ball_group.add(self.ball)

        self.paddle1=Paddle(self.screen_dimen, self.paddle_dimen, self.score_margin, self.color1)
        self.paddle2=Paddle(self.screen_dimen, self.paddle_dimen, self.score_margin, self.color2)

        self.gameReset()

    def setPaddleMargin(self, paddle_margin):
        self.paddle_margin=paddle_margin

    def setPaddleSpeed(self, paddle_speed):
        self.paddle_speed=paddle_speed

    def setBallResetMargin(self, ball_reset_margin):
        self.ball_reset_margin=ball_reset_margin

    def setBounceBias(self, bounce_bias):
        self.bounce_bias=bounce_bias

    def setPlayer1Name(self, p1Name):
        self.p1Name=p1Name
        
    def setPlayer2Name(self, p2Name):
        self.p2Name=p2Name

    def setBounceAcceleration(self, bounce_acceleration):
        self.bounce_acceleration = bounce_acceleration

    def setPlayerColors(self,color1,color2):
        self.color1=color1
        self.color2=color2

        self.paddle1=Paddle(self.screen_dimen, self.paddle_dimen, self.score_margin, self.color1)
        self.paddle2=Paddle(self.screen_dimen, self.paddle_dimen, self.score_margin, self.color2)

    def getWinnerColor(self):
        return self.winnerColor
    
    def getWinnerName(self):
        return self.winnerName

    def getLoserName(self):
        return self.loserName
    
    def getScores(self):
        return (self.score1,self.score2)

    def getFinalScores(self):
        return self.winnerScore, self.loserScore

    def getGameState(self):
        new_state2=[None for i in range(12)]
        new_state2[IND_BVELX]=self.ball.getXSpeed()/self.screen_dimen[0]
        new_state2[IND_BVELY]=self.ball.getYSpeed()/self.screen_dimen[1]
        new_state2[IND_BVELXP]=(-new_state2[IND_BVELX])
        new_state2[IND_BVELYP]=(-new_state2[IND_BVELY])

        new_state2[IND_BPOSX]=self.ball.x/self.screen_dimen[0]
        new_state2[IND_BPOSY]=self.ball.y/self.screen_dimen[1]
        new_state2[IND_BPOSXP]=1 - new_state2[IND_BPOSX]
        new_state2[IND_BPOSYP]=1 - new_state2[IND_BPOSY]
        
        new_state2[IND_PPOSX]=self.paddle2.rect.x/self.screen_dimen[0]
        new_state2[IND_PPOSY]=self.paddle2.rect.y/self.screen_dimen[1]
        new_state2[IND_PPOSXP]=1 - new_state2[IND_PPOSX]
        new_state2[IND_PPOSYP]=1 - new_state2[IND_PPOSY]
        
        return new_state2
