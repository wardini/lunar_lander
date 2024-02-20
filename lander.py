import ast
import numpy as np
import pygame

class Body():
    def __init__(self,points):
        self.points=np.array(points)

    def draw(self,angle,location,scale,offset,screen):
        p = (angle @ self.points.T).T
        p = (p + location) * scale + offset
        pygame.draw.polygon(screen,pygame.Color('white'),p,width=1)

class Strut():
    def __init__(self,points):
        self.points=np.array(points)

    def draw(self,angle,location,scale,offset,screen):
        p = (angle @ self.points.T).T
        p = (p + location) * scale + offset
        pygame.draw.line(screen,pygame.Color('white'),*p,width=1)

class Engine():
    def __init__(self,points,posneg=True):
        self.points=np.array(points)
        self.thrust_poly=np.array([self.points[1],self.points[2]])
        self.thrust_base = (self.points[1]+self.points[2])/2.0
        self.thrust_vector = 0.07*(self.thrust_base - self.points[0])
        self.thrust = 0.0
        self.posneg= 1. if posneg else -1.

    def draw(self,angle,location,scale,thrust,offset,screen):

        if self.posneg * thrust > 0.0:
            tpoly = np.vstack((self.thrust_poly, \
                self.thrust_base+self.posneg*thrust*self.thrust_vector))
            p = (angle @ tpoly.T).T
            p = (p + location) * scale + offset
            pygame.draw.polygon(screen,pygame.Color('red'),p,width=0)

        p = (angle @ self.points.T).T
        p = (p + location) * scale + offset
        pygame.draw.polygon(screen,pygame.Color('white'),p,width=1)

def rtm(a):
    return(np.array([[np.cos(a),-np.sin(a)], [np.sin(a), np.cos(a)]]))

