import pygame
import r

class Border(pygame.sprite.Sprite):

    def rectangle(self, screen):
        pygame.draw.line(screen, r.colors.WHITE, [0,0],[r.game.SCREEN_WIDTH,0], 9)
        pygame.draw.line(screen, r.colors.WHITE, [r.game.SCREEN_WIDTH,0],[r.game.SCREEN_WIDTH,r.game.SCREEN_HEIGHT], 9)
        pygame.draw.line(screen, r.colors.WHITE, [r.game.SCREEN_WIDTH,r.game.SCREEN_HEIGHT],[0,r.game.SCREEN_HEIGHT], 9)
        pygame.draw.line(screen, r.colors.WHITE, [0,r.game.SCREEN_HEIGHT],[0,0], 9)
