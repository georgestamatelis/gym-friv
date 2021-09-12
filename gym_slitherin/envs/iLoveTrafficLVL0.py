from os import fwalk
from gym import spaces
from gym.core import ObservationWrapper, RewardWrapper
import numpy as np
import cv2

from numpy.lib.function_base import trim_zeros
import pygame

import gym
from gym import spaces
from gym.envs.box2d.car_dynamics import Car
from gym.utils import seeding, EzPickle
from gym.envs.classic_control import rendering

import math
from gym.utils import seeding, EzPickle


WINDOW_W=500
WINDOW_H=500
STATE_W = 96  # less than Atari 160x192
STATE_H = 96

SCALE = 6.0  
FPS = 1  # Frames are taken care of by pygame
assetsPath="/home/georgestamatelis/gym-slitherin/iLoveTraffic/"

bg = pygame.image.load(assetsPath+'background.png')
bg = pygame.transform.scale(bg,(WINDOW_H,WINDOW_W))
clock = pygame.time.Clock()


class Car(object):
    def __init__(self,x,y,width,height,color=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cleared=False
        self.color=color
        self.hitbox = (self.x, self.y,self.width,self.height)
        self.HP=500
    def draw(self,win):
        self.hitbox = (self.x, self.y,self.width,self.height)
        pygame.draw.rect(win, self.color, self.hitbox)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
class iLoveTrafficEnv0(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array", "state_pixels"],
        "video.frames_per_second": FPS,
    }
    def __init__(self, verbose=1):
        """
        """
        self.win = pygame.display.set_mode((WINDOW_H,WINDOW_W))
        pygame.display.set_caption("I Love Traffic")
        self.viewer=None
        """
        actions are 
        0 do nothing
        1 change the top left traffic light
        
        """
        self.action_space=spaces.Discrete(2)
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(STATE_H,STATE_W, 3), dtype=np.uint8
        )

    def reset(self):
        """
        """
        #empty lists of cars 
        self.downCars=[]
        
        self.downCars.append(Car(230,10,25,40,(240,0,255)))
       
        self.isRedTopLeft=True
        

        #numSteps is used to determine wether a car will be generated
        self.numSteps=0
        self.numCleared=0 #if we clear enough cars we win
        observation=self.render(mode="state_pixels")

        return observation
    def step(self,action):
        """
        actions are 
        0 do nothing
        1 change the top left traffic light
        
        """
        if action == 1:
            self.isRedTopLeft= not self.isRedTopLeft
     
        self.numSteps+=1
        reward=0
        done=False
        #first generate cars
        if self.numSteps %90==0:
           
            self.downCars.append(Car(230,10,25,40,(240,0,255)))
        numWaiting=0        
        #animate existing downCars
        for c in self.downCars:
            if c.y<=225 or  self.isRedTopLeft==False or c.y >=255:
                #make sure the animations wait in line and not one no top of the other
                willCollide=False
                for c2 in self.downCars:
                    if c2.y == c.y+45:
                        willCollide=True
                        numWaiting+=1
                if not willCollide:
                    c.y+=5
            #cleared a car
            if c.y >=300 and c.cleared==False:
                c.cleared=True
                self.numCleared+=1
                reward+=1/5
            if c.y >=500:
                self.downCars.remove(c)

        
        
        if numWaiting >=4:
            print("TO MUCH TRAFFIC")
            done=True
            reward=-1
        #check end/victory condition
        if self.numCleared >=5:
            print("VICTORY")
            done=True
        state=self.render(mode="state_pixels")
        return  state,reward,done,{}  
    def render(self, mode='human', close=False):
        if mode == 'human':
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.redraw(mode="human")
        elif mode == 'rgb_array':
            img =self.redraw(mode="rgb_array") #self.get_state()
            return img
        elif mode =="state_pixels":
            img =self.redraw(mode="rgb_array") #self.get_state()
            img = self.get_state()
            img=cv2.resize(img,(STATE_H,STATE_W))
            return img
    def get_state(self):
        state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
            pygame.display.get_surface()).astype(np.uint8))))
        return state
    def redraw(self,mode="human"):
        self.win.blit(bg, (0,0))
        #draw black lines surounding the roads
        pygame.draw.rect(self.win,(1,1,1),(220,0,10,500))
        pygame.draw.rect(self.win,(1,1,1),(230+45,0,10,500))
      

        #draw the roads
        road1=(230,0,45,500)
        pygame.draw.rect(self.win, (127,127,127), road1)
        
        
        
        #top left traffic light
        pygame.draw.rect(self.win,(1,1,1),(170,265,40,40))
        if self.isRedTopLeft:
            pygame.draw.circle(self.win,(255,0,0),(190,285),12.5)
        else:
            pygame.draw.circle(self.win,(0,255,0),(190,285),12.5)
       
        for c in self.downCars:
            c.draw(self.win)
        
        if mode == "rgb_array":
            img= pygame.surfarray.array3d(self.win)
            return img
        else:
            pygame.display.update() 
if __name__ == "__main__":
    run=True
    env=iLoveTrafficEnv0()
    env.reset()
    totalRew=0
    mouseDelay=0
    while run:
        action=0
        clock.tick(27)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #for better user experience
        if mouseDelay >0:
            mouseDelay+=1
        if mouseDelay >3 :
            mouseDelay=0
        #user action
        if pygame.mouse.get_pressed()[0]==1 and mouseDelay==0:
            mx,my=pygame.mouse.get_pos()
            if 170<=mx<=210 and 260 <=my<=305:
                action=1
                mouseDelay=1
          
        obs, reward, done, info=env.step(action)
        env.render(mode='human')
        totalRew+=reward
        print("total reward=",totalRew)
        if done==True:
            break