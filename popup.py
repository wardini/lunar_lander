from txt_item import Txt_item
import pygame
#import pygame.gfxdraw

# msglist = [('txt',font size,x,y)]
# txtlist = [('txt',x,y,action txt]

class PopUp():
    def __init__(self,msglist,rect,txtlist):
        self.rect = rect
        self.scr_width, self.scr_height = pygame.display.get_window_size()
        self.msgs = []
        for msg in msglist:
            self.font = pygame.font.SysFont('timesnewroman',msg[1])
            text_surface = self.font.render(msg[0], True, pygame.Color("white"))
            trect = text_surface.get_rect(topleft=(msg[2]+rect[0],msg[3]+rect[1]))
            self.msgs.append((text_surface,trect))

        self.titems = []
        for t in txtlist:
            self.titems.append((Txt_item(t[0],(t[1]+rect[0],t[2]+rect[1]),True,t[3]),t[4]))


    def events(self,event):
        if event.type == pygame.FINGERUP:
            pos = event.x*self.scr_width , event.y*self.scr_height
            for t in self.titems:
                if t[0].check_select(pos):
                    return(t[0].action)

        elif event.type == pygame.KEYDOWN:
            for t in self.titems:
                if event.key == t[1]:
                    return(t[0].action)

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for t in self.titems:
                if t[0].check_select(pos):
                    return(t[0].action)

        return(None)

    def draw(self,screen):
        pygame.draw.rect(screen, pygame.Color("black"),self.rect,0)
        for m in self.msgs:
            screen.blit(m[0],m[1])
        for t in self.titems:
            t[0].render_text(screen)
        pygame.draw.rect(screen, pygame.Color("white"),self.rect,3)
        #pygame.gfxdraw.box(screen, self.rect, (50,50,50,100))
