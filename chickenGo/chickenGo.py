from os import fwalk
from numpy.lib.function_base import trim_zeros
import pygame
import random
pygame.init()

win = pygame.display.set_mode((1000,500))
assetsPath="/home/georgestamatelis/gym-slitherin/chickenGo/"
clock = pygame.time.Clock()


class Chicken(object):
    walkRight = [pygame.image.load(assetsPath+'R1.png'), pygame.image.load(assetsPath+'R2.png'), pygame.image.load(assetsPath+'R3.png'), pygame.image.load(assetsPath+'R4.png'), pygame.image.load(assetsPath+'R5.png'), pygame.image.load(assetsPath+'R6.png'), pygame.image.load(assetsPath+'R7.png')]
    walkLeft = [pygame.image.load(assetsPath+'L1.png'), pygame.image.load(assetsPath+'L2.png'), pygame.image.load(assetsPath+'L3.png'), pygame.image.load(assetsPath+'L4.png'), pygame.image.load(assetsPath+'L5.png'), pygame.image.load(assetsPath+'L6.png'), pygame.image.load(assetsPath+'L7.png')]
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel = 15
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
            
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
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
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
class Car(object):
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
        pygame.draw.rect(win,(100,40,0),self.hitbox,0)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
class Car(object):
    def __init__(self,x,y,vel):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 80
        self.cleared=False
        self.vel=vel
        self.hitbox = (self.x, self.y,self.width,self.height)
        self.HP=500
    def draw(self,win):
        self.y+=self.vel

        self.hitbox = (self.x, self.y,self.width,self.height)
        pygame.draw.rect(win, (240,0,255), self.hitbox)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)

def redraw():
    #first draw the background
    pygame.draw.rect(win,(20,200,0),(0,0,150,500))
    pygame.draw.rect(win,(200,200,110),(150,0,20,500))
    pygame.draw.rect(win,(127,127,127),(170,0,230,500))
    pygame.draw.rect(win,(200,200,110),(380,0,20,500))
    pygame.draw.rect(win,(0,70,150),(400,0,150,500))
    pygame.draw.rect(win,(200,200,110),(550,0,20,500))
    pygame.draw.rect(win,(127,127,127),(570,0,230,500))
    pygame.draw.rect(win,(200,200,110),(790,0,20,500))
    pygame.draw.rect(win,(20,200,0),(810,0,200,500))
    for c in cars:
        c.draw(win)
    for c in logs:
        c.draw(win)
    for c in chickens:
        c.draw(win)
    pygame.display.update()
cars=[]
logs=[]
chickens=[]
chickens.append(Chicken(15,25))
c=chickens[0]
run=True
totalTimeSteps=0
while run:
    clock.tick(27)
    totalTimeSteps+=1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and c.x > 0:
        c.x-=5
        c.movingLeft=True
        c.movingRight=False
        c.standing=False
    elif keys[pygame.K_RIGHT] and c.x <= 990:
        c.x+=5
        c.movingLeft=False
        c.movingRight=True
        c.standing=False
    else:
        c.movingLeft=False
        c.movingRight=False
        c.standing=True
    if keys[pygame.K_UP] and c.y >=10:
        c.y-=5
        c.movingRight=True
        c.movingLeft=False
        c.standing=False

    if keys[pygame.K_DOWN] and c.y <=490:
        c.y+=5
        c.movingRight=True
        c.movingLeft=False
        c.standing=False
    if totalTimeSteps %80 ==0:
        logs.append(log(420,520,-2))
        logs.append(log(490,-20,2))
    if totalTimeSteps %100==0 or totalTimeSteps ==50 :
        cars.append(Car(190,-20,7))
    if totalTimeSteps %70==0 or totalTimeSteps ==30  :
        cars.append(Car(250,-20,7))
    if totalTimeSteps %120==0 or totalTimeSteps == 40 :
        cars.append(Car(315,-20,7))
    if totalTimeSteps %90==0 and random.random()<=0.8:
        cars.append(Car(570,520,-7))
    if totalTimeSteps %110==0 and random.random()<=0.6:
        cars.append(Car(570+60,520,-7))
    if totalTimeSteps %80==0 and random.random()<=0.8:
        cars.append(Car(570+120,520,-7))
    onLog=False
    for l in logs:
        rectA=pygame.Rect(l.hitbox)
        rectB=pygame.Rect(c.hitbox)
        #print(rectB)
        #print(pygame.Rect.colliderect(rectA,rectB))
        if pygame.Rect.colliderect(rectA,rectB)==True:
            c.y+=l.vel
            onLog=True
            break
        if l.y<=-80:
            logs.remove(l)
    if 390<=c.x<=506 and onLog==False:
        print("DROWN")
        pygame.quit()
        exit()
    if c.y <=-30 or c.y >=530:
        print("OUT OF BOUNDS")
        pygame.quit()
        exit()
    for car in cars:
        rectA=pygame.Rect(car.hitbox)
        rectB=pygame.Rect(c.hitbox)
        #print(rectB)
        #print(pygame.Rect.colliderect(rectA,rectB))
        if pygame.Rect.colliderect(rectA,rectB)==True:
            print("COLISSION GAME OVER")
            pygame.quit()
            exit()
        if car.y >=540 or car.y <=-40:
            cars.remove(car)
    if c.x >=820:
        print("VICTORY")
        pygame.quit()
        exit()
    redraw()