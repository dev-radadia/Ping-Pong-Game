import pygame

import r

pygame.init()

class Textbox:
    def __init__(self, x, y, width, height, fontsize=r.font_size.xxs+1, maxlength=12, text='', textcolor=r.colors.BLACK, inactivebordercolor=r.colors.SILVER, activebordercolor=r.colors.GOLD):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = inactivebordercolor
        self.inactivecolor = inactivebordercolor
        self.textcolor = textcolor
        self.activecolor = activebordercolor
        self.maxlength = maxlength
        self.text = text
        
        self.fontsize = fontsize
        self.font=pygame.font.Font(None, self.fontsize)

        self.txt_surface = self.font.render(text, True, self.color)
        self.txt_surface.set_alpha(0)

        self.active = False

        self.repeater_count={}
        self.nr_init=400
        self.nr_inter=35

        self.clock=pygame.time.Clock()

    def handle_event(self, events):
        for event in events:
            self.define_event(event)

        for k in self.repeater_count:
            self.repeater_count[k][0] += self.clock.get_time()
            if self.repeater_count[k][0] >= self.nr_init:
                self.repeater_count[k][0] = (self.nr_init - self.nr_inter)

                e_key, e_uni = k, self.repeater_count[k][1]
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=e_key, unicode=e_uni))
        
        self.text_surface = self.font.render(self.text, True, self.textcolor)
        
        self.clock.tick()

    def define_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                click = pygame.mixer.Sound('sound/click3.wav')
                click.play()
                self.active = True
                self.color = self.activecolor
            else:
                self.active = False
                self.color = self.inactivecolor

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key not in self.repeater_count:
                    self.repeater_count[event.key]=[0,event.unicode]

                if event.key == pygame.K_DELETE:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key in [pygame.K_TAB, pygame.K_ESCAPE]:
                    pass
                else:
                    if len(self.text) < self.maxlength:
                        self.text += event.unicode

            elif event.type==pygame.KEYUP:
                del self.repeater_count[event.key]

    def draw(self, screen):
        pygame.draw.line(screen, r.colors.WHITE, (self.rect.x+2,self.rect.y+self.rect.height/2), (self.rect.x+self.rect.width-2,self.rect.y+self.rect.height/2), 30)
        pygame.draw.rect(screen, self.color, self.rect, 4)
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))

    def ai_draw(self, screen):
        pygame.draw.line(screen, r.colors.WHITE, (self.rect.x+2,self.rect.y+self.rect.height/2), (self.rect.x+self.rect.width-2,self.rect.y+self.rect.height/2), 30)
        pygame.draw.rect(screen, self.color, self.rect, 4)
        self.text_surface = self.font.render(self.text, True, self.textcolor)
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))

    def getText(self):
        return self.text
