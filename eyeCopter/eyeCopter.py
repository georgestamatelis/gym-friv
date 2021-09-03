from os import fwalk
from numpy.lib.function_base import trim_zeros
import pygame
pygame.init()

win = pygame.display.set_mode((900,700))

assetsPath="/home/georgestamatelis/gym-slitherin/eyeCopter/"
flying = [pygame.image.load(assetsPath+'F1.png'), pygame.image.load(assetsPath+'F2.png'), pygame.image.load(assetsPath+'F3.png'), pygame.image.load(assetsPath+'F4.png'), pygame.image.load(assetsPath+'F5.png')]
bg = pygame.image.load('/home/georgestamatelis/gym-slitherin/eyeCopter/EyeCopterBG.png')
bg = pygame.transform.scale(bg,(900,700))
char = pygame.image.load(assetsPath+'standing.png')
grassPic=pygame.image.load(assetsPath+'grassBG.png')
clock = pygame.time.Clock()

score = 0

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
        self.hitbox = (self.x + 17, self.y + 11, 30, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 15:
            self.walkCount = 0

       
        self.hitbox = (self.x +5, self.y + 11, 54, 52)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)

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
class Diamond:
    def __init__(self,x,y,):
        self.x = x
        self.y = y
        self.img=pygame.image.load(assetsPath+'diamond.png')
        self.hitbox=(self.x,self.y+20,45,25)
    def draw(self,win):
        self.hitbox=(self.x,self.y+20,45,25)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
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
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
        win.blit(self.img,(self.x,self.y))
class Goal:
    def __init__(self,x,y,):
        self.x = x
        self.y = y
        self.fireHeight=0
        self.img=pygame.image.load(assetsPath+'diamond.png')
        self.hitbox=(self.x,self.y+20,45,25)
    def draw(self,win):
             
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
        win.blit(self.img,(self.x,self.y))

def redrawGameWindow():
    win.blit(bg, (0,0))
    win.blit(grassPic,(0,260))
    win.blit(grassPic,(80,260))
    win.blit(grassPic,(720,260))
    win.blit(grassPic,(820,260))

    for b in blocks:
        b.draw(win)
    for c in coins:
        c.draw(win)
    man.draw(win)
    goal.draw(win)
    if pl.active:
        pl.draw(win)
    #redRect=(10,10,50,20)
    #pygame.draw.rect(win,(255,0,0),redRect)
    pygame.display.update()


#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(20, 280, 64,64)
goal = Diamond(840,300)
run = True
blocks=[]
coins=[]
pl=Platform(20,290)
#first two rows no the left
for w in [0,30,60,90,120,150]:
    for h in [350,380]:
        blocks.append(Block(w,h,30,30))

#third row on left
for w in [0,30,60,90,120]:
    blocks.append(Block(w,410,30,30))

#last row on left
for w in [0,30,60,90]:
    blocks.append(Block(w,440,30,30))

#first two rows no the right
for w in [720,750,780,810,840,870]:
    for h in [350,380]:
        blocks.append(Block(w,h,30,30))

#third row on right
for w in [750,780,810,840,870]:
    blocks.append(Block(w,410,30,30))

#last row on right
for w in [780,810,840,870]:
    blocks.append(Block(w,440,30,30))
#now draw the 12 coins
coins.append(Coin(200,250,10))
coins.append(Coin(240,210,10))
coins.append(Coin(280,170,10))
coins.append(Coin(320,130,10))
coins.append(Coin(360,90,10))
coins.append(Coin(400,60,10))
coins.append(Coin(440,60,10))
coins.append(Coin(480,90,10))
coins.append(Coin(520,130,10))
coins.append(Coin(560,170,10))
coins.append(Coin(600,210,10))
coins.append(Coin(640,250,10))

while run:
    clock.tick(27)


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    

    keys = pygame.key.get_pressed()
    #first of all handle gravity
    onBlock=False
    for b in blocks:
        if b.manOnBlock(man):
            onBlock=True
            man.flying=False
    if onBlock==False:
        man.y+=10
    if  keys[pygame.K_LEFT] :
        if onBlock==True:
            man.x-=man.vel*0.25
        else :
            man.x -=man.vel
        man.movingLeft=True
        man.movingRight=False
    elif keys[pygame.K_RIGHT]:
        if onBlock==True:
            man.x+=man.vel*0.25
        else:
            man.x+=man.vel
        man.movingRight=True        
        man.movingLeft=False

    else:
        man.movingLeft=False
        man.movingRight=False
    if keys[pygame.K_UP]:
        man.y-=3*man.vel
        man.flying=True

    #check collision with blocks
    for b in blocks:
        if b.manCollides(man) and onBlock==False:
            if man.movingRight==True:
                man.x-=man.vel 
            elif man.movingLeft==True:
                man.x+=man.vel
            if man.flying==True and man.y<=b.y+b.height:
                man.y+=man.vel
    #check collision with coins
    for c in coins:
        rectA=pygame.Rect(c.hitbox)
        rectB=pygame.Rect(man.hitbox)
        if pygame.Rect.colliderect(rectA,rectB):
            coins.remove(c)
    #check diamong
    rectA=pygame.Rect(goal.hitbox)
    rectB=pygame.Rect(man.hitbox)
    if pygame.Rect.colliderect(rectA,rectB):
        man.hasDiamond=True
        pl.active=True

    if man.hasDiamond==True:
        goal.x=man.x +10
        goal.y = man.y +45
        rectA=pygame.Rect(man.hitbox)
        rectB=pygame.Rect(pl.hitbox)
        if pygame.Rect.colliderect(rectA,rectB):
            print("VICTORY")
            break

    #check bounds
    if man.x <=-60 or man.x >=960:
        print("GAME OVER ")
        break
    if man.y >=800 or man.y<=-90:
        print("GAME OVER")
        break
    redrawGameWindow()

pygame.quit()


