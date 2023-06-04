import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen_dimen, paddle_dimen, score_margin, color):
        
        super().__init__()
        
        self.image = pygame.Surface([paddle_dimen[0],paddle_dimen[1]])
        self.image.fill(color)
        self.screen_dimen=screen_dimen
        self.paddle_dimen=paddle_dimen
        self.score_margin=score_margin

        self.rect = self.image.get_rect()

    def moveUp(self,pixels):
        self.rect.y -= pixels

        if self.rect.y < self.score_margin + 3:
            self.rect.y = self.score_margin + 3

    def moveDown(self,pixels):
        self.rect.y += pixels

        if self.rect.y > self.screen_dimen[1] - self.paddle_dimen[1] - 4:
            self.rect.y = self.screen_dimen[1] - self.paddle_dimen[1] - 4
