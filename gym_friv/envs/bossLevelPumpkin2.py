
import pygame
import random

"""
    This environment, is the same as boss level pumpkin one. The only difference is that
the boss has a little more health and moves slightly faster, the cats move downwards 
a  little faster and they last for a little longer. The player causes less damage 
to the boss.

"""
#gym imports
import gym
from gym import spaces
from gym.envs.box2d.car_dynamics import Car
from gym.utils import seeding, EzPickle
from gym.envs.classic_control import rendering

#cv2 for resizing  observations
import cv2
#for fliping state image
import numpy as np 

STATE_W = 100  # less than Atari 160x192
STATE_H = 100
FPS =1 #pygame animation deals with FPS

assetsPath="bossLevelPumpkin/"
walkRight = [pygame.image.load(assetsPath+'R1.png'), pygame.image.load(assetsPath+'R2.png'), pygame.image.load(assetsPath+'R3.png'), pygame.image.load(assetsPath+'R4.png'), pygame.image.load(assetsPath+'R5.png'), pygame.image.load(assetsPath+'R6.png'), pygame.image.load(assetsPath+'R7.png'), pygame.image.load(assetsPath+'R8.png'), pygame.image.load(assetsPath+'R9.png')]
walkLeft = [pygame.image.load(assetsPath+'L1.png'), pygame.image.load(assetsPath+'L2.png'), pygame.image.load(assetsPath+'L3.png'), pygame.image.load(assetsPath+'L4.png'), pygame.image.load(assetsPath+'L5.png'), pygame.image.load(assetsPath+'L6.png'), pygame.image.load(assetsPath+'L7.png'), pygame.image.load(assetsPath+'L8.png'), pygame.image.load(assetsPath+'L9.png')]
bg = pygame.image.load(assetsPath+'bg.png')
bg = pygame.transform.scale(bg,(700,700))

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 30, 52)
        self.movingRight=True
        self.movingLeft=False
        self.HP=100
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
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
               
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x 
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing #+-1
        self.vel=16*facing
        self.hitbox=(self.x-self.radius,self.y-self.radius,2*self.radius,2*self.radius)
    def draw(self,win):
        self.hitbox=(self.x-self.radius,self.y-self.radius,2*self.radius,2*self.radius)
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius) #,1 for not filled
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

        
class Enemy(object):
    img=pygame.image.load(assetsPath+"ghost.png")
    def __init__(self,x,y):
        self.x=x
        self.y=y 
        self.hitbox = (self.x +25 , self.y+25, 110,105)
        self.vel=4
        self.HP=750

    def draw(self,win):
        if self.x >=560:
            self.vel=-4
        if self.x<=-60:
            self.vel=4
            
        self.x=self.x+self.vel
        self.hitbox = (self.x +25 , self.y+25, 110,105)
        win.blit(self.img,(self.x,self.y))
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
class evilcat(object):
    img=pygame.image.load(assetsPath+"evilCat.png")
    def __init__(self,x,y):
        self.x=x
        self.y=y 
        self.hitbox = (self.x+2 , self.y+5, 92,85)

        self.vel=17
        self.lifeSpan=100
    def getHitbox(self):
        return self.hitbox
    def draw(self,win):
        self.lifeSpan=self.lifeSpan-1
        if self.y <=520:
            self.y=self.y+self.vel
        self.hitbox = (self.x+2 , self.y+5, 92,85)
        win.blit(self.img,(self.x,self.y))
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)


