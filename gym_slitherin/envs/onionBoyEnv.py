from os import fwalk
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
#in here there are the classes used by the environment
from gym_slitherin.envs.onionClasses import *

FPS=27


pygame.init()


pygame.display.set_caption("onionBoy")



STATE_W = 130  # less than Atari 160x192
STATE_H = 130
"""
the rewards are given as followed
0.1/num enemies for killing an enemy
0.1/num flying enemies for killing a flying enemy
0.1 for killing the ball (To kill the ball you need to hop on it twice)
0.1/num of coins for collection a coint
0.6 for finishing
"""
class onionBoyEnv(gym.Env, EzPickle):
    metadata = {
        "render.modes": ["human", "rgb_array", "state_pixels"],
        "video.frames_per_second": FPS,
    }

    def __init__(self, verbose=1):
        """
        
        """
        pygame.init()

        self.win = pygame.display.set_mode((600,500))

        self.viewer=None
        """
        actions are
        0 nothing
        1 left 
        2 right
        3 jump
        4 jump left
        5 jump right
        """
        self.action_space=spaces.Discrete(6)
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(STATE_H,STATE_W, 3), dtype=np.uint8
        )
        self.maxTimeSteps=5000
    def _destroy(self):
        """
        """

    def reset(self):
        """
        """
        self.timeSteps=0
        self._destroy()
        self.font = pygame.font.SysFont('comicsans', 30, True)
        self.man = player(50, 200, 64,64)

        self.cameraX=self.man.x-200
        self.run = True
        self.blocks=[]
        self.spikes=[]
        self.coins=[]      
        self.enemies=[]
        self.flyingEnemies=[]
        self.coins=[]
        self.WoodenBlocks=[]
        self.boxes=[]
        self.balls=[]
        self.platforms=[]
        self.platforms.append(platform(1485,300,64,64))
        self.ball=Ball(3150,240,64,140,3700)
        self.balls.append(self.ball)
        self.blocks.append(Block(-350,360,6350,300,hard=True))

        self.blocks.append(Block(-350,320,1150+230+350,80,hard=True))

        self.blocks.append(Block(200,200,200,160))
        self.coins.append(Coin(400,180,10))
        self.coins.append(Coin(430,150,10))
        self.coins.append(Coin(450,120,20))
        self.coins.append(Coin(460,150,10))
        self.coins.append(Coin(490,180,10))

        self.blocks.append(Block(500,190,400,170,hard=True))
        self.boxes.append(Box(550,100,15))
        self.boxes.append(Box(580,100,15))
        self.boxes.append(Box(610,100,15))

        self.coins.append(Coin(660,60,10))
        self.coins.append(Coin(690,60,10))
        self.coins.append(Coin(720,60,10))
        self.coins.append(Coin(660,35,10))
        self.coins.append(Coin(690,35,10))
        self.coins.append(Coin(720,35,10))

        self.blocks.append(Block(900,220,200,140,hard=True))
        self.coins.append(Coin(950,100,20))
        self.blocks.append(Block(1100,250,150,110,hard=True))

        for x in [1420,1450,1480,1510,1540,1570]:
            for y in [190,160,130,100,70,40]:
                self.coins.append(Coin(x,y,10))

        self.blocks.append(Block(1600,320,600,80,hard=True))
        self.WoodenBlocks.append(WoodenBlock(1660,220,75,100))
        self.flyingEnemies.append(flyingEnemy(1660,150,50,25,230))

        self.blocks.append(Block(1800,195,300,140,hard=False))
        for w in [2170,2200,2230,2260]:
            for h in [150,120]:
                self.coins.append(Coin(w,h,10))
