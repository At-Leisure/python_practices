import pygame
import math
import time
import os

class Circle:
    def __init__(self,color,position,raduis,width):
        self.color = color
        self.position = position
        self.raduis = raduis
        self.width = width

    def draw(self,screen):
        pygame.draw.circle(screen,
            color = self.color,
            center = self.position,
            radius = self.raduis,
            width = self.width)

    @property
    def center_xy(self):
        return self.position

    @center_xy.setter
    def center_xy(self,tuple_):
        self.position = tuple_

class Linecircle:
    def __init__(self,master,center=(0,0),line_length=50,theta=0,first_theta=0,circle_color=(255,255,255)) -> None:
        """ 0 <= theta,first_theta < 180 """
        print(f'{circle_color=}')
        self.circle = Circle(circle_color,center,20,0)
        self.master = master
        self.length = line_length/2
        self.center = center
        self.first_theta = math.pi/180*first_theta
        self.reset_theta(theta%180)
        self.omega = 2
        self.birth_time = time.time()

    def draw(self):
        pygame.draw.line(self.master,(100,100,100),self.start_xy,self.end_xy,1)
        dist = self.length * math.cos( self.omega * time.time() - self.birth_time  +  self.first_theta)
        self.circle.center_xy = (self.center[0]+dist*math.cos(self.theta), self.center[1]+dist*math.sin(self.theta))
        self.circle.draw(self.master)

    def reset_theta(self,theta):
        self.theta = math.pi/180* -theta
        self.start_xy = (self.center[0]-math.cos(self.theta)*self.length, self.center[1]-math.sin(self.theta)*self.length)
        self.end_xy = (self.center[0]+math.cos(self.theta)*self.length, self.center[1]+math.sin(self.theta)*self.length)


class Seen:
    def __init__(self,wid,hei) -> None:
        self.wid = wid
        self.hei = hei

    @property
    def size(self):
        return (self.wid, self.hei)

    @size.setter
    def size(self, wid, hei):
        self.wid = wid
        self.hei = hei

    @property
    def center(self):
        return (self.wid/2, self.hei/2)

