from os import fwalk
from gym import spaces
from gym.core import ObservationWrapper
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
#from topDownCar import *
FPS=1

"""
ASSETS
"""
assetsPath="/home/georgestamatelis/gym-slitherin/Game/"
walkRight = [pygame.image.load(assetsPath+'R1.png'), pygame.image.load(assetsPath+'R2.png'), pygame.image.load(assetsPath+'R3.png'), pygame.image.load(assetsPath+'R4.png'), pygame.image.load(assetsPath+'R5.png'), pygame.image.load(assetsPath+'R6.png'), pygame.image.load(assetsPath+'R7.png'), pygame.image.load(assetsPath+'R8.png'), pygame.image.load(assetsPath+'R9.png')]
walkLeft = [pygame.image.load(assetsPath+'L1.png'), pygame.image.load(assetsPath+'L2.png'), pygame.image.load(assetsPath+'L3.png'), pygame.image.load(assetsPath+'L4.png'), pygame.image.load(assetsPath+'L5.png'), pygame.image.load(assetsPath+'L6.png'), pygame.image.load(assetsPath+'L7.png'), pygame.image.load(assetsPath+'L8.png'), pygame.image.load(assetsPath+'L9.png')]
bg = pygame.image.load(assetsPath+'agentPlatformerBG.png')
bg = pygame.transform.scale(bg,(900,700))
char = pygame.image.load(assetsPath+'standing.png')

clock = pygame.time.Clock()

score = 0


"""
CLASSES USED BY THE ACTUAL ENVIRONMENT / GAME
"""
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.flying = False
        self.fuelLeft=100
        self.hitbox = (self.x + 17, self.y + 11, 30, 52)
        self.movingRight=True
        self.movingLeft=False

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
               
