import numpy as np 

import pygame
import random
import cv2 
import matplotlib.pyplot as plt
from gym.envs.classic_control import rendering

import PIL.Image as Image
import gym
import random
import os 
from gym import Env, spaces
import time
import random
"""
the cars in this game appear a little les frequently, 
they move with half the speed,
the logs appear a litle more frequently

and the chicken is slightly faster
"""

"""
On both games 
reward = 0.3 for reaching the logs, 
0.2 for reaching the second road 
and 0.5 for finishing
"""

font = cv2.FONT_HERSHEY_COMPLEX_SMALL 
clock = pygame.time.Clock()

#this is where the sprites for the characters are located
assetsPath="/home/georgestamatelis/gym-friv/chickenGo/"

class Chicken(object):
    walkRight = [pygame.image.load(assetsPath+'R1.png'), pygame.image.load(assetsPath+'R2.png'), pygame.image.load(assetsPath+'R3.png'), pygame.image.load(assetsPath+'R4.png'), pygame.image.load(assetsPath+'R5.png'), pygame.image.load(assetsPath+'R6.png'), pygame.image.load(assetsPath+'R7.png')]
    walkLeft = [pygame.image.load(assetsPath+'L1.png'), pygame.image.load(assetsPath+'L2.png'), pygame.image.load(assetsPath+'L3.png'), pygame.image.load(assetsPath+'L4.png'), pygame.image.load(assetsPath+'L5.png'), pygame.image.load(assetsPath+'L6.png'), pygame.image.load(assetsPath+'L7.png')]
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel = 20
        self.standing=True
        self.movingRight=False
        self.movingLeft=False
        self.walkCount = 0
        self.hitbox = (self.x,self.y, 44, 40)

    def draw(self, win):
        if self.walkCount + 1 >= 21:
            self.walkCount = 0
        if self.standing==True:
            win.blit(self.walkRight[0], (self.x,self.y))

        elif self.movingRight:
            self.walkCount+=1
            win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        else:
            self.walkCount+=1
            win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount +=1
        if self.movingLeft==True:
            self.hitbox = (self.x,self.y, 44, 40)
        else:
            self.hitbox = (self.x+7,self.y, 44, 40)
            
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
class log(object):
    def __init__(self,x,y,vel):
        self.x=x 
        self.y=y 
        self.width=50
        self.height=70
        self.vel=vel
        self.hitbox = (self.x,self.y, self.width, self.height)

    def draw(self,win):
        self.y+=self.vel
        self.hitbox = (self.x,self.y, self.width, self.height)
        pygame.draw.rect(win,(140,100,0),self.hitbox,0)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

class Car(object):
    def __init__(self,x,y,vel):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 80
        self.vel=vel
        self.hitbox = (self.x, self.y,self.width,self.height)
    def draw(self,win):
        self.y+=self.vel

        self.hitbox = (self.x, self.y,self.width,self.height)
        pygame.draw.rect(win, (240,0,255), self.hitbox)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

