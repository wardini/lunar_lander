# create a touch slider
# but also works with mouse
import pygame

class Touch_Slider():
    def __init__(self,location,direction,length,vmin,vmax,key1,key2,start):
        self.location = location
        self.direction = direction
        self.cur_value = start
        self.vmin = vmin
        self.vmax = vmax
        self.key1 = key1
        self.key2 = key2
        self.length = length
        if self.direction == 'up':
            self.slider_rect = pygame.Rect(location[0],location[1]-length,5,length)
            self.grab_rect = pygame.Rect(location[0]-10,location[1]-length-10,25,length+20)
            self.release_rect = pygame.Rect(location[0]-20,location[1]-length-30,45,length+60)
            #self.text_location = 
        elif self.direction == 'right':
            self.slider_rect = pygame.Rect(location[0],location[1],length,5)
            self.grab_rect = pygame.Rect(location[0]-10,location[1]-10,length+20,25)
            self.release_rect = pygame.Rect(location[0]-30,location[1]-20,length+60,45)

        self.change = False
        self.scr_width, self.scr_height = pygame.display.get_window_size()

        self.font = pygame.font.SysFont('timesnewroman',12)
        self.keyboard_control = False
        self.mouse_control = False
        self.binding_finger_id = None
        self.delta = 0

    def set_enabled(self,enabled):
        self.enabled = enabled

    # needed because of depressed keyboard controls
    # which we want to continue to have an action
    def update(self):
        if self.keyboard_control:
            self.change = True
            self.cur_value += self.delta
            self.cur_value = min(self.cur_value,self.vmax)
            self.cur_value = max(self.cur_value,self.vmin)
        else:
            self.change = False
        
    def events(self,event):
        self.change = False

        if self.mouse_control:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP and not event.touch:
                self.mouse_control = False
            elif self.release_rect.collidepoint(pos):
                self.change = True
                if self.direction == 'up':
                    self.cur_value = self.vmin  + (self.vmax - self.vmin)*(self.location[1] - pos[1])/self.length
                    self.cur_value = int(min(max(self.vmin,self.cur_value),self.vmax))
                elif self.direction == 'right':
                    self.cur_value = self.vmin  + (self.vmax - self.vmin)*(pos[0] - self.location[0])/self.length
                    self.cur_value = int(min(max(self.vmin,self.cur_value),self.vmax))
            else:
                self.mouse_control = False

        elif self.keyboard_control:
            if event.type == pygame.KEYUP:
                if event.key in self.key1:
                    self.keyboard_control = False
                elif event.key in self.key2:
                    self.keyboard_control = False

        if event.type == pygame.MOUSEBUTTONDOWN and not event.touch:
            pos = pygame.mouse.get_pos()
            if self.grab_rect.collidepoint(pos):
                self.change = True
                self.mouse_control = True
                if self.direction == 'up':
                    self.cur_value = self.vmin  + (self.vmax - self.vmin)*(self.location[1] - pos[1])/self.length
                    self.cur_value = int(min(max(self.vmin,self.cur_value),self.vmax))
                elif self.direction == 'right':
                    self.cur_value = self.vmin  + (self.vmax - self.vmin)*(pos[0] - self.location[0])/self.length
                    self.cur_value = int(min(max(self.vmin,self.cur_value),self.vmax))

        elif event.type == pygame.FINGERDOWN:
            pos = event.x*self.scr_width , event.y*self.scr_height
            if self.grab_rect.collidepoint(pos):
                self.change = True
                self.binding_finger_id = event.finger_id
                if self.direction == 'up':
                    self.cur_value = self.vmin  + (self.vmax - self.vmin)*(self.location[1] - pos[1])/self.length
                    self.cur_value = int(min(max(self.vmin,self.cur_value),self.vmax))
                elif self.direction == 'right':
                    self.cur_value = self.vmin  + (self.vmax - self.vmin)*(pos[0] - self.location[0])/self.length
                    self.cur_value = int(min(max(self.vmin,self.cur_value),self.vmax))
        elif event.type == pygame.FINGERUP:
            if event.finger_id == self.binding_finger_id:
                self.binding_finger_id = None
        elif event.type == pygame.FINGERMOTION:
            if event.finger_id == self.binding_finger_id:
                pos = event.x*self.scr_width , event.y*self.scr_height
                if self.release_rect.collidepoint(pos):
                    self.change = True
                    if self.direction == 'up':
                        self.cur_value = self.vmin  + (self.vmax - self.vmin)*(self.location[1] - pos[1])/self.length
                        self.cur_value = int(min(max(self.vmin,self.cur_value),self.vmax))
                    elif self.direction == 'right':
                        self.cur_value = self.vmin  + (self.vmax - self.vmin)*(pos[0] - self.location[0])/self.length
                        self.cur_value = int(min(max(self.vmin,self.cur_value),self.vmax))
                else:
                    self.binding_finger_id = None

        elif event.type == pygame.KEYDOWN:
            if event.key in self.key1:
                self.change = True
                self.keyboard_control = True
                self.delta = 1
            elif event.key in self.key2:
                self.change = True
                self.keyboard_control = True
                self.delta = -1

    def draw(self,screen):
        if self.vmax - self.vmin == 0:
            pixdelta = self.length
        else:
            pixdelta = self.length * (self.cur_value - self.vmin) / (self.vmax - self.vmin)
        text_surface = self.font.render(str(self.cur_value), True, pygame.Color("white"))
        if self.direction == 'up':
            self.handle_rect = pygame.Rect(self.location[0]-5,self.location[1]-pixdelta-3,15,6)
            textrect = text_surface.get_rect(midright=(self.location[0]-10,self.location[1]-pixdelta))
        elif self.direction == 'right':
            self.handle_rect = pygame.Rect(self.location[0]+pixdelta-3,self.location[1]-5,6,15)
            textrect = text_surface.get_rect(center=(self.location[0]+pixdelta,self.location[1]-12))
            
        pygame.draw.rect(screen, pygame.Color("white"),self.slider_rect,2)
        pygame.draw.rect(screen, pygame.Color("white"),self.handle_rect,2)

        screen.blit(text_surface,textrect)