class Lander():
    def __init__(self):
        self.bodys=[]
        self.struts=[]
        self.engineLR=[]
        self.engineD=[]
        self.lp_start=np.array([])

        with open('lander.txt', 'r') as f:
            shapelist = ast.literal_eval(''.join(f.readlines()))

        for s in shapelist:
            if s[0] == 'body':
                self.bodys.append(Body(s[1]))
            elif s[0] == 'strut':
                self.struts.append(Strut(s[1]))
            elif s[0] == 'engineL':
                self.engineLR.append(Engine(s[1],posneg=True))
            elif s[0] == 'engineR':
                self.engineLR.append(Engine(s[1],posneg=False))
            elif s[0] == 'engineD':
                self.engineD.append(Engine(s[1],posneg=True))
            elif s[0] == 'pad':
                self.struts.append(Strut(s[1]))
                if self.lp_start.shape[0]==0:
                    self.lp_start=np.array(s[1][0])
                else:
                    self.lp_start = np.vstack((self.lp_start,np.array(s[1][0])))
            elif s[0] == 'hull':
                self.hull_start = np.array(s[1])

        self.xy = np.array([0.,0.])
        self.vxy = np.array([0.,0.])
        self.angle = 0.
        self.vangle = 0.
        self.fuel = 80.0
        self.mass = 30
        self.hull = self.hull_start
        self.landpoints = self.lp_start
        self.state = 'flying'

    def startup(self):
        self.state = 'flying'
        self.fuel = 80.0

    def update_rot_matrix(self):
        self.rot_matrix = rtm(self.angle)
        self.hull = (self.rot_matrix @ self.hull_start.T).T + self.xy
        self.landpoints = (self.rot_matrix @ self.lp_start.T).T + self.xy

    def update(self,Axy,angA,dt,thrust,Athrust):
        if self.state == 'flying':
            self.xy = self.xy + self.vxy*dt
            self.vxy += Axy * dt
            self.angle += (self.vangle * dt) % (2*np.pi)
            self.vangle += angA * dt / 5
            self.update_rot_matrix()
            self.fuel = max(self.fuel - thrust/2000 - Athrust/8000,0)
        elif self.state == 'crashing':
            for i in range(len(self.crash_vangle_list)):
                self.crash_angle_list[i] += self.crash_vangle_list[i]*dt
                self.crash_xy_list[i]    += self.crash_vxy_list[i]*dt

    def draw(self,thrust,Athrust,scale,offset,final_offset,window):
        if self.state == 'flying':

            drawthrust = thrust*(self.fuel > 0)
            drawAthrust = Athrust*(self.fuel > 0)

            for b in self.bodys:
                b.draw(self.rot_matrix,self.xy,scale,offset,window)
            for s in self.struts:
                s.draw(self.rot_matrix,self.xy,scale,offset,window)
            for e in self.engineLR:
                e.draw(self.rot_matrix,self.xy,scale,drawAthrust,offset,window)
            for e in self.engineD:
                e.draw(self.rot_matrix,self.xy,scale,drawthrust,offset,window)
        elif self.state == 'crashing':
            i = 0
            for b in self.bodys:
                b.draw(rtm(self.crash_angle_list[i]),self.crash_xy_list[i],scale,offset,window)
                i += 1
            for s in self.struts:
                s.draw(rtm(self.crash_angle_list[i]),self.crash_xy_list[i],scale,offset,window)
                i += 1
            for e in self.engineLR:
                e.draw(rtm(self.crash_angle_list[i]),self.crash_xy_list[i],scale,0,offset,window)
                i += 1
            for e in self.engineD:
                e.draw(rtm(self.crash_angle_list[i]),self.crash_xy_list[i],scale,0,offset,window)
                i += 1

    def start_crash(self):
        self.state = 'crashing'

        self.crash_vangle_list=[]
        self.crash_angle_list=[]
        self.crash_vxy_list=[]
        self.crash_xy_list=[]

        for b in self.bodys:
            self.crash_vangle_list.append(np.random.random(1)[0]*2-1)
            self.crash_angle_list.append(np.copy(self.angle))
            rand_ang = (110 + 140*np.random.random(1)[0])*np.pi/180
            self.crash_vxy_list.append((rtm(rand_ang) @ self.vxy.T).T)
            self.crash_xy_list.append(np.copy(self.xy))
        for s in self.struts:
            self.crash_vangle_list.append(np.random.random(1)[0]*2-1)
            self.crash_angle_list.append(np.copy(self.angle))
            rand_ang = (110 + 140*np.random.random(1)[0])*np.pi/180
            self.crash_vxy_list.append((rtm(rand_ang) @ self.vxy.T).T)
            self.crash_xy_list.append(np.copy(self.xy))
        for e in self.engineLR:
            self.crash_vangle_list.append(np.random.random(1)[0]*2-1)
            self.crash_angle_list.append(np.copy(self.angle))
            rand_ang = (110 + 140*np.random.random(1)[0])*np.pi/180
            self.crash_vxy_list.append((rtm(rand_ang) @ self.vxy.T).T)
            self.crash_xy_list.append(np.copy(self.xy))
        for e in self.engineD:
            self.crash_vangle_list.append(np.random.random(1)[0]*2-1)
            self.crash_angle_list.append(np.copy(self.angle))
            rand_ang = (110 + 140*np.random.random(1)[0])*np.pi/180
            self.crash_vxy_list.append((rtm(rand_ang) @ self.vxy.T).T)
            self.crash_xy_list.append(np.copy(self.xy))

if __name__ == '__main__':
    import pygame
    pygame.init()
    with open('constants.txt','r') as f:
        lines = f.readlines()
    glbls = ast.literal_eval(''.join(lines))
    window = pygame.display.set_mode((glbls['WIDTH'], glbls['HEIGHT']))
    clock = pygame.time.Clock()
    pygame.display.set_caption(f"lander class test")
    lander = Lander()
    done = False
    thrust = 0.
    Athrust = 0.
    angA = 0.

    scale = np.array([5,-5])
    offset = np.array([200,400])

    while not done:
        dt = clock.tick(30) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True
                elif event.key == pygame.K_RIGHT:
                    Athrust -= 1.0
                elif event.key == pygame.K_LEFT:
                    Athrust += 1.0
                elif event.key == pygame.K_UP:
                    thrust += 2.
                elif event.key == pygame.K_DOWN:
                    thrust = max(thrust - 2.,0.)

        # compute accelerations
        Axy = np.array([0.,-1.])
        Axy = Axy + np.array([0,thrust])

        lander.update(Axy,Athrust/(lander.mass+lander.fuel),dt)

        window.fill(pygame.Color("black"))
        lander.draw(thrust,Athrust,scale,offset,window)
        pygame.display.update()
