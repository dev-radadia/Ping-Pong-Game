import pygame
import random
import math

ball_color_default = (255,255,255)

class Ball(pygame.sprite.Sprite):
    def __init__(self, ball_dimen, screen_dimen, paddle_dimen, score_margin):

        super().__init__()

        self.image = pygame.Surface([ball_dimen[0] , ball_dimen[1]], pygame.SRCALPHA)
        pygame.draw.circle(self.image, ball_color_default, (ball_dimen[0]//2, ball_dimen[0]//2),ball_dimen[0]//2)

        self.rect = self.image.get_rect()

        self.speed = 0
        self.x = 0
        self.y = 0
        self.px = 0
        self.py = 0
        self.direction = 0
        self.bounce_bias = 0
        self.reset_margin = 0
        self.ball_dimen = ball_dimen
        self.screen_dimen = screen_dimen
        self.paddle_dimen = paddle_dimen
        self.score_margin = score_margin

        self.bounceSound=pygame.mixer.Sound('sound/bounce1.wav')
        self.crossedSound=pygame.mixer.Sound('sound/bounce2.wav')

        self.ballReset()

    def bounce(self,b_param):
        p_dir=self.direction
        self.direction = (180-self.direction)%360
        if not self.same_dir(p_dir,self.direction + (b_param/self.paddle_dimen[1])*self.bounce_bias):
            self.direction += (b_param/self.paddle_dimen[1])*self.bounce_bias

    def same_dir(self,dir1,dir2):
        dir1=dir1%360
        dir2=dir2%360
        r1=-1
        r2=-1

        if (dir1<=90 and dir2>=0) or (dir1>=270 and dir1<=360):
            r1=1
        if (dir2<=90 and dir2>=0) or (dir2>=270 and dir2<=360):
            r2=1

        return r1==r2

    def crossed(self,xcor):
        return (((self.x+self.px)/2-xcor)*((self.px+self.ppx)/2-self.getXSpeed()-xcor) < 0)

    def ballReset(self):
        self.speed = 4.0
        self.y = random.randrange(self.reset_margin + self.score_margin , self.screen_dimen[1] - self.reset_margin)
        self.x = self.screen_dimen[0]/2 - self.ball_dimen[0]/2 
        self.py = self.y
        self.px = self.x

        self.direction = random.randrange(-45,45)

        if random.randrange(2) == 0:
            self.direction += 180

    def update(self):        
        rads = math.radians(self.direction)

        self.ppx=self.px
        self.ppy=self.py
        self.px=self.x
        self.py=self.y
        self.x += math.cos(rads) * self.speed
        self.y -= math.sin(rads) * self.speed

        if self.x < -self.ball_dimen[0]*5 or self.x > self.screen_dimen[0] + self.ball_dimen[0]*5:
            self.crossedSound.play()
            self.ballReset()        

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if self.y <= self.score_margin:
            self.bounceSound.play()
            self.direction = (360-self.direction)%360
            self.y = 1 + self.score_margin
        if self.y >= self.screen_dimen[1] - self.ball_dimen[1]:
            self.bounceSound.play()
            self.direction = (360-self.direction)%360
            self.y = self.screen_dimen[1] - self.ball_dimen[1] - 1

    def setBounceBias(self, bias):
        self.bounce_bias = bias

    def setResetMargin(self, margin):
        self.reset_margin = margin

    def setBallSpeed(self, speed):
        self.speed = speed

    def getXSpeed(self):
        return math.cos(math.radians(self.direction)) * self.speed

    def getYSpeed(self):
        return -math.sin(math.radians(self.direction)) * self.speed