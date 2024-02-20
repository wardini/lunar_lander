# a simple button
import pygame

class Button():
    def __init__(self,rect,img1,img2,start,kbd):
        self.change = False
        self.scr_width, self.scr_height = pygame.display.get_window_size()
        self.grab_rect = pygame.Rect(*rect)
        self.state = start
        self.img1 = img1
        self.img2 = img2
        self.kbd = kbd

    def update(self):
        pass

    def events(self,event):
        self.change = False
        if event.type == pygame.FINGERDOWN:
            pos = event.x*self.scr_width , event.y*self.scr_height
            if self.grab_rect.collidepoint(pos):
                self.change = True
                self.state = not self.state

        elif event.type == pygame.KEYDOWN:
            if event.key == self.kbd:
                self.change = True
                self.state = not self.state

        elif event.type == pygame.MOUSEBUTTONDOWN and not event.touch:
            pos = pygame.mouse.get_pos()
            if self.grab_rect.collidepoint(pos):
                self.change = True
                self.state = not self.state

    def draw(self,screen):
        if not self.state:
            screen.blit(self.img1,self.grab_rect)
        else:
            screen.blit(self.img2,self.grab_rect)
