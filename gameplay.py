import pygame
from base import BaseState
from txt_item import Txt_item
from slider import Touch_Slider
from button import Button
from fingerview import FingerView
from level import Level
from lander import Lander
from popup import PopUp
import ast
import numpy as np
from pipnumpy import pip_rtnp as pip_rtnp


# LIst of valid states
#   game
#   paused
#   playback
#   crashed
#   finishing
#   crashing
#   rewrite

# Going to try to get this to simplify everything
# game
# crashing
# finishing
# 
# for each of those three states we add a pause state
#
# three more states are the following
# and when enacted they auto force pause enabled
# finished
# crashed
# rewrite
#
# playback is not really a state.
# because if the history slider current value is less than the max value
# then history is loaded instead of generated

class GamePlay(BaseState):
    def __init__(self,glbls):
        super(GamePlay,self).__init__(glbls)

        # load all level information
        self.levels=[]
        with open('levels.txt','r') as f:
            lines = f.readlines()

        Nparams=9
        self.startxy = []
        self.startvxy = []
        self.startangle = []
        for i in range(len(lines)//Nparams):
            name = lines[i*Nparams]
            polys = ast.literal_eval(lines[i*Nparams+1])
            Ms = ast.literal_eval(lines[i*Nparams+2])
            CMs = ast.literal_eval(lines[i*Nparams+3])
            Av = float(lines[i*Nparams+4])
            Lz = ast.literal_eval(lines[i*Nparams+5])
            self.startxy.append(np.array(ast.literal_eval(lines[i*Nparams+6])))
            self.startvxy.append(np.array(ast.literal_eval(lines[i*Nparams+7])))
            self.startangle.append(ast.literal_eval(lines[i*Nparams+8]))
            self.levels.append(Level(name.strip(':\n'),polys,Ms,CMs,Av,Lz))

        # load lander class
        self.lander = Lander()
        self.engine_sound = pygame.mixer.Sound("engine_sound.ogg")
        self.engine_sound.set_volume(0)
        self.engine_sound.play(-1)
        self.crash_sound = pygame.mixer.Sound("Explosion.ogg")
        self.crash_sound.set_volume(1)
        self.finish_sound = pygame.mixer.Sound("tada.ogg")
        self.finish_sound.set_volume(0.1)


        # popup definition
        msg_rect = (50,500,300,200)
        self.popups = {}
        self.popups['finishing'] = PopUp([('Congratulations',40,10,20)],msg_rect, \
                [('Main menu',85,90,True,pygame.K_RETURN),('Watch Replay',80,150,False,pygame.K_BACKSPACE)])
        self.popups['crashed'] = PopUp([('You Crashed!',40,40,60)],msg_rect, \
                [('Main menu',30,160,True,pygame.K_RETURN),('Fix it',180,160,False,pygame.K_BACKSPACE)])
        self.popups['rewrite'] = PopUp([('This will rewrite history!',25,25,10),('Continue?',55,35,55)],msg_rect, \
                [('Yes',35,150,True,pygame.K_RETURN),('No',235,150,False,pygame.K_ESCAPE)])

        # controls initialation
        self.controls = {}
        self.controls['thrust'] = Touch_Slider((200,700),'up',200,0,100,[pygame.K_UP,pygame.K_w],[pygame.K_DOWN,pygame.K_s],0)
        self.controls['Athrust'] = Touch_Slider((50,750),'right',300,-50,50,[pygame.K_RIGHT,pygame.K_d],[pygame.K_LEFT,pygame.K_a],0)
        self.controls['history'] = Touch_Slider((55,475),'right',300,0,0,[pygame.K_RIGHTBRACKET],[pygame.K_LEFTBRACKET],0)
        pausebtn = pygame.image.load("pause.png").convert()
        playbtn =  pygame.image.load("play.png").convert()
        self.controls['pause'] = Button((15,465,25,25),pausebtn,playbtn,False,pygame.K_SPACE)
        cutbtn =  pygame.image.load("cut.png").convert()
        self.controls['cut'] = Button((367,461,32,32),cutbtn,cutbtn,False,pygame.K_BACKSLASH)
        exitbtn =  pygame.image.load("exit.png").convert()
        self.controls['exit'] = Button((0,0,25,25),exitbtn,exitbtn,False,pygame.K_q)
        self.controls['zoom'] = Touch_Slider((350,620),'up',100,1,6,[pygame.K_PERIOD],[pygame.K_COMMA],4)
        self.controls['fz'] = FingerView((25,25,350,425))
        auto_btn = pygame.image.load("view_auto.png").convert()
        manual_btn =  pygame.image.load("view_manual.png").convert()
        self.controls['vmode'] = Button((338,650,25,25),manual_btn,auto_btn,True,pygame.K_v)
        helpbtn =  pygame.image.load("help_btn.png").convert()
        self.controls['help'] = Button((200,0,60,25),helpbtn,helpbtn,False,pygame.K_h)

        # help text item definitions
        self.help_items={}
        self.help_items['history'] = Txt_item('History Selector ([ ])',(130,445),False,None,fontsize=18)
        self.help_items['pause'] = Txt_item('Pause (space)',(0,445),False,None,fontsize=18)
        self.help_items['chist1'] = Txt_item('Change (\)',(320,425),False,None,fontsize=18)
        self.help_items['chist2'] = Txt_item('History',(325,445),False,None,fontsize=18)
        self.help_items['thrust1'] = Txt_item('Main',(210,505),False,None,fontsize=18)
        self.help_items['thrust2'] = Txt_item('Thrust',(210,525),False,None,fontsize=18)
        self.help_items['thrust3'] = Txt_item('(up down)',(210,545),False,None,fontsize=18)
        self.help_items['zoom1'] = Txt_item('Zoom',(290,565),False,None,fontsize=18)
        self.help_items['zoom2'] = Txt_item('(< >)',(290,585),False,None,fontsize=18)
        self.help_items['view1'] = Txt_item('View',(290,655),False,None,fontsize=18)
        self.help_items['view2'] = Txt_item('Mode (V)',(290,675),False,None,fontsize=18)
        self.help_items['fuel'] = Txt_item('Fuel',(25,655),False,None,fontsize=18)
        self.help_items['v1'] = Txt_item('Velocity',(90,655),False,None,fontsize=18)
        self.help_items['v2'] = Txt_item('relative to',(87,675),False,None,fontsize=18)
        self.help_items['v3'] = Txt_item('landing zone',(84,695),False,None,fontsize=18)
        self.help_items['rot'] = Txt_item('Rotate Thrusters (left right)',(100,760),False,None,fontsize=18)
        self.help_items['fz1'] = Txt_item('Swipe to',(300,100),False,None,fontsize=18)
        self.help_items['fz2'] = Txt_item('adjust view',(300,120),False,None,fontsize=18)

        self.levnum = 0
        self.lev_time = 0
        self.history =[]
        self.state = 'game'
        self.doneframe = (0,'game')

        # Auto View Trigger Bounderies
        self.av_recenter = np.array([(100,100),(300,100),(300,300),(100,300)])
        self.av_edge = np.array([(25,25),(375,25),(375,450),(25,450)])
        self.scaledict = {1:0.25,2:0.35,3:0.6,4:1.0,5:1.8,6:3.2}

    def startup(self):
        super(GamePlay,self).startup()

        self.levnum = self.glbls['Current Level']

        # reset lander to start position for the current level
        self.lander.startup()
        self.lander.xy = np.copy(self.startxy[self.levnum])
        self.lander.vxy = np.copy(self.startvxy[self.levnum])
        self.lander.angle = np.copy(self.startangle[self.levnum])
        self.lander.vangle=0.

        self.levels[self.levnum].reset()

        self.view_offset = (self.lander.xy + self.levels[self.levnum].Lz[0]) / 2.0 + np.array([200,300])
        self.controls['thrust'].cur_value=0
        self.controls['Athrust'].cur_value=0

        self.state = 'game'

        self.crash_time=0
        self.lev_time = 0

        self.history = [((np.copy(self.lander.xy),np.copy(self.lander.vxy),np.copy(self.lander.angle), \
                             np.copy(self.lander.vangle),np.copy(self.lander.fuel),                    \
                             np.copy(self.controls['thrust'].cur_value),                               \
                             np.copy(self.controls['Athrust'].cur_value),                              \
                             np.copy(self.levels[self.levnum].angle)))]
        self.controls['history'].vmax = 0
        self.controls['history'].cur_value = 0
        self.get_history()
        self.controls['pause'].state = False
        self.controls['vmode'].state = True
        self.doneframe = (0,'game')
        self.controls['fz'].cur_value = 4
        self.view_angle = self.lander.angle
        self.controls['zoom'].cur_value = 4
        self.engine_sound.set_volume(0)


    def get_history(self):
        cur_frame = self.controls['history'].cur_value
        self.lander.xy = np.copy(self.history[cur_frame][0])
        self.lander.vxy = np.copy(self.history[cur_frame][1])
        self.lander.angle = np.copy(self.history[cur_frame][2])
        self.lander.vangle = np.copy(self.history[cur_frame][3])
        self.lander.fuel = np.copy(self.history[cur_frame][4])
        self.lander.update_rot_matrix()
        self.controls['thrust'].cur_value = np.copy(self.history[cur_frame][5])
        self.controls['Athrust'].cur_value = np.copy(self.history[cur_frame][6])
        self.levels[self.levnum].angle = np.copy(self.history[cur_frame][7])

        self.levels[self.levnum].update(0)

    def do_finish(self):
        deltav = np.linalg.norm(self.lander.vxy - self.levels[self.levnum].Lz_velocity)
        self.controls['thrust'].cur_value = 0
        self.controls['Athrust'].cur_value = 0
        self.controls['thrust'].mouse_control = False
        self.controls['Athrust'].mouse_control = False
        self.state = 'finishing'
        self.doneframe = (len(self.history),'finishing')
        sfuel = round(self.lander.fuel,1)
        stime = round(len(self.history)/100,1)
        svel = round(deltav,1)
        score = round(sfuel-stime-svel,1)
        if self.glbls['scores'][f'Level_{self.levnum+1}'] == None:
            self.glbls['scores'][f'Level_{self.levnum+1}'] = f'{str(sfuel):5s}   -   {str(stime):4s}  -  {str(svel):4s}   =   {score}'
            self.glbls['STATES']['LOADSCORES'].save_scores_and_version()
            self.finish_sound.play(0)
        else:
            old_score = float(self.glbls['scores'][f'Level_{self.levnum+1}'].split('=')[1])
            if score > old_score:
                self.glbls['scores'][f'Level_{self.levnum+1}'] = f'{str(sfuel):5s}   -   {str(stime):4s}  -  {str(svel):4s}   =   {score}'
                self.glbls['STATES']['LOADSCORES'].save_scores_and_version()
                self.finish_sound.play(0)

    def update(self,dt):

        self.lev_time += 1

        if self.state == 'rewrite':
            return

        # for keyboard down key control
        for sk in self.controls.keys():
            self.controls[sk].update()
        if self.controls['thrust'].change or self.controls['Athrust'].change:
            if self.controls['history'].cur_value != len(self.history)-1:
                self.state = 'rewrite'
                self.controls['pause'].state = True
                self.controls['thrust'].keyboard_control = False
                self.controls['Athrust'].keyboard_control = False

        if self.state == 'finishing':
            if not self.controls['pause'].state:
                return
        elif self.state in ['crashing','crashed']:
            if not self.controls['pause'].state:
                self.lander.update(np.array([0,0]),0,0.03,0,0)
                if self.lev_time > 100+self.crash_time:
                    self.state = 'crashed'
        elif self.controls['history'].cur_value != len(self.history)-1:
            self.get_history()
            if not self.controls['pause'].state:
                self.controls['history'].cur_value += 1
                v = self.controls['thrust'].cur_value + abs(self.controls['Athrust'].cur_value)
                self.engine_sound.set_volume(v/150)
            else:
                self.engine_sound.set_volume(0)
        elif self.controls['pause'].state:
            self.engine_sound.set_volume(0)
            return
        elif self.state == 'game' and self.doneframe[0] == 0:
            v = self.controls['thrust'].cur_value + abs(self.controls['Athrust'].cur_value)
            self.engine_sound.set_volume(v/150)
            # compute lander acceleration toward level CMs
            Axy = np.array([0.,0.])
            for i in range(self.levels[self.levnum].Ms.shape[0]):
                dxy = self.levels[self.levnum].CMs[i] - self.lander.xy 
                f = 6.6E-11*self.levels[self.levnum].Ms[i] / (dxy**2).sum()
                Axy += f*dxy / np.linalg.norm(dxy)

            #print(dxy,f,Axy)

            f = float(self.lander.fuel > 0)

            # compute lander acceleration due to thrust
            Axy += 5*f*self.controls['thrust'].cur_value * \
                    np.array([-np.sin(self.lander.angle),np.cos(self.lander.angle)]) /  \
                    (self.lander.mass + self.lander.fuel)

            self.levels[self.levnum].update(0.03)

            self.lander.update(Axy,-1*f*self.controls['Athrust'].cur_value / \
                    (self.lander.mass+self.lander.fuel),0.03,        \
                    self.controls['thrust'].cur_value,self.controls['Athrust'].cur_value)

            # waypoint success detection
            if self.levels[self.levnum].Lz.shape[0] == 4:
                if pip_rtnp(self.lander.hull[:,0],self.lander.hull[:,1],self.levels[self.levnum].Lz,anyall='all'):
                    self.engine_sound.set_volume(0)
                    self.do_finish()

            # collision detection
            # get all the outside points of the lander
            # and see if they are instide any of the level polygons.
            # see if the hull points (implemented for the lander)
            # are in any of the level polygons.  Use the epmi4c point in poly code
            for s in self.levels[self.levnum].shapes:
                if pip_rtnp(self.lander.hull[:,0],self.lander.hull[:,1],s):
                    self.engine_sound.set_volume(0)
                    print('collision')

                    # check if landing is good
                    if pip_rtnp(self.lander.landpoints[:,0],self.lander.landpoints[:,1], \
                            self.levels[self.levnum].safe_Lz,anyall='all'):
                        print('in safe landing area')

                        #if #velocities match
                        # compare velocity vectors for ship and landing zone
                        deltav = np.linalg.norm(self.lander.vxy - self.levels[self.levnum].Lz_velocity)
                        print('deltav',deltav)

                        if deltav < 4.0:
                            self.do_finish()
                        else:
                            self.crash_time = self.lev_time
                            self.state = 'crashing'
                            self.lander.start_crash()
                            self.doneframe = (len(self.history),'crashing')
                            self.crash_sound.play(0)
                    else:
                        self.crash_time = self.lev_time
                        self.state = 'crashing'
                        self.lander.start_crash()
                        self.doneframe = (len(self.history),'crashing')
                        self.crash_sound.play(0)

            self.history.append((np.copy(self.lander.xy),np.copy(self.lander.vxy),np.copy(self.lander.angle), \
                                 np.copy(self.lander.vangle),np.copy(self.lander.fuel),                       \
                                 np.copy(self.controls['thrust'].cur_value),                                  \
                                 np.copy(self.controls['Athrust'].cur_value),                                 \
                                 np.copy(self.levels[self.levnum].angle)))
            self.controls['history'].vmax = len(self.history)-1
            self.controls['history'].cur_value = len(self.history)-1

        elif self.state == 'game':
            self.state = self.doneframe[1]
            if self.state == 'crashing':
                self.lander.state = 'crashing'
                self.crash_time = self.lev_time
                self.engine_sound.set_volume(0)
            elif self.state == 'finishing':
                self.engine_sound.set_volume(0)
        else:
            print('should not be here')

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.done = True
            self.quit = True

        if self.state == 'finishing':
            r = self.popups['finishing'].events(event)
            if r == True:
                self.next_state = "MENU"
                self.done = True
            elif r == False:
                self.controls['history'].cur_value = 0
                self.state = 'game'
        elif self.state == 'crashed':
            r = self.popups['crashed'].events(event)
            if r == True:
                self.next_state = "MENU"
                self.done = True
            elif r == False:
                self.controls['history'].cur_value = int(0.9*len(self.history))
                self.get_history()
                self.controls['pause'].state = True
                self.lander.state='flying'
                self.engine_sound.set_volume(0)
                self.state = 'game'
        elif self.state == 'rewrite':
            r = self.popups['rewrite'].events(event)
            if r == True:
                # erase remaining history
                self.history = self.history[0:self.controls['history'].cur_value+1]
                self.controls['history'].vmax = len(self.history)-1
                self.controls['history'].cur_value = len(self.history)-1
                self.controls['pause'].state = True
                self.state = 'game'
                self.doneframe = (0,'game')
            elif r == False:
                self.controls['pause'].state = True
                self.state = 'game'

        else:
            for sk in self.controls.keys():
                self.controls[sk].events(event)

            if self.controls['exit'].change:
                self.done = True
                self.next_state = "MENU"
                self.engine_sound.set_volume(0)

            if self.controls['history'].change:
                self.controls['pause'].state = True
                self.engine_sound.set_volume(0)
                self.get_history()
                if self.controls['history'].cur_value != len(self.history)-1:
                    self.lander.state='flying'
                    self.state = 'game'
                else:
                    if self.doneframe[0] != 0:
                        self.state = self.doneframe[1]
                        if self.state == 'crashing':
                            self.lander.state='crashing'

            if self.controls['thrust'].change or self.controls['Athrust'].change or self.controls['cut'].change:
                if self.controls['history'].cur_value != len(self.history)-1:
                    self.controls['pause'].state = True
                    self.state = 'rewrite'
                    self.controls['thrust'].mouse_control = False
                    self.controls['thrust'].keyboard_control = False
                    self.controls['Athrust'].mouse_control = False
                    self.controls['Athrust'].keyboard_control = False

                # sounds
                if self.controls['pause'].state == False:
                    v = self.controls['thrust'].cur_value + abs(self.controls['Athrust'].cur_value)
                    self.engine_sound.set_volume(v/150)

            if self.controls['fz'].change:
                if self.controls['fz'].dzoom:
                    curscale = self.scaledict[self.controls['zoom'].cur_value]
                    self.controls['zoom'].cur_value += self.controls['fz'].dzoom
                    self.controls['zoom'].cur_value = min(self.controls['zoom'].cur_value,self.controls['zoom'].vmax)
                    self.controls['zoom'].cur_value = max(self.controls['zoom'].cur_value,self.controls['zoom'].vmin)
                    newscale = self.scaledict[self.controls['zoom'].cur_value]
                    if curscale != newscale:
                        pos = self.controls['fz'].last_pos
                        self.view_offset = pos - (newscale/curscale) * (pos - self.view_offset)
                else:
                    self.view_offset += self.controls['fz'].dxy
                self.controls['fz'].use_deltas()

    def draw(self, screen):
        screen.fill(pygame.Color("black"))

        # compute the desired scale for the view

        # put the lander in the center of the view ??
        # then compute the landing pad and put it x% from the bottom of the screen
        # that distance is in pixels which is a constant so we know pixels / meters
        #s = 80 / ((self.lander.xy - self.levels[self.levnum].Lz.mean(axis=0))**2).sum()**0.5
        #s=-0.5+0.75*self.controls['zoom'].cur_value
        s=self.scaledict[self.controls['zoom'].cur_value]
        scale = np.array([s,-s])


        # need to compute a camera location based on something
        # that location is subtracted from each element
        # before the scaling or offset operation

        #offset = np.array([200,400])
        if self.controls['vmode'].state == False:
            #final_rotation = self.lander.angle
            #final_offset = self.lander.xy + np.array([200,300])
            final_rotation = 0
            final_offset = 0
            #self.view_offset = np.array([200,200]) - scale * self.lander.xy 
        else:
            final_rotation = 0
            final_offset = 0

            # This is auto view mode which updates based on lander and lz position on screen
            # 1. if mid point is far from the center, recenter
            # 2. if mid point is near the center then zoom out 1

            # if lz and lander are both close together relative to the screen size regardless
            # of being close to the edge
            # 1. recenter
            # 2. zoom in 1

            lander_loc = self.lander.xy*scale+self.view_offset
            lz_loc = np.mean(self.levels[self.levnum].Lz,axis=0)*scale+self.view_offset
            pts = np.array([lander_loc,lz_loc])
            midpoint = (lander_loc+lz_loc) / 2.0

            if not pip_rtnp(np.array([midpoint[0]]),np.array([midpoint[1]]),self.av_recenter):
                self.view_offset += np.array([200,200]) - midpoint
            elif not pip_rtnp(pts[:,0],pts[:,1],self.av_edge,anyall='all'):
                self.controls['zoom'].cur_value -= 1
                self.controls['zoom'].cur_value = max(self.controls['zoom'].cur_value,self.controls['zoom'].vmin)
            elif np.linalg.norm(lander_loc - lz_loc) < 40 and self.controls['zoom'].cur_value < 5:
                self.controls['zoom'].cur_value += 1
                self.controls['zoom'].cur_value = min(self.controls['zoom'].cur_value,self.controls['zoom'].vmax)


        self.levels[self.levnum].draw(scale,self.view_offset,final_rotation,screen)
        self.lander.draw(self.controls['thrust'].cur_value,-self.controls['Athrust'].cur_value, \
                scale,self.view_offset,final_offset,screen)
        for sk in self.controls.keys():
            self.controls[sk].draw(screen)

        # relative velocity Indicator
        v_metric = -self.lander.vxy + self.levels[self.levnum].Lz_velocity
        v_mag = np.linalg.norm(v_metric)
        if v_mag > 10:
            v_metric *= 10.0/v_mag

        if v_mag < 4:
            icol='green'
        else:
            icol='red'
        pygame.draw.line(screen,pygame.Color(icol),(120,620),(120-4*v_metric[0],620+4*v_metric[1]),width=5)
        pygame.draw.circle(screen,pygame.Color(icol),(120,620),40,width=2)

        # Fuel Guage
        if self.lander.fuel > 50:
            fcol='green'
        elif self.lander.fuel > 10:
            fcol='orange'
        else:
            fcol='red'
        pygame.draw.line(screen,pygame.Color(fcol),(40,660),(40,660-self.lander.fuel),width=5)

        # Help Items
        if self.controls['help'].state:
            for t in self.help_items.keys():
                self.help_items[t].render_text(screen)

        if self.state == 'finishing':
            self.popups['finishing'].draw(screen)
        elif self.state == 'crashed':
            self.popups['crashed'].draw(screen)
        elif self.state == 'rewrite':
            self.popups['rewrite'].draw(screen)

