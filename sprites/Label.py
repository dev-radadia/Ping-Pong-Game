import pygame

class Label():
    def __init__(self,screen,limitRect,fg_color,bg_color,font,text="",lineSpacing=-2):
        self.limitRect=pygame.Rect(limitRect)
        self.screen=screen
        self.fg_color=fg_color
        self.bg_color=bg_color
        self.font=font
        self.text=text
        self.lineSpacing=lineSpacing

    def draw(self):
        fh=self.font.size("Tg")[1]
        blit_list=[]
        j=0
        temptxt=self.text
        i=1
        flag=True

        while temptxt and (len(blit_list)*(fh+self.lineSpacing)<=self.limitRect.height):
            if temptxt[0] == '\n':
                for x in range(1,len(temptxt)):
                    if temptxt[x]!='\n':
                        break
                    blit_list.append("")
                temptxt=temptxt[x:]
                continue

            i=1
            flag=True

            while self.font.size(temptxt[:i])[0] < self.limitRect.width and i < len(temptxt) and flag:
                i+=1
                if temptxt[i-1]=='\n':
                    flag=False

            if i<len(temptxt) and flag:
                i=temptxt.rfind(" ",0,i)+1

            if not flag:
                i-=1

            blit_list.append(temptxt[:i])
            temptxt=temptxt[i:]

        y=self.limitRect.top
        for st in blit_list:
            image=self.font.render(st,1,self.fg_color)
            self.screen.blit(image,(self.limitRect.left,y))
            y+=fh+self.lineSpacing
            
    def setText(self,text):
        self.text=text