#coins.append(Coin(2150,160,10))
        self.blocks.append(Block(2200,330,20,70,hard=True)) 
        self.blocks.append(Block(2220,340,20,70,hard=True))
        self.blocks.append(Block(2240,350,20,70,hard=True))

        self.blocks.append(Block(2400,320,200,80,hard=True))
        self.blocks.append(Block(2600,300,200,280,hard=True))
        self.blocks.append(Block(2800,280,300,280,hard=True))
        for w in [2850,2890,2930,2970]:
            self.boxes.append(Box(w,190,20))
        for w in [3010,3040,3070,3100]:
            self.coins.append(Coin(w,190,10))
            self.coins.append(Coin(w,160,10))


        self.blocks.append(Block(3100,300,50,280,hard=True))
        self.blocks.append(Block(3150,320,1000,280,hard=True))

        self.WoodenBlocks.append(WoodenBlock(3750,225,75,95))
        self.enemies.append(enemy(3800,200,50,50,3950))

        self.WoodenBlocks.append(WoodenBlock(4000,250,75,70))

        self.blocks.append(Block(4450,300,1000,140,hard=True))
        e=enemy(4150,300,50,50,4450)
        self.enemies.append(e)
        e=enemy(4150,300,50,50,4450)
        e.x=4233
        self.enemies.append(e)
        e=enemy(4150,300,50,50,4450)
        e.x=4317
        self.enemies.append(e)
        for w in [4510,4550,4590,4630]:
            self.boxes.append(Box(w,200,20))
        self.WoodenBlocks.append(WoodenBlock(4700,230,75,70))
        self.flyingEnemies.append(flyingEnemy(4700,150,50,25,250))
        self.WoodenBlocks.append(WoodenBlock(4900,205,75,95))
        self.flyingEnemies.append(flyingEnemy(5060,160,50,25,80))
        self.coins.append(Coin(5100,90,20))

        self.blocks.append(Block(5450,100,1000,500,hard=True))

        for w in [5200,5230,5270,5300]:
            self.coins.append(Coin(w,170,10))

        self.goalCoin=Coin(5400,220,10,color=(0,255,255))
#blocks.append(Block(1700,130,300,140,hard=False))




