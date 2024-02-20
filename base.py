import pygame


class BaseState(object):
    def __init__(self,glbls):
        self.done = False
        self.quit = False
        self.next_state = None
        self.glbls = glbls

    def startup(self):
        pass

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, window):
        pass