class Block(object):
    def __init__(self,x,y,width,height,color=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color=color
        self.hitbox = (self.x, self.y,self.width,self.height)

    def draw(self,win):
        self.hitbox = (self.x, self.y,self.width,self.height)
        pygame.draw.rect(win, self.color, self.hitbox,0)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def manOnBlock(self,man):
        rectA=pygame.Rect(self.hitbox)
        rectB=pygame.Rect(man.hitbox)
        #print(rectB)
        #print(pygame.Rect.colliderect(rectA,rectB))
        if pygame.Rect.colliderect(rectA,rectB)==True:
            #print("self.y=",self.y,"many=",man.hitbox[1],"height=",man.hitbox[3])
            if self.y>=man.hitbox[1] +4*man.hitbox[3]//5:
                return True
        #print(pygame.Rect.collidelistall(self.hitbox))
        return False
        
    def manCollides(self,man):#a collision happened but man is not above the block
        rectA=pygame.Rect(self.hitbox)
        rectB=pygame.Rect(man.hitbox)
        if self.manOnBlock(man):
            return False
        return pygame.Rect.colliderect(rectA,rectB)
        #print(pygame.Rect.colliderect(rectA,rectB))
        #if pygame.Rect.colliderect(rectA,rectB)==True:
        #    if self.y+self.height >=man.y:#+man.height:
        #        return True
        #print(pygame.Rect.collidelistall(self.hitbox))
        #return False
class Spikes(object):
    def __init__(self,x,y,width,height,color=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color=color
        self.hitbox = (self.x, self.y,self.width,self.height)
        self.img=pygame.image.load(assetsPath+"nails.png")
        self.img=pygame.transform.scale(self.img,(50,50))

    def draw(self,win):
        win.blit(self.img,(self.x,self.y))

    def manDown(self,man):
        xOk=False
        yOk=False
        if self.x <= man.hitbox[0] <=self.x + self.width:
            xOk=True
        if self.x <= man.hitbox[0] +man.hitbox[2] <=self.x + self.width:
            xOk=True
        #print("xOk=",xOk,"self.y=",self.y,"man.y=",man.y,"height=",self.height)
        if self.y-self.height<=man.y <=self.y:
            yOk=True
        return (xOk and yOk)

class Vacum(object):
    def __init__(self,x,y,width,height,color=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color=color
        self.hitbox = (self.x, self.y,self.width,self.height)
        self.img=pygame.image.load(assetsPath+"platformVacum.png")
        self.img=pygame.transform.scale(self.img,(self.width,self.height))

    def draw(self,win):
        win.blit(self.img,(self.x,self.y))
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
class Coin:
    def __init__(self,x,y,radius,color=(200,150,0)):
        self.x = x
        self.y = y
        self.color=color
        self.radius=radius
        self.hitbox=(self.x-self.radius,self.y-self.radius,2*self.radius,2*self.radius)
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)


"""
 ENVIRONMENT
"""
STATE_W = 100  # less than Atari 160x192
STATE_H = 100
class agentPlatformerEnv(gym.Env, EzPickle):
    metadata = {
        "render.modes": ["human", "rgb_array", "state_pixels"],
        "video.frames_per_second": FPS,
    }

    def __init__(self, verbose=1):
        """
        
        """
        pygame.init()

        self.win = pygame.display.set_mode((900,700))
        self.viewer=None
        pygame.display.set_caption("Agent Platformer")
        """
        actions are
        0 nothing
        1 left 
        2 right
        3 jump
        4 fly
        5 jump left
        6 jump right
        7 fly left
        8 fly right
        """
        self.action_space=spaces.Discrete(9)
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(STATE_H,STATE_W, 3), dtype=np.uint8
        )

    def _destroy(self):
        """
        """
    def reset(self):
        """
        """
        self._destroy()
        #mainloop
        self.font = pygame.font.SysFont('comicsans', 30, True)
        self.man = player(50, 20, 64,64)
        self.blocks=[]
        self.spikes=[]
        self.vacums=[]  
        self.coins=[]

        self.coins.append(Coin(230,230,10))
        self.coins.append(Coin(260,230,10))
        self.coins.append(Coin(785,620,10))
        self.coins.append(Coin(785,590,10))
        self.coins.append(Coin(785,560,10))
        self.coins.append(Coin(785,530,10))


        self.blocks.append(Block(300,0,50,400))
        self.blocks.append(Block(225,250,75,50))
        self.blocks.append(Block(350,350,75,50))
        self.blocks.append(Block(400,400,75,50))
        self.blocks.append(Block(500,250,75,50))

        self.blocks.append(Block(440,270,40,20,color=(255,255,255)))


        self.blocks.append(Block(650,200,100,50))

        #spikes in air
        self.blocks.append(Block(200,525,50,50))
        self.spikes.append(Spikes(250,525,50,50))
        self.blocks.append(Block(300,525,50,50))

        self.goalBlock=Block(675,175,25,25,color=(255,255,255))
        self.movingDownwards=True

        self.spikes.append(Spikes(650,650,50,50))   
        self.spikes.append(Spikes(700,650,50,50))


        self.vacums.append(Vacum(675,250,50,300))


        self.blocks.append(Block(475,500,50,50))
        self.vacums.append(Vacum(525,500,50,150))
        self.blocks.append(Block(575,500,50,50))


        self.vel=1
        self.onBlock=False
        #self.redraw(mode="rgb_array")
        observation=self.render(mode="state_pixels")#self.get_state()
        #state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
        #     pygame.display.get_surface()).astype(np.uint8))))
        return observation
    def step(self, action):
        """
        actions are
        0 nothing
        1 left 
        2 right
        3 jump
        4 fly
        5 jump left
        6 jump right
        7 fly left
        8 fly right
        """

        done=False
        reward=0
        if (action==1 or action==5 or action==7) and self.man.x>=30:
            self.man.x -= self.man.vel
            self.man.left = True
            self.man.right = False
            self.man.standing = False
            self.man.movingRight=False
            self.man.movingLeft=True
        elif (action==2 or action==6 or action==8) and self.man.x<850 - self.man.width - self.man.vel:
            self.man.x += self.man.vel
            self.man.right = True
            self.man.left = False 
            self.man.standing = False
            self.man.movingLeft=False
            self.man.movingRight=True
        else:
            self.man.movingRight=False
            self.man.movingLeft=False
            self.man.standing = True
            self.man.walkCount = 0
        if (action==4 or action==7 or action==8) and self.man.y >=10 and self.man.fuelLeft>0:
            manCollides=False
            for b in self.blocks:
                if b.manCollides(self.man):
                    manCollides=True
            if manCollides==False:
                self.man.y=self.man.y-self.man.vel -10 # 10 is to undo gravity    
                inVacum=False
                rectB=pygame.Rect(self.man.hitbox)
                for v in self.vacums:
                    rectA=pygame.Rect(v.hitbox)
                    if pygame.Rect.colliderect(rectA,rectB):
                        inVacum=True 
                if inVacum==False:
                    self.man.fuelLeft-=2
                self.man.flying=True
        else:
            if self.man.fuelLeft<100:
                self.man.fuelLeft+=1
        if  not(self.man.isJump):
            if (action==3 or action==5 or action==6) and self.man.y >=120 and (self.onBlock==True or self.man.y>=580): 
                self.man.isJump = True
                self.man.right = False
                self.man.left = False
                self.man.walkCount = 0
                movingDownwards=False
        else:
            if self.man.jumpCount >= 0:
                neg = 1
                if self.man.jumpCount < 0:
                    neg = -1
                
                self.man.y -= (self.man.jumpCount ** 2) * 0.5 * neg
                self.man.jumpCount -= 1
            else:
                movingDownwards=True
                self.man.isJump = False
                self.man.jumpCount = 10
        self.onBlock=False
        for block in self.blocks:
            if block.manOnBlock(self.man): 
                #man.y=-man.height+block.y
                self.onBlock=True
        for block in self.blocks:
            if block.manCollides(self.man):
                #print("Man Colides")
                if not self.onBlock and (self.man.isJump==True or self.man.flying==True): 
                    #man.y +=25
                    if self.man.isJump==True:
                        self.man.isJump=False
                        self.man.jumpCount=10
                        movingDownwards=True
                #print("self.man.x,block.x,movingL,movingR=",self.man.x,block.x,self.man.movingLeft,self.man.movingRight)
                if self.man.movingRight==True and block.x >=self.man.x:
                    self.man.x-=self.man.vel*2
                elif self.man.movingLeft==True and block.x <=self.man.x:
                    #print("WHY DOESN'T IT WORK?")
                    self.man.x+=self.man.vel*2
        ymin=580
        if 630<=self.man.x<=720:
            ymin=650         

        
            #print("self.ymin=",self.ymin)
        if self.man.y <=ymin and self.man.isJump==False and self.onBlock==False:
            self.man.y += 10
        if self.goalBlock.manOnBlock(self.man):
            done=True
            reward=1*0.75
            print("VICTORY")
        for spike in self.spikes:
            if spike.manDown(self.man):
                reward=-1
                print("Game Over")
                done=True
    #move the small mobile white platform
        for b in self.blocks:
            if b.color==(255,255,255):
                if b.x>=460:
                    self.vel=-1
                if b.x <= 380:
                    self.vel=1
                b.x=b.x+2*self.vel
                if b.manOnBlock(self.man):
                    self.man.x=self.man.x+2*self.vel
            #print("b.x=",b.x,"vel=",vel)
    #check coins collected
        for c in self.coins:
            rectA=pygame.Rect(self.man.hitbox)
            rectB=pygame.Rect(c.hitbox)
            if pygame.Rect.colliderect(rectA,rectB):
                self.coins.remove(c)
                reward=reward+(1/6)*0.25

        state=self.render(mode="state_pixels")#self.get_state()
        return state,reward,done,{}
    def get_state(self):
        state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
            pygame.display.get_surface()).astype(np.uint8))))
        return state
    def redraw(self, mode="human"):
        """
        """
    
        self.win.blit(bg, (0,0))
        pygame.draw.rect(self.win, (255,0,0), (10,10, 50, 20))
        pygame.draw.rect(self.win, (0,128,0), (10,10, 50 - (5 * (10 -0.1*self.man.fuelLeft )), 20))
        text = self.font.render('Score: ' + str(score), 1, (0,0,0))
        self.win.blit(text, (390, 10))
        for b in self.blocks:
            b.draw(self.win)
        for s in self.spikes:
            s.draw(self.win)
        for v in self.vacums:
            v.draw(self.win)
        for c in self.coins:
            c.draw(self.win)
        self.goalBlock.draw(self.win)
        self.man.draw(self.win)
        if mode == "rgb_array":
            img= pygame.surfarray.array3d(self.win)
            return img
        else:
    #redRect=(10,10,50,20)
    #pygame.draw.rect(win,(255,0,0),redRect)
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
if __name__ == "__main__":
    run=True
    env=agentPlatformerEnv()
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
        1 left 
        2 right
        3 jump
        4 fly
        5 jump left
        6 jump right
        7 fly left
        8 fly right
        """
        left=False
        right=False
        jump=False 
        fly=False
        if keys[pygame.K_LEFT]:
            left=True
        if keys[pygame.K_RIGHT]:
            right=True
        if keys[pygame.K_SPACE]:
            jump=True
        if keys[pygame.K_UP]:
            fly=True
        ############################
        if left==True:
            if jump==True:
                action=5
            elif fly==True:
                action=7
            else:
                action=1
        elif right==True:
            if jump==True:
                action=6
            elif fly==True:
                action=8
            else:
                action=2
        if jump==True and (left==False and right==False):
            action=3
        if fly==True and (left==False and right==False):
            action=4
        obs, reward, done, info=env.step(action)
        env.render(mode='human')
        totalRew+=reward
        print("total reward=",totalRew)
        if done==True:
            break
        #env.render()
    