STATE_H =75
STATE_W =150
class chickenGoEnvSlow(Env):
    metadata = {
        'render.modes': ['human', 'rgb_array',"state_pixels"],
        'video.frames_per_second': 1 # pygame takes care of frames
    }
    def __init__(self):
        super(chickenGoEnvSlow, self).__init__()
        self.win= pygame.display.set_mode((1000,500))
        self.viewer=None
        pygame.display.set_caption("GO CHICKEN GO !!")
        """
        actions are
        0 = do nothing 
        1 = move left 
        2 = move right 
        3 = move up 
        4 = move down 
        5 = move left and up
        6 = move left and down
        7 = right and up
        8 = right and down
        """
        self.action_space=spaces.Discrete(9)
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(STATE_H,STATE_W, 3), dtype=np.uint8
        )

       
       


    def reset(self):
        self.cars=[]
        self.logs=[]
        self.chickens=[]
        self.chickens.append(Chicken(15,25))
        self.c=self.chickens[0]
        self.hasReachedLogs=False
        self.hasReachedSecondRoad=False

        self.totalTimeSteps=0
        observation=self.render(mode="state_pixels")
        return observation
        
    def get_state(self):
        state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
            pygame.display.get_surface()).astype(np.uint8))))
        return state
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
            img=cv2.resize(img,(STATE_W,STATE_H))
            return img
    def redraw(self,mode="human"):
        #first draw the background
        pygame.draw.rect(self.win,(20,200,0),(0,0,150,500))
        pygame.draw.rect(self.win,(200,200,110),(150,0,20,500))
        pygame.draw.rect(self.win,(127,127,127),(170,0,230,500))
        pygame.draw.rect(self.win,(200,200,110),(380,0,20,500))
        pygame.draw.rect(self.win,(0,70,150),(400,0,150,500))
        pygame.draw.rect(self.win,(200,200,110),(550,0,20,500))
        pygame.draw.rect(self.win,(127,127,127),(570,0,230,500))
        pygame.draw.rect(self.win,(200,200,110),(790,0,20,500))
        pygame.draw.rect(self.win,(20,200,0),(810,0,200,500))
        for c in self.cars:
            c.draw(self.win)
        for c in self.logs:
            c.draw(self.win)
        for c in self.chickens:
            c.draw(self.win)
        if mode == "rgb_array":
            img= pygame.surfarray.array3d(self.win)
            return img
        else:
            pygame.display.update() 
    
    def step(self, action):
        clock.tick(27)

        self.totalTimeSteps+=1
        """
        actions are
        0 = do nothing 
        1 = move left 
        2 = move right 
        3 = move up 
        4 = move down 
        5 = move left and up
        6 = move left and down
        7 = right and up
        8 = right and down
        """
        """
        DEAL WITH ACTIONS
        """
        if (action==1 or action ==5 or action==6) and self.c.x > 0:
            self.c.x-=5
            self.c.movingLeft=True
            self.c.movingRight=False
            self.c.standing=False
        elif (action==2 or action==7 or action==8) and self.c.x <= 990:
            self.c.x+=5
            self.c.movingLeft=False
            self.c.movingRight=True
            self.c.standing=False
        else:
            self.c.movingLeft=False
            self.c.movingRight=False
            self.c.standing=True
        if (action==3 or action==5 or action==7) and self.c.y >=10:
            self.c.y-=5
            self.c.movingRight=True
            self.c.movingLeft=False
            self.c.standing=False

        if (action==4 or action==6 or action==8) and self.c.y <=490:
            self.c.y+=5
            self.c.movingRight=True
            self.c.movingLeft=False
            self.c.standing=False
        """
        GENERATE LOGS AND CARS
        """
        if self.totalTimeSteps %50 ==0:
            self.logs.append(log(420,520,-2))
            self.logs.append(log(490,-20,2))
        if self.totalTimeSteps %120==0 or self.totalTimeSteps ==50 :
            self.cars.append(Car(190,-20,2))
        if self.totalTimeSteps %150==0 or self.totalTimeSteps ==100  :
            self.cars.append(Car(250,-20,2))
        if self.totalTimeSteps %160==0 or self.totalTimeSteps == 70 :
            self.cars.append(Car(315,-20,2))
        if self.totalTimeSteps %110==0 and random.random()<=0.8:
            self.cars.append(Car(570,520,-2))
        if self.totalTimeSteps %150==0 and random.random()<=0.6:
            self.cars.append(Car(570+60,520,-2))
        if self.totalTimeSteps %120==0 and random.random()<=0.8:
            self.cars.append(Car(570+120,520,-2))
        """
        COLISION AND "DROWNING" DETECTION
        """
        onLog=False
        reward=0
        done=False
        for l in self.logs:
            rectA=pygame.Rect(l.hitbox)
            rectB=pygame.Rect(self.c.hitbox)
            #print(rectB)
            #print(pygame.Rect.colliderect(rectA,rectB))
            if pygame.Rect.colliderect(rectA,rectB)==True:
                self.c.y+=l.vel*2#*3
                onLog=True
                if self.hasReachedLogs==False:
                    reward+=0.3
                    self.hasReachedLogs=True
                break
            if l.y<=-80:
                self.logs.remove(l)
        if 390<=self.c.x<=506 and onLog==False:
            print("DROWN")
            reward=-1
            done=True
            state=self.render(mode="state_pixels")
            return state,reward,done,{}
        if self.c.y <=-30 or self.c.y >=530:
            print("OUT OF BOUNDS")
            reward=-1
            done=True
            state=self.render(mode="state_pixels")
            return state,reward,done,{}
        for car in self.cars:
            rectA=pygame.Rect(car.hitbox)
            rectB=pygame.Rect(self.c.hitbox)
            #detect collision with chicken
            if pygame.Rect.colliderect(rectA,rectB)==True:
                print("COLISSION GAME OVER")
                reward=-1
                done=True
                state=self.render(mode="state_pixels")
                return state,reward,done,{}
            if car.y >=540 or car.y <=-40:
                self.cars.remove(car)
        if self.c.x >=820:
            print("VICTORY")
            reward+=0.5
            done=True
            state=self.render(mode="state_pixels")
            return state,reward,done,{}
        if self.hasReachedSecondRoad==False and self.c.x >=510:
            reward+=0.2
            self.hasReachedSecondRoad=True
        state=self.render(mode="state_pixels")
        return state,reward,done,{}


if __name__ == "__main__":
    run=True
    env=chickenGoEnvSlow()
    env.reset()
    totalRew=0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #action=env.action_space.sample()
        action=0 #do nothing
        keys = pygame.key.get_pressed()
        """
        actions are
        0 = do nothing 
        1 = move left 
        2 = move right 
        3 = move up 
        4 = move down 
        5 = move left and up
        6 = move left and down
        7 = right and up
        8 = right and down
        """
        left=False
        right=False
        up=False
        down=False
        if keys[pygame.K_LEFT] :
            left=True
        elif keys[pygame.K_RIGHT]:
            right=True
        if keys[pygame.K_UP]:
            up=True
        elif keys[pygame.K_DOWN]:
            down=True 
        if left==True:
            if up==True:
                action=5
            elif down==True:
                action=6
            else:
                action=1
        elif right==True:
            if up==True:
                action=7
            elif down==True:
                action=8
            else:
                action=2
        if up==True and (left==False and right==False):
            action=3
        if down==True and (left==False and right==False and up==False):
            action=4
        obs, reward, done, info=env.step(action)
        env.render(mode='human')
        totalRew+=reward
        print("total reward=",totalRew)
        if done==True:
            break
        