#blocks.append(Block(0,140,400,120,hard=True))
#blocks.append(Block(450,140,400,120,hard=True))

        self.onBlock=False

        self.enemies.append(enemy(180,130,50,50,330))

        e=enemy(700,140,50,500,500)
        e.path=[500,1600]
        e.vel=-1.5
        self.enemies.append(e)

        e=enemy(800,140,50,500,500)
        e.path=[500,1600]
        e.vel=-1.5
        self.enemies.append(e)

        e=enemy(850,140,50,500,500)
        e.path=[800,1000]
        e.vel=-1.5
        self.enemies.append(e)

        e=enemy(950,170,50,500,500)
        e.path=[900,1600]
        e.vel=-1.5
        self.enemies.append(e)

        #enemies.append(enemy(800,100,50,500,500))
        #enemies.append(enemy(900,100,50,500,500))
        self.enemies.append(enemy(1800,100,50,50,2000))

        e=enemy(2600,170,150,500,500)
        e.path=[1000,2600]
        e.vel=0
        self.enemies.append(e)

        e=enemy(2800,170,150,500,500)
        e.path=[900,3000]
        e.vel=0
        self.enemies.append(e)

        e=enemy(3100,250,50,50,3500)
        e.path=[3100,3550]
        self.enemies.append(e)
        e=enemy(3200,250,50,50,3500)
        e.path=[3100,3550]
        self.enemies.append(e)

        e=enemy(3300,250,50,50,3500)
        e.path=[3100,3550]
        self.enemies.append(e)

        self.enemies.append(enemy(4900,200,50,50,5600))

        self.maxX=5700
        level=1
        self.ymin=300


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
        4 jump left
        5 jump right
        """
        self.timeSteps+=1
        done=False
        reward=0
        if (action==1 or action==4) and self.man.x > -30:
            self.man.x -= self.man.vel
            self.cameraX-=self.man.vel
            self.man.left = True
            self.man.right = False
            self.man.standing = False
            self.man.movingLeft=True
            self.man.movingRight=False
        elif (action==2 or action==5) :#and man.x < 580 - man.width - man.vel:
            self.man.x += self.man.vel
            self.cameraX+=self.man.vel
            self.man.right = True
            self.man.left = False 
            self.man.standing = False
            self.man.movingLeft=False
            self.man.movingRight=True

        else:
            self.man.movingLeft=False
            self.man.movingRight=False
            self.man.standing = True
            self.man.walkCount = 0
        #print("fookin action=",action)
        if not(self.man.isJump):
            if (action==3 or action==4 or action==5) and self.man.y >=20 and (self.onBlock==True or self.man.y>=300):
                self.man.isJump = True
                self.man.right = False
                self.man.left = False
                self.man.walkCount = 0

        else:
            if self.man.jumpCount >= 0 :
                neg = 1
                if self.man.jumpCount < 0:
                    neg = -1
                self.man.y -= (self.man.jumpCount ** 2) *0.65* neg
                self.man.jumpCount -= 1
            else:
                self.man.isJump = False
                self.man.jumpCount = 8



        #check if man is on block to cancell out gravity
        self.onBlock=False
        for block in self.blocks:
            if block.manOnBlock(self.man): 
                self.onBlock=True
                #if self.man.y !=260:
                #    print("man on fookin block",self.man.y)
        for wb in self.WoodenBlocks:
            if wb.manOnBlock(self.man):
                self.onBlock=True
        for b in self.boxes:
            if b.manOnBlock(self.man):
                self.onBlock=True
        #gravity
        if self.onBlock==False and self.man.y<self.ymin and self.man.isJump==False:
            self.man.y+=10
                
        for e in self.enemies:
            rectA=pygame.Rect(self.man.hitbox)
            rectB=pygame.Rect(e.hitbox)
            if pygame.Rect.colliderect(rectA,rectB):
                if (self.man.y <=e.y-0.5*self.man.hitbox[3])  and self.man.isJump==False:
                    print("Enemy dead")
                    self.enemies.remove(e)
                    reward+=0.1/16
                else:
                    print("GAME OVER")
                    reward=-1
                    done=True
        for e in self.flyingEnemies:
            rectA=pygame.Rect(self.man.hitbox)
            rectB=pygame.Rect(e.hitbox)
            if pygame.Rect.colliderect(rectA,rectB):
                if (self.man.y <=e.y-0.5*self.man.hitbox[3])  and self.man.isJump==False and self.onBlock==False:
                    print("Enemy dead")
                    self.flyingEnemies.remove(e)
                    reward+=0.1/3
                else:
                    print("GAME OVER")
                    reward=-1
                    done=True
        for b in self.blocks:
            if b.hard==True:
                if b.manCollides(self.man):
                    if self.man.movingRight==True and b.x >=self.man.x:
                        self.man.x-=self.man.vel*2
                        self.cameraX-=self.man.vel*2
                    elif self.man.movingLeft==True and b.x <=self.man.x:
                        self.man.x+=self.man.vel*2
                        self.cameraX+=self.man.vel*2
        for wb in self.WoodenBlocks:
            if wb.manCollides(self.man):
                if self.man.movingRight==True and wb.x >=self.man.x:
                    self.man.x-=self.man.vel*2
                    self.cameraX-=self.man.vel*2
                elif self.man.movingLeft==True and wb.x <=self.man.x:
                    self.man.x+=self.man.vel*2
                    self.cameraX+=self.man.vel*2
        for b in self.boxes:
            if b.manCollides(self.man):
                if not self.onBlock and (self.man.isJump==True): 
                    self.man.isJump=False
                    self.man.jumpCount=8
                    self.movingDownwards=True
                if self.man.movingRight==True and b.x >=self.man.x:
                    self.man.x-=self.man.vel*2
                    self.cameraX-=self.man.vel*2
                elif self.man.movingLeft==True and b.x <=self.man.x:
                    self.man.x+=self.man.vel*2
                    self.cameraX+=self.man.vel*2
            

        if self.maxX - self.man.width - self.man.vel<=self.man.x<=self.maxX - self.man.width - self.man.vel+10:
            self.man.x-=self.man.vel

        """
        user animation is okk now time to handle enemy animation
        """
        for e in self.enemies:
            enemyOnBlock=False
            for b in self.blocks:
                if b.manOnBlock(e):
                    enemyOnBlock=True
                if b.manCollides(e):
                    e.vel=e.vel*(-1)
        #if e.x >=500:
        #    print("ON BLOCK=",enemyOnBlock)
            if enemyOnBlock==False :
                e.y+=10
            if e.vel==0 and self.man.x >=2000:
                e.vel=-1.5
        """
        time to remove coins (and ad score)
        """
        for c in self.coins:
            rectA=pygame.Rect(self.man.hitbox)
            rectB=pygame.Rect(c.hitbox)
            if pygame.Rect.colliderect(rectA,rectB):
                self.coins.remove(c)
                reward+=0.1/69
        """
        finaly before the end of the loop check end condition
        """
        rectA=pygame.Rect(self.man.hitbox)
        rectB=pygame.Rect(self.goalCoin.hitbox)
        if pygame.Rect.colliderect(rectA,rectB):
            print("VICTORY")
            reward+=0.6
            done=True
            
        """
        now deal with ball collision
        """
        for ball in self.balls:
            rectB=pygame.Rect(ball.hitbox)
            if pygame.Rect.colliderect(rectA,rectB):
                if self.man.hitbox[1]<=ball.hitbox[1]-self.man.hitbox[3]/2:
                    if abs(ball.vel)==3.5*4:
                        self.balls.remove(ball)
                        reward+=0.1
                    else:
                        ball.vel=ball.vel*4
                        ball.x+=ball.vel*5
                        self.man.y-=100
                        break
                else:
                    print("GAME OVER")
                    #pygame.quit()
                    reward=-1
                    done=True
            if abs(ball.vel)==3.5*4:
                for e in self.enemies:
                    rectA=pygame.Rect(e.hitbox)
                    if pygame.Rect.colliderect(rectA,rectB):
                        self.enemies.remove(e)
                        reward+=0.1/13
            for pl in self.platforms:
                rectA=pygame.Rect(self.man.hitbox)
                rectB=pygame.Rect(pl.hitbox)
                if pygame.Rect.colliderect(rectA,rectB):
                    #man.y-=200
                    self.man.jumpCount=11
                    self.man.y-=20
                    self.man.isJump=True
                    pl.active=True
        if self.timeSteps >self.maxTimeSteps:
            done=True
            reward=-1
            print("time run out")
        state=self.render(mode="state_pixels")#self.get_state()
        return state,reward,done,{}
    def get_state(self):
        state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
            pygame.display.get_surface()).astype(np.uint8))))
        return state
    def redraw(self, mode="human"):
        self.win.blit(bg, (bgx,bgy))
        text=str(self.maxTimeSteps-self.timeSteps)
        textsurface = self.font.render(text, False, (0, 0, 0))

        self.win.blit(textsurface,(25,25))

        for b in self.blocks:
            b.draw(self.win,self)
        for e in self.enemies:
            e.draw(self.win,self)
        for fe in self.flyingEnemies:
            fe.draw(self.win,self)
        for wb in self.WoodenBlocks:
            wb.draw(self.win,self)
        for b in self.boxes:
            b.draw(self.win,self)
        for c in self.coins:
            c.draw(self.win,self)
        for b in self.balls:
            b.draw(self.win,self)
        for pl in self.platforms:
            pl.draw(self.win,self)
        self.goalCoin.draw(self.win,self)
        self.man.draw(self.win,self)
    #pygame.draw.rect(win,(255,0,0),redRect)
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
    env=onionBoyEnv()
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
        5 jump left
        6 jump right
        """
        left=False
        right=False
        jump=False 
        if keys[pygame.K_LEFT]:
            left=True
        if keys[pygame.K_RIGHT]:
            right=True
        if keys[pygame.K_UP]:
            jump=True
        ############################
        if left==True:
            if jump==True:
                action=4
            else:
                action=1
        elif right==True:
            if jump==True:
                action=5
            else:
                action=2
        if jump==True and (left==False and right==False):
            action=3
        obs, reward, done, info=env.step(action)
        env.render(mode='human')
        totalRew+=reward
        print("total reward=",totalRew)
        if done==True:
            break
        #env.render()
    

