from gym import spaces
from gym.core import ObservationWrapper
import numpy as np
import cv2

import pygame

import gym
from gym import spaces
from gym.envs.box2d.car_dynamics import Car
from gym.utils import seeding, EzPickle
from gym.envs.classic_control import rendering

import math
from gym.utils import seeding, EzPickle

STATE_W = 96  # less than Atari 160x192
STATE_H = 96

FPS = 1  # Frames are taken care of by pygame

#global variables determining where the sprites for animation are placed 
assetsPath="eyeCopter/"
flying = [pygame.image.load(assetsPath+'F1.png'), pygame.image.load(assetsPath+'F2.png'), pygame.image.load(assetsPath+'F3.png'), pygame.image.load(assetsPath+'F4.png'), pygame.image.load(assetsPath+'F5.png')]
bg = pygame.image.load('/home/georgestamatelis/gym-friv/eyeCopter/EyeCopterBG.png')
bg = pygame.transform.scale(bg,(900,700))
char = pygame.image.load(assetsPath+'standing.png')
grassPic=pygame.image.load(assetsPath+'grassBG.png')
"""
reward is 
0.3/(num of coins ) for each coin collected
0.1 for collecting the diamong
0.6 for bringing the diamond to the base
"""



#this class moves and animates the helicopter
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        self.flying=False
        self.movingRight=False
        self.movingLeft=False
        self.walkCount = 0
        self.jumpCount = 10
        self.fuelLeft=100
        self.hasDiamond=False
        self.velUp=0
        self.velLeft=0
        self.velRight=0
        self.hitbox = (self.x + 17, self.y + 11, 30, 52)

    def draw(self,win):
        if self.walkCount + 1 >= 15:
            self.walkCount = 0

       
        self.hitbox = (self.x +5, self.y + 11, 54, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

        if self.flying==False:
            win.blit(char,(self.x,self.y))
        else:
            win.blit(flying[self.walkCount // 3],(self.x,self.y))
            self.walkCount+=1
               
class Block(object):
    def __init__(self,x,y,width,height,color=(100,40,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color=color
        self.hitbox = (self.x, self.y,self.width,self.height)

    def draw(self,win):
        self.hitbox = (self.x, self.y,self.width,self.height)
        pygame.draw.rect(win, self.color, self.hitbox,0)
        pygame.draw.rect(win, (0,0,0), self.hitbox,2)

    def manOnBlock(self,man):
        rectA=pygame.Rect(self.hitbox)
        rectB=pygame.Rect(man.hitbox)
       
        if pygame.Rect.colliderect(rectA,rectB)==True:
            if self.y>=man.hitbox[1] +2*man.hitbox[3]//3:           
                return True
        
        return False
        
    def manCollides(self,man):#a collision happened but man is not above the block
        rectA=pygame.Rect(self.hitbox)
        rectB=pygame.Rect(man.hitbox)
        if self.manOnBlock(man):
            return False
        return pygame.Rect.colliderect(rectA,rectB)




class Coin:
    def __init__(self,x,y,radius,color=(200,150,0)):
        self.x = x
        self.y = y
        self.color=color
        self.radius=radius
        self.hitbox=(self.x-self.radius,self.y-self.radius,2*self.radius,2*self.radius)
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
class Diamond:
    def __init__(self,x,y,):
        self.x = x
        self.y = y
        self.img=pygame.image.load(assetsPath+'diamond.png')
        self.hitbox=(self.x,self.y+20,45,25)
    def draw(self,win):
        self.hitbox=(self.x,self.y+20,45,25)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
        win.blit(self.img,(self.x,self.y))
        
class Platform:
    def __init__(self,x,y,):
        self.x = x
        self.y = y
        self.fireHeight=50
        self.vel=-2.5
        self.img=pygame.image.load(assetsPath+'platform.png')
        self.active=False
        self.hitbox=(self.x+5,self.y+40,55,25)
    def draw(self,win):
        self.hitbox=(self.x+5,self.y+40,55,25)
        
        fireBox=(self.x+12,self.y+40+20-self.fireHeight,45,self.fireHeight)
        if self.fireHeight >=50:
            self.vel=-2.5
        if self.fireHeight <=10:
            self.vel=2.5
        self.fireHeight+=self.vel
        pygame.draw.rect(win, (250,250,250),fireBox)   
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
        win.blit(self.img,(self.x,self.y))
class Goal:
    def __init__(self,x,y,):
        self.x = x
        self.y = y
        self.fireHeight=0
        self.img=pygame.image.load(assetsPath+'diamond.png')
        self.hitbox=(self.x,self.y+20,45,25)
    def draw(self,win):
             
        win.blit(self.img,(self.x,self.y))

class eyeCopterEnv1(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array", "state_pixels"],
        "video.frames_per_second": FPS,
    }

    def __init__(self, verbose=1):
        """
        the player moves the helicopter trying to collect the diamond and then 
        bring back to the goal/base for take off. Bonus points for coins collected. 
        If the helicopter moves out of site it is lost. If the player takes too long
        they loose
        """
        pygame.init()
        self.win = pygame.display.set_mode((900,700))
        self.viewer=None
        pygame.display.set_caption("Eye Copter")
        """
        actions are 
        0 do nothing
        1 fly 
        2 left
        3 right 
        4 fly left
        5 fly right
        """
        self.action_space=spaces.Discrete(6)
        """
        the state is a STATE_H x STATE_W SCREENSHOT OF THE GAME CONSOLE
        """
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(STATE_H,STATE_W, 3), dtype=np.uint8
        )
    def reset(self) :
        self.totalTimeSteps=0
        self.font = pygame.font.SysFont('comicsans', 30, True)
        self.man = player(20, 280, 64,64)
        self.goal = Diamond(840,300)
        self.blocks=[]
        self.coins=[]
        self.pl=Platform(20,290)
        #first two rows no the left
        for w in [0,30,60,90,120,150]:
            for h in [350,380]:
                self.blocks.append(Block(w,h,30,30))

        #third row on left
        for w in [0,30,60,90,120]:
            self.blocks.append(Block(w,410,30,30))

        #last row on left
        for w in [0,30,60,90]:
            self.blocks.append(Block(w,440,30,30))

        #first two rows no the right
        for w in [720,750,780,810,840,870]:
            for h in [350,380]:
                self.blocks.append(Block(w,h,30,30))

        #third row on right
        for w in [750,780,810,840,870]:
            self.blocks.append(Block(w,410,30,30))

        #last row on right
        for w in [780,810,840,870]:
            self.blocks.append(Block(w,440,30,30))
        #now draw the 12 self.coins
        self.coins.append(Coin(200,250,10))
        self.coins.append(Coin(240,210,10))
        self.coins.append(Coin(280,170,10))
        self.coins.append(Coin(320,130,10))
        self.coins.append(Coin(360,90,10))
        self.coins.append(Coin(400,60,10))
        self.coins.append(Coin(440,60,10))
        self.coins.append(Coin(480,90,10))
        self.coins.append(Coin(520,130,10))
        self.coins.append(Coin(560,170,10))
        self.coins.append(Coin(600,210,10))
        self.coins.append(Coin(640,250,10))

        self.onBlock=False
        observation=self.render(mode="state_pixels")#self.get_state()
        self.render(mode='human')
        #state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
        #     pygame.display.get_surface()).astype(np.uint8))))
        return observation
    def step(self,action):
        """
        actions are 
        0 do nothing
        1 fly 
        2 left
        3 right 
        4 fly left
        5 fly right
        """
        self.totalTimeSteps+=1
        reward=0
        done=False
        self.onBlock=False
        for b in self.blocks:
            if b.manOnBlock(self.man):
                self.onBlock=True
                self.man.flying=False
        
        if (-20<=self.man.hitbox[0] <= 180) or (670<=self.man.hitbox[0]<=930):
            if 290<=self.man.hitbox[1]<=360:
                self.onBlock=True
        if self.onBlock==False:
            self.man.y+=2*self.man.vel
        if  action==2 or action==4 :
            if self.onBlock==True:
                self.man.x-=self.man.vel*0.25
            else :
                self.man.x -=self.man.vel
            self.man.movingLeft=True
            self.man.movingRight=False
        elif action==3 or action==5:
            if self.onBlock==True:
                self.man.x+=self.man.vel*0.25
            else:
                self.man.x+=self.man.vel
            self.man.movingRight=True        
            self.man.movingLeft=False

        else: #neither left nor right
            self.man.movingLeft=False
            self.man.movingRight=False
        #fly
        if action==1 or action==4 or action==5:
            #self.man.y-=3*self.man.vel
            if self.man.velUp==0:
                self.man.velUp=15
            if self.man.velUp<=60:
                self.man.velUp+=5
            self.man.flying=True
        else:
            self.man.velUp=0
        #print("Self.man.velups=",self.man.velUp)
        self.man.y-=self.man.velUp
        #check collision with blocks
        for b in self.blocks:
            if b.manCollides(self.man) and self.onBlock==False:
                if self.man.movingRight==True:
                    self.man.x-=self.man.vel 
                elif self.man.movingLeft==True:
                    self.man.x+=self.man.vel
                if self.man.flying==True and self.man.y<=b.y+b.height:
                    self.man.y+=self.man.velUp
                    self.man.velUp=15
        #check collision with coins
        for c in self.coins:
            rectA=pygame.Rect(c.hitbox)
            rectB=pygame.Rect(self.man.hitbox)
            if pygame.Rect.colliderect(rectA,rectB):
                self.coins.remove(c)
                reward+=0.3*1/12
        #check diamong
        rectA=pygame.Rect(self.goal.hitbox)
        rectB=pygame.Rect(self.man.hitbox)
        if pygame.Rect.colliderect(rectA,rectB):
            self.man.hasDiamond=True
            reward+=0.1
            self.pl.active=True

        if self.man.hasDiamond==True:
            self.goal.x=self.man.x +10
            self.goal.y = self.man.y +45
            rectA=pygame.Rect(self.man.hitbox)
            rectB=pygame.Rect(self.pl.hitbox)
            if pygame.Rect.colliderect(rectA,rectB):
                print("VICTORY")
                reward+=0.6
                done=True

        #check bounds
        if self.man.x <=-60 or self.man.x >=960:
            print("GAME OVER ")
            reward=-1
            done=True
        if self.man.y >=820 or self.man.y<=-120:
            print("GAME OVER")
            reward=-1
            done=True
        if self.totalTimeSteps >=2000:
            done=True
            reward=-1
            print("TIME OUT")
        state=self.render(mode="state_pixels")#self.get_state()
        self.render(mode='human')
        
        return state,reward,done,{}
    def get_state(self):
        state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
            pygame.display.get_surface()).astype(np.uint8))))
        return state
    def redraw(self, mode="human"):
        """
        """
        self.win.blit(bg, (0,0))
        self.win.blit(grassPic,(0,260))
        self.win.blit(grassPic,(80,260))
        self.win.blit(grassPic,(720,260))
        self.win.blit(grassPic,(820,260))

        for b in self.blocks:
            b.draw(self.win)
        for c in self.coins:
            c.draw(self.win)
        self.man.draw(self.win)
        self.goal.draw(self.win)
        if self.pl.active:
            self.pl.draw(self.win)
        if mode == "rgb_array":
            img= pygame.surfarray.array3d(self.win)
            return img
        else:
            pygame.display.update() 

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
#main function for user play
#just type python3 <path to file> /eyeCopterEnv1.py to play as a human agent
if __name__ == "__main__":
    run=True
    env=eyeCopterEnv1()
    env.reset()
    totalRew=0
    while run:
        #clock.tick(27)


    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #action=env.action_space.sample()
        action=0 #do nothing
        keys = pygame.key.get_pressed()

       
       
        """
        actions are 
        0 do nothing
        1 fly 
        2 left
        3 right 
        4 fly left
        5 fly right
        """
        left=False
        right=False
        fly=False
        if keys[pygame.K_LEFT]:
            left=True
        if keys[pygame.K_RIGHT]:
            right=True
        
        if keys[pygame.K_UP]:
            fly=True
        ############################
        action=0
        if left==True:
            if fly==True: #fly left
               action=4
            else:
                action=2
        elif right==True:
            if fly==True: #fly right
               action=5
            else:
                action=3
            
        if fly==True and (left==False and right==False):
            action=1
        obs, reward, done, info=env.step(action)
        env.render(mode='human')
        totalRew+=reward
        print("total reward=",totalRew)
        if done==True:
            break
        #env.rende