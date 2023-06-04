import pygame
from pygame.sprite import Sprite
from pygame.rect import Rect

from r.game import *

class PauseButton(Sprite):
    def __init__(self, action = None):

        pygame.init()

        self.pausebutton = pygame.image.load('image\image.png')
        
        self.pb = pygame.transform.scale(self.pausebutton, (50,50))
        
        self.mouse_over = False

        self.rect = self.pb.get_rect(center = (SCREEN_WIDTH/2, 35))
    
        self.action = action
        
        self.clickSound=pygame.mixer.Sound('sound/click3.wav')
    
        super().__init__()

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                self.clickSound.play()
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.pb, self.rect)

