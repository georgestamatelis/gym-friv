#from gym_friv.envs.zombieOnslaught import zombieOnslaught
import numpy as np 
import cv2 
import matplotlib.pyplot as plt
import PIL.Image as Image
import gym
from gym.envs.classic_control import rendering

import random
import os
from numpy.core.fromnumeric import reshape 
from scipy import ndimage
import pygame
from gym_friv.envs.zombieClasses  import *


from gym import Env, spaces
import time

FPS=30
STATE_W=100
STATE_H=100
WINDOW_W=500
WINDOW_H=500
class zombieOnslaughtEasyEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 27
    }
    def __init__(self):
        """
        """
        pygame.init()

        self.win = pygame.display.set_mode((WINDOW_W,WINDOW_H))

        self.viewer=None
        """
        actions are
        0 nothing
        1 up
        2 down
        3 shoot
        """
        self.action_space=spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(STATE_H,STATE_W, 3), dtype=np.uint8
        )
        self.zombiesToKill=6
        self.positions=[400,300,200]
        self.bg = pygame.image.load(assetsPath+'backround.png')
        self.bg = pygame.transform.scale(self.bg,(WINDOW_H,WINDOW_W))
        #clock = pygame.time.Clock()
        self.viewer=None

    def reset(self):
        """
        """
        #print("RESETING")
        self.zombiesKilled=0
        self.Crates=[]
        self.Crates.append(Crate(75,self.positions[0]+40,30,40,color=(100,40,0)))
        self.Crates.append(Crate(75,self.positions[1]+40,30,40,color=(100,40,0)))
        self.Crates.append(Crate(75,self.positions[2]+40,30,40,color=(100,40,0)))

        self.weakZombies=[]
        self.bullets=[]
        #player 
        self.man=player(10,self.positions[0],50,50)
        #weak zombies
        self.weakZombies.append(weakZombie(500,self.positions[0],64,64))
        self.weakZombies.append(weakZombie(550,self.positions[1],64,64))
        self.weakZombies.append(weakZombie(570,self.positions[2],64,64))
        self.weakZombies.append(weakZombie(500,self.positions[1],64,64))
        self.weakZombies.append(weakZombie(620,self.positions[1],64,64))
        self.weakZombies.append(weakZombie(570,self.positions[0],64,64))

        self.shootReset=0
        self.run = True
        self.goalPos=self.man.y
        self.moveReset=0

        state=self.render(mode="state_pixels")
        return state

    def step(self,action):
        """
        """
        if self.shootReset>=7:
            self.shootReset=0
        if self.shootReset >0:
            self.shootReset+=1
        if self.moveReset>0:
            self.moveReset+=1
        if self.moveReset >3:
            self.moveReset=0
        """
        ANIMATE BULLETS
        """

        reward=0
        done=False
        for bullet in self.bullets:
            if bullet.x <=500 and bullet.x >0:
                bullet.x +=bullet.vel
            else:
                self.bullets.pop(self.bullets.index(bullet)) 
                continue
            for z in self.weakZombies:
                rectA=pygame.Rect(z.hitbox)
                rectB=pygame.Rect(bullet.hitbox)
                if pygame.Rect.colliderect(rectA,rectB)==True:
                    z.HP-=50
                    if z.HP<=0:
                        self.weakZombies.remove(z)
                        self.zombiesKilled+=1
                        reward+=1.0/self.zombiesToKill
                    self.bullets.pop(self.bullets.index(bullet))
        if self.zombiesKilled==self.zombiesToKill:
            print("VICTORY")
            done=True
            state=self.render(mode="state_pixels")
            return state,reward,done,{}
        """
        now check collision between zombies and crates
        """
        for wz in self.weakZombies:
            for cr in self.Crates:
                if cr.manCollides(wz):
                    cr.HP-=50
                    wz.vel=0
                    if cr.HP<=0:
                        self.Crates.remove(cr)
                        wz.vel=+3
            if wz.x<=0:
                print("GAME OVER")
                done=True 
                reward=-1
                state=self.render(mode="state_pixels")
                return state,reward,done,{}

        
        if (not self.man.isMoving ) :
            if self.moveReset >0:
                state=self.render(mode="state_pixels")
                return state,reward,done,{}
            if action==1:
                self.man.isMoving=True
                if self.man.y==self.positions[0]:
                    self.goalPos=self.positions[1]
                    self.man.vel=-5
                elif self.man.y==self.positions[1]:
                    self.goalPos=self.positions[2]
                    self.man.vel=-5
                else:
                    self.man.isMoving=False
            elif action==2:
                self.man.isMoving=True
                if self.man.y==self.positions[2]:
                    self.goalPos=self.positions[1]
                    self.man.vel=+5
                elif self.man.y==self.positions[1]:
                    self.goalPos=self.positions[0]
                    self.man.vel=+5
                else:
                    self.man.isMoving=False
            elif action==3:
                if self.shootReset>0:
                    state=self.render(mode="state_pixels")
                    return state,reward,done,{}
                if len(self.bullets)<=15:
                    facing=1
                    bullet=projectile(
                        round(self.man.x+self.man.width+5),round(self.man.y+self.man.height//2),6,(0,0.2,0.6),facing)
                    self.bullets.append(bullet)
                    self.shootReset+=1
                    self.shooting=True
        else:
            #print("goalPos=",goalPos,"man.y=",man.y)
            self.man.y+=self.man.vel 
            self.man.walkCount+=1
            if self.man.y==self.goalPos and self.man.isMoving:
                self.man.isMoving=False
                self.man.walkCount=0
                if self.moveReset==0:
                    self.moveReset=1
        state=self.render(mode="state_pixels")
        return state,reward,done,{}
    def get_state(self):
        state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
            pygame.display.get_surface()).astype(np.uint8))))
        return state
    def redrawGameWindow(self,mode="human"):
        self.win.blit(self.bg, (0,0))
        self.man.draw(self.win)
        for cr in self.Crates:
            cr.draw(self.win)
        for wz in self.weakZombies:
            wz.draw(self.win)
        for bullet in self.bullets:
            bullet.draw(self.win)
        if mode=="rgb_array":
            img= pygame.surfarray.array3d(self.win)
            return img
        elif mode=="human":
            pygame.display.update()

    def render(self,mode = "human"):
        """
        """
        if mode == 'human':
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.redrawGameWindow(mode="human")
        elif mode == 'rgb_array':
            img =self.redrawGameWindow(mode="rgb_array") #self.get_state()
            return img
        elif mode =="state_pixels":
            img =self.redrawGameWindow(mode="rgb_array") #self.get_state()
            img = self.get_state()
            img=cv2.resize(img,(STATE_H,STATE_W))
            return img
    #main function for user play
if __name__ == "__main__":
    run=True
    env=zombieOnslaughtEasyEnv()
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
        0 nothing
        1 up 
        2 down
        3 =shoot
        """
        action=0
        if keys[pygame.K_UP]:
            action=1
        elif keys[pygame.K_DOWN]:
            action=2
        elif keys[pygame.K_a]:
            action=3
        ############################
        
        obs, reward, done, info=env.step(action)
        env.render(mode='human')
        totalRew+=reward
        print("total reward=",totalRew)
        if done==True:
            obs=env.reset()
            totalRew=0
        #env.render()
    

