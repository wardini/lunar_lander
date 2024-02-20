import pygame
from base import BaseState
from txt_item import Txt_item

TITLE="The computer broke. Land it yourself!"
STITLE1='Conservation of'
STITLE2='Angular Momentum'
STITLE3='Lander Simulator'

ABOUT1 = 'In the physical world objects'
ABOUT2 = 'behave under the laws of motion.'
ABOUT3 = 'An object in motion will stay'
ABOUT4 = 'in motion. And this equally'
ABOUT5 = 'applies to objects in rotation.'

ABOUT6 = 'Out of curiosity, we asked:'
ABOUT7 = 'How difficult would a game be'
ABOUT8 = 'if this law was imposed?'

ABOUT9 = 'Answer: Very!'

ABOUT10 = 'To make this game somewhat'
ABOUT11 = 'playable we added a history'
ABOUT12 = 'capability to allow "mistakes"'
ABOUT13 = 'to be erased.    Good Luck!'

class About(BaseState):
    def __init__(self,glbls):
        super(About, self).__init__(glbls)

        self.next_state = "MENU"

    def startup(self):
        super(About,self).startup()
        self.texts = [
            Txt_item(TITLE,(10,40),False,None,fontsize=22),
            Txt_item(STITLE1,(100,100),False,None),
            Txt_item(STITLE2,(83,135),False,None),
            Txt_item(STITLE3,(90,170),False,None),
            Txt_item("Menu",(165,705),True,'MENU'),
            Txt_item(ABOUT1,(15,230),False,None),
            Txt_item(ABOUT2,(15,260),False,None),
            Txt_item(ABOUT3,(15,290),False,None),
            Txt_item(ABOUT4,(15,320),False,None),
            Txt_item(ABOUT5,(15,350),False,None),
            Txt_item(ABOUT6,(15,400),False,None),
            Txt_item(ABOUT7,(15,430),False,None),
            Txt_item(ABOUT8,(15,460),False,None),
            Txt_item(ABOUT9,(100,505),False,None),
            Txt_item(ABOUT10,(15,550),False,None),
            Txt_item(ABOUT11,(15,580),False,None),
            Txt_item(ABOUT12,(15,610),False,None),
            Txt_item(ABOUT13,(15,640),False,None),
        ]

    def get_event(self, event):

        if event.type == pygame.QUIT:
            self.done = True
            self.quit = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for t in self.texts:
                    if t.check_select(event.pos):
                        if t.action == 'MENU':
                            self.done = True

    def draw(self, window):
        window.fill(pygame.Color("black"))

        for t in self.texts:
            t.render_text(window)
