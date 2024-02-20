# All levels consist of a polygon representing
# the terrain.  A collection of masses and centers
# And a landing zone which is just a line I think.
# Av is the angular velocity of the polygon
import pygame
import numpy as np

# The body rotates around 0,0

class Level():
    def __init__(self,name,polys,Ms,CMs,Av,Lz):
        self.name = name
        self.start_shapes = []
        for i in range(len(polys)):
            self.start_shapes.append(np.array(polys[i]))
        self.Ms = np.array(Ms)
        self.start_CMs = np.array(CMs)
        self.Av = Av
        self.start_Lz = np.array(Lz)
        self.angle = 0.0

        # compute safe landing zone.  This is where
        # the legs points must be within during a
        # safe landing.  It's just a rectangle
        # around the landing zone points.  We will
        # use 2 meters for this zone
        zone = 2.0
        ray = self.start_Lz[1] - self.start_Lz[0]
        ray = zone * ray / np.linalg.norm(ray)
        ang135 = 135*np.pi/180
        ang45 = 45*np.pi/180
        rot135 = np.array([[np.cos(ang135),-np.sin(ang135)], \
                               [np.sin(ang135), np.cos(ang135)]])
        rotm135 = np.array([[np.cos(-ang135),-np.sin(-ang135)], \
                               [np.sin(-ang135), np.cos(-ang135)]])
        rot45= np.array([[np.cos(ang45),-np.sin(ang45)], \
                               [np.sin(ang45), np.cos(ang45)]])
        rotm45 = np.array([[np.cos(-ang45),-np.sin(-ang45)], \
                               [np.sin(-ang45), np.cos(-ang45)]])
        lz00=(rot135  @ np.array([ray]).T).T[0] + self.start_Lz[0]
        lz01=(rotm135 @ np.array([ray]).T).T[0] + self.start_Lz[0]
        lz11=(rotm45  @ np.array([ray]).T).T[0] + self.start_Lz[1]
        lz10=(rot45   @ np.array([ray]).T).T[0] + self.start_Lz[1]
        self.start_safe_Lz = np.array([lz00,lz01,lz11,lz10])

        self.Lz = np.copy(self.start_Lz)
        self.update(0.0)

    def reset(self):
        self.angle = 0

    def update(self,dt):
        # compute rotation as needed
        self.angle = (self.angle + dt * self.Av) % (2*np.pi)

        rot_matrix = np.array([[np.cos(self.angle),-np.sin(self.angle)], \
                               [np.sin(self.angle), np.cos(self.angle)]])

        self.shapes = []
        for i in range(len(self.start_shapes)):
            self.shapes.append((rot_matrix @ self.start_shapes[i].T).T)
        self.CMs = (rot_matrix @ self.start_CMs.T).T
        self.last_Lz = np.copy(self.Lz)
        self.Lz = (rot_matrix @ self.start_Lz.T).T
        self.safe_Lz = (rot_matrix @ self.start_safe_Lz.T).T
        self.Lz_velocity = self.Lz[0] - self.last_Lz[0]

    def draw(self,scale,offset,fr,screen):
        # draw polygon and Lz on screen
        for p in self.shapes:
            pygame.draw.polygon(screen,pygame.Color('white'),p*scale+offset,width=1)

        pygame.draw.polygon(screen,pygame.Color('green'),self.Lz*scale+offset,width=1)
 
        #pygame.draw.line(screen,pygame.Color('green'),*(self.Lz*scale+offset),width=2)



