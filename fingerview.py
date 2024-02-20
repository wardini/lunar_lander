# Finger view control
# Allow two finger control
# of the display to include
# 1. Change view center
# 2. Zoom
# 3. Rotate View
import pygame
import numpy as np

class FingerView():
    def __init__(self,rect):
        self.grab_rect = pygame.Rect(*rect)
        self.release_rect = pygame.Rect(rect[0]-10,rect[1]-10,rect[2]+20,rect[3]+20)

        self.mouse_start_pos = np.array([0,0])
        self.mouse_control = False

        self.finger_start_pos = np.array([0,0])
        self.binding_finger_id = None

        self.dxy=0
        self.dang=0
        self.dzoom=0

        self.last_pos = np.array([0,0])
        self.scr_width, self.scr_height = pygame.display.get_window_size()

    def update(self):
        pass

    def use_deltas(self):
        self.dxy=0
        self.dang=0
        self.dzoom=0

    def events(self,event):
        self.change = False

        if self.mouse_control:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP and not event.touch:
                self.mouse_control = False
            elif not self.release_rect.collidepoint(pos):
                self.mouse_control = False
            else:
                self.change = True
                self.dxy = np.array(pos) - self.mouse_start_pos
                self.mouse_start_pos = np.array(pos)

        if event.type == pygame.MOUSEBUTTONDOWN and not event.touch:
            pos = pygame.mouse.get_pos()
            if self.grab_rect.collidepoint(pos):
                self.mouse_control = True
                self.mouse_start_pos = np.array(pos)
        elif event.type == pygame.MOUSEWHEEL and not event.touch:
            self.last_pos = pygame.mouse.get_pos()
            self.change = True
            self.dzoom += event.y

        elif event.type == pygame.FINGERDOWN:
            pos = event.x*self.scr_width , event.y*self.scr_height
            if self.grab_rect.collidepoint(pos):
                self.binding_finger_id = event.finger_id
                self.finger_start_pos = np.array(pos)
        elif event.type == pygame.FINGERUP:
            if event.finger_id == self.binding_finger_id:
                self.binding_finger_id = None
        elif event.type == pygame.FINGERMOTION:
            if event.finger_id == self.binding_finger_id:
                pos = event.x*self.scr_width , event.y*self.scr_height
                if not self.release_rect.collidepoint(pos):
                    self.binding_finger_id = None
                else:
                    self.change = True
                    self.dxy = np.array(pos) - self.finger_start_pos
                    self.finger_start_pos = np.array(pos)

    def draw(self,screen):
        pass