class bossLevelPumpkin2(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array", "state_pixels"],
        "video.frames_per_second": FPS,
    }

    def __init__(self, verbose=1):
        pygame.init()
        self.win = pygame.display.set_mode((700,700))
        self.viewer=None
        pygame.display.set_caption("Boss Level Pumpkin")
        """
        actions are 
        0 do nothing 
        1 L
        2 R 
        3 Shoot
        4 Shoot  & L
        5 Shoot & R
        6 J
        7 J & L
        8 J & R
        9 J & Shoot
        10 J & Shoot & L
        11 J & Shoot & R
        
        """
        self.action_space=spaces.Discrete(12)
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(STATE_H,STATE_W, 3), dtype=np.uint8
        )
    def reset(self):
        """
         INTIALISE ENEMY, PLAYER , LISTS OF OBJECTS AND RESET COUNTERS
        """
        pygame.font.init()
        self.font = pygame.font.SysFont('comicsans', 30, True)
        self.man = player(50, 560, 64,64)
        self.ghost = Enemy(random.randrange(0,400),50)
        self.ghost.vel=random.choice([-4.5,4.5,-5,5,-4.75,4.75,-5.2,5.2])
        self.bullets=[]
        self.evilcats=[]
        self.shootReset=0
        self.catReset=0
        observation=self.render(mode="state_pixels")#self.get_state()
        self.render(mode='human')
        #state = np.fliplr(np.flip(np.rot90(pygame.surfarray.array3d(
        #     pygame.display.get_surface()).astype(np.uint8))))
        return observation
    def step(self,action):

        #animate the bullets
        reward=0
        done = False
        for b in self.bullets:
            if b.y <=5:
                self.bullets.pop(self.bullets.index(b))
            else:
                b.y=b.y -20
                rectA=pygame.Rect(b.hitbox)
                rectB=pygame.Rect(self.ghost.hitbox)
                if pygame.Rect.colliderect(rectA,rectB)==True:
                    self.ghost.HP=self.ghost.HP-20
                    reward = reward + 20/750
                    if self.ghost.HP <=0:
                        print("VICTORY")   
                        done=True
                    self.bullets.pop(self.bullets.index(b))

        #animate the cats
        if self.catReset >=16:
            self.catReset=0
        if self.catReset>0:
            self.catReset+=1
        if self.catReset==0 and random.randrange(0,1)<=0.65:
            #c=evilcat(ghost.x,ghost.y)
            self.evilcats.append(evilcat(self.ghost.x,self.ghost.y))
            self.catReset=1
        for c in self.evilcats:
            if c.lifeSpan<0:
                self.evilcats.pop(self.evilcats.index(c))
            else:
                hitbox=c.hitbox
                rectA=pygame.Rect(hitbox)
                rectB=pygame.Rect(self.man.hitbox)
                if pygame.Rect.colliderect(rectA,rectB)==True:
                    self.man.HP=self.man.HP-25
                    reward=reward - 25/100

                    if self.man.HP <=0:
                        done=True
                        print("GAME OVER")
                    self.evilcats.pop(self.evilcats.index(c))
        """
            actions are 
            0 do nothing 
            1 L
            2 R 
            3 Shoot
            4 Shoot  & L
            5 Shoot & R
            6 J
            7 J & L
            8 J & R
            9 J & Shoot
            10 J & Shoot & L
            11 J & Shoot & R
        
        """
        if self.shootReset>=10:
            self.shootReset=0
        if self.shootReset >0:
            self.shootReset+=1
        if action in [3,4,5,9,10,11]:
            if self.shootReset <=0 and len(self.bullets)<=15:
                facing=1
                bullet=projectile(
                        round(self.man.x+self.man.width+5),round(self.man.y+self.man.height//2),15,(0,0.2,0.6),facing)
                self.bullets.append(bullet)
                self.shootReset+=1
                self.shooting=True
        if action in [1,4,7,10] and self.man.x >=10:
            self.man.x -= self.man.vel
            self.man.left = True
            self.man.right = False
            self.man.standing = False
            self.man.movingRight=False
            self.man.movingLeft=True
        if action in [2,5,8,11] and self.man.x <=650 - self.man.width - self.man.vel :
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
        if not(self.man.isJump) :
            if action in [6,7,8,9,10,11]:
                self.man.isJump = True
                self.man.right = False
                self.man.left = False
                self.man.walkCount = 0
                self.movingDownwards=False
        else:
            if self.man.jumpCount >= -10:
                neg = 1
                if self.man.jumpCount < 0:
                    neg = -1
                    
                self.man.y -= (self.man.jumpCount ** 2) * 0.5 * neg
                self.man.jumpCount -= 1
            else:
                self.movingDownwards=True
                self.man.isJump = False
                self.man.jumpCount = 10
        state=self.render(mode="state_pixels")#self.get_state()
        self.render(mode='human')
        
        return state,reward,done,{}
        


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
            img=cv2.resize(img,(STATE_H,STATE_W))
            return img
    def redraw(self, mode="human"):
        self.win.blit(bg, (0,0))
        textsurface = self.font.render('ENEMY', False, (0, 0, 0))
        textsurface2 = self.font.render('PLAYER', False, (0, 0, 0))

        self.win.blit(textsurface,(20,0))
        self.win.blit(textsurface2,(520,0))

        pygame.draw.rect(self.win, (0,255.0,0), (10,40,0.4*self.ghost.HP, 25))
        pygame.draw.rect(self.win, (0,255.0,0), (450,40,2*self.man.HP, 25))

        self.man.draw(self.win)
        for b in self.bullets:
            b.draw(self.win)
        for c in self.evilcats:
            c.draw(self.win)
        self.ghost.draw(self.win)
        pygame.display.update()
#main function for user play
#just type python3 <path to file> /eyeCopterEnv1.py to play as a human agent
if __name__ == "__main__":
    run=True
    env=bossLevelPumpkin2()
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
            1 L
            2 R 
            3 Shoot
            4 Shoot  & L
            5 Shoot & R
            6 J
            7 J & L
            8 J & R
            9 J & Shoot
            10 J & Shoot & L
            11 J & Shoot & R
        
        """
        jumping=False 
        shooting=False
        left=False
        right=False
        if keys[pygame.K_LEFT]:
            left=True
        if keys[pygame.K_RIGHT]:
            right=True
        if keys[pygame.K_UP]:
            jumping=True
        if keys[pygame.K_x]:
            shooting=True
        #determine action
        if left==True:
            if jumping==True and shooting==True:
                action=10
            if jumping==True and shooting==False:
                action = 7
            if jumping==False and shooting==True:
                action=4
            if jumping==False and shooting==False:
                action=1
        if right==True:
            if jumping==True and shooting==True:
                action=11
            if jumping==True and shooting==False:
                action = 8
            if jumping==False and shooting==True:
                action=5
            if jumping==False and shooting==False:
                action=2
        if right==False and left==False:
            if jumping==True and shooting==True:
                action=9
            if jumping==True and shooting==False:
                action=6
            if jumping==False and shooting==True:
                action=3
        obs, reward, done, info=env.step(action)
        env.render(mode='human')
        totalRew+=reward
        print("total reward=",totalRew)
        if done==True:
            break