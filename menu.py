import pygame
from base import BaseState
from txt_item import Txt_item

TITLE="The computer broke. Land it yourself!"
STITLE1='Conservation of'
STITLE2='Angular Momentum'
STITLE3='Lander Simulator'

BEST = 'Best Scores'
SC1 = '    Fuel         Time   Landing'
SC2 = 'Remaining  to land  velocity        Total'


class Menu(BaseState):
    def __init__(self,glbls):
        super(Menu, self).__init__(glbls)

        self.next_state = "MENU"

        self.music=False
        self.first_music=True

    def startup(self):
        super(Menu,self).startup()
        self.texts = [
            Txt_item(TITLE,(10,40),False,None,fontsize=22),
            Txt_item(STITLE1,(100,100),False,None),
            Txt_item(STITLE2,(83,135),False,None),
            Txt_item(STITLE3,(90,170),False,None),
            Txt_item(BEST,(175,230),False,None),
            Txt_item("Music on/off",(140,670),True,'MUSIC'),
            Txt_item("Quit",(165,705),True,'QUIT'),
            Txt_item(SC1,(120,260),False,None,fontsize=16),
            Txt_item(SC2,(120,277),False,None,fontsize=16),
            Txt_item("About",(150,635),True,'ABOUT')
        ]

        N = len(self.glbls['STATES']["GAMEPLAY"].levels)
        lev_buttons = [None]*N
        for i in range(N):
            name = self.glbls['STATES']["GAMEPLAY"].levels[i].name
            self.texts.append(Txt_item(name,(30,300+35*i),True,'GAMEPLAY '+str(i),fontsize=20))
            lev_buttons[i] = self.texts[-1]

        first = True
        for i in range(N):
            scorei = str(self.glbls['scores']['Level_'+str(i+1)])
            if scorei != "None":
                #self.texts.append(Txt_item(f'{scorei:7.2f}',(250,295+35*i),False,None))
                self.texts.append(Txt_item(scorei,(135,295+35*i),False,None,fontsize=20))
            else:
                if first:
                    first = False
                    continue
                else:
                    lev_buttons[i].disable_click()

        if self.first_music:
            pygame.mixer.music.load('ObservingTheStar.ogg')
            self.music_on_off()
            self.first_music = False

        
    def music_on_off(self):
        if self.music:
            self.texts[5].change_text('Music Off')
            pygame.mixer.music.play(-1)
        else:
            self.texts[5].change_text('Music On')
            pygame.mixer.music.stop()

    def get_event(self, event):

        if event.type == pygame.QUIT:
            self.quit = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for t in self.texts:
                    if t.check_select(event.pos):
                        if t.action == 'QUIT':
                            self.quit = True
                        elif t.action == 'ABOUT':
                            self.done = True
                            self.next_state='ABOUT'
                        elif t.action == 'MUSIC':
                            self.music = not self.music
                            self.music_on_off()
                        elif 'GAMEPLAY' in t.action:
                            self.glbls['Current Level']=int(t.action.split()[1])
                            self.done = True
                            self.next_state='GAMEPLAY'

    def draw(self, window):
        window.fill(pygame.Color("black"))

        for t in self.texts:
            t.render_text(window)
