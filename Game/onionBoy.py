
from os import fwalk
from numpy.lib.function_base import trim_zeros
import pygame
pygame.init()

win = pygame.display.set_mode((600,500))

pygame.display.set_caption("onionBoy")

assetsPath="/home/georgestamatelis/gym-slitherin/Game/assets/"
walkRight = [pygame.image.load(assetsPath+'R1.png'), pygame.image.load(assetsPath+'R2.png'), pygame.image.load(assetsPath+'R3.png'), pygame.image.load(assetsPath+'R4.png'), pygame.image.load(assetsPath+'R5.png'), pygame.image.load(assetsPath+'R6.png'), pygame.image.load(assetsPath+'R7.png'), pygame.image.load(assetsPath+'R8.png'), pygame.image.load(assetsPath+'R9.png')]
walkLeft = [pygame.image.load(assetsPath+'L1.png'), pygame.image.load(assetsPath+'L2.png'), pygame.image.load(assetsPath+'L3.png'), pygame.image.load(assetsPath+'L4.png'), pygame.image.load(assetsPath+'L5.png'), pygame.image.load(assetsPath+'L6.png'), pygame.image.load(assetsPath+'L7.png'), pygame.image.load(assetsPath+'L8.png'), pygame.image.load(assetsPath+'L9.png')]
bg = pygame.image.load(assetsPath+'onionBoyBG2.png')
bg = pygame.transform.scale(bg,(600,500))
bgx=0
bgy=0
char = pygame.image.load(assetsPath+'standing.png')

clock = pygame.time.Clock()

score = 0

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
        self.jumpCount = 8
        self.standing = True
        self.flying = False
        self.fuelLeft=100
        self.hitbox = (self.x +7, self.y + 11, 48, 52)
        self.movingRight=True
        self.movingLeft=False

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x-cameraX,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x-cameraX,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x-cameraX, self.y))
            else:
                win.blit(walkLeft[0], (self.x-cameraX, self.y))
        self.hitbox = (self.x + 7-cameraX, self.y + 11,48, 52)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
class WoodenBlock(object):
    def __init__(self,x,y,width,height,color=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color=color
        self.hitbox = (self.x, self.y,self.width,self.height)
    def draw(self,win):
        self.hitbox = (self.x-cameraX, self.y,self.width,self.height)
        pygame.draw.rect(win, (100,40,0), self.hitbox)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
    def manOnBlock(self,man):
        rectA=pygame.Rect(self.hitbox)
        rectB=pygame.Rect(man.hitbox)
        #print(rectB)
        #print(pygame.Rect.colliderect(rectA,rectB))
        if pygame.Rect.colliderect(rectA,rectB)==True:
            if self.y>=man.hitbox[1] +2*man.hitbox[3]//3:
                return True

        #print(pygame.Rect.collidelistall(self.hitbox))
        return False
    def manCollides(self,man):#a collision happened but man is not above the block
        rectA=pygame.Rect(self.hitbox)
        rectB=pygame.Rect(man.hitbox)
        if self.manOnBlock(man):
            return False
        return pygame.Rect.colliderect(rectA,rectB)
class Block(object):
    def __init__(self,x,y,width,height,color=(0,0,0),hard=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color=color
        self.hitbox = (self.x, self.y,self.width,self.height)
        self.img=pygame.image.load(assetsPath+"onionBlock.png")
        self.img=pygame.transform.scale(self.img,(width,height))
        self.hard=hard

    def draw(self,win):
        self.hitbox = (self.x-cameraX, self.y,self.width,self.height)
        win.blit(self.img,(self.x-cameraX,self.y))
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
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
        #if self.x==500 and man.x >=890 and man.x <=920:
        #    print("foooook",self.manOnBlock(man))
        if self.manOnBlock(man):
            return False
        
        return pygame.Rect.colliderect(rectA,rectB)

class enemy(object):
    walkRight = [pygame.image.load(assetsPath+'RE1.png'), pygame.image.load(assetsPath+'RE2.png'), pygame.image.load(assetsPath+'RE3.png'), pygame.image.load(assetsPath+'RE4.png'), pygame.image.load(assetsPath+'RE5.png'), pygame.image.load(assetsPath+'RE6.png'), pygame.image.load(assetsPath+'RE7.png'), pygame.image.load(assetsPath+'RE8.png'), pygame.image.load(assetsPath+'RE9.png')]
    walkLeft = [pygame.image.load(assetsPath+'LE1.png'), pygame.image.load(assetsPath+'LE2.png'), pygame.image.load(assetsPath+'LE3.png'), pygame.image.load(assetsPath+'LE4.png'), pygame.image.load(assetsPath+'LE5.png'), pygame.image.load(assetsPath+'LE6.png'), pygame.image.load(assetsPath+'LE7.png'), pygame.image.load(assetsPath+'LE8.png'), pygame.image.load(assetsPath+'LE9.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y-12
        #self.y=self.y
        self.width = width
        self.height = height
        if end >  x:
            self.path = [x, end]
        else:
            self.path= [end,x]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 4, self.y, 45, 60)

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x-cameraX,self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x-cameraX,self.y))
            self.walkCount += 1
        self.hitbox = (self.x + 4-cameraX, self.y, 45, 60)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
class Ball(object):
    walkRight = [pygame.image.load(assetsPath+'RB1.png'), pygame.image.load(assetsPath+'RB2.png'), pygame.image.load(assetsPath+'RB3.png'), pygame.image.load(assetsPath+'RB4.png'), pygame.image.load(assetsPath+'RB5.png'), pygame.image.load(assetsPath+'RB6.png'), pygame.image.load(assetsPath+'RB7.png')]
    walkLeft = [pygame.image.load(assetsPath+'LB1.png'), pygame.image.load(assetsPath+'LB2.png'), pygame.image.load(assetsPath+'LB3.png'), pygame.image.load(assetsPath+'LB4.png'), pygame.image.load(assetsPath+'LB5.png'), pygame.image.load(assetsPath+'LB6.png'), pygame.image.load(assetsPath+'LB7.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y=y
        self.width = width
        self.height = height
        if end >  x:
            self.path = [x, end]
        else:
            self.path= [end,x]
        self.walkCount = 0
        self.vel = 3.5
        self.hitbox = (self.x + 4, self.y+35, self.width, 60)

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 21:
            self.walkCount = 0
            
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x-cameraX,self.y))
            self.walkCount += 1
            self.hitbox = (self.x + 4-cameraX, self.y+35, self.width, 60)
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x-cameraX,self.y))
            self.walkCount += 1
            self.hitbox = (self.x + 34-cameraX, self.y+35, self.width, 60)

        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def hit(self):
        print("hit")
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
class flyingEnemy(object):
    
    images=[pygame.image.load(assetsPath+"UP1.png"),pygame.image.load(assetsPath+"UP2.png"),pygame.image.load(assetsPath+"UP3.png")]
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if end >  y:
            self.path = [y, end]
        else:
            self.path= [end,y]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 24, self.y, 35, 60)

    def draw(self, win):
        self.move()
        
        if self.walkCount  >= 3:
            self.walkCount = 0
        
        if self.vel > 0:
            win.blit(self.images[self.walkCount], (self.x-cameraX,self.y))
            self.walkCount += 1
        else:
            win.blit(self.images[self.walkCount], (self.x-cameraX,self.y))
            self.walkCount += 1
        
        self.hitbox = (self.x + 24-cameraX, self.y, 35, 60)
        #pygame.draw.rect(win,(240,0,255),self.hitbox)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def hit(self):
        print("hit")
    def move(self):
        if self.vel > 0:
            if self.y < self.path[1] + self.vel:
                self.y += self.vel
                self.walkCount+=1
            else:
                self.vel = self.vel * -1
                self.y += self.vel
                self.walkCount = 0
        else:
            if self.y > self.path[0] - self.vel:
                self.y += self.vel
                self.walkCount+=1
            else:
                self.vel = self.vel * -1
                self.y += self.vel
                self.walkCount = 0
class platform(object):
    
    images=[pygame.image.load(assetsPath+"PL1.png"),pygame.image.load(assetsPath+"PL2.png"),pygame.image.load(assetsPath+"PL3.png"),pygame.image.load(assetsPath+"PL2.png"),pygame.image.load(assetsPath+"PL1.png")]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active=False
        self.walkCount = 0
        self.hitbox = (self.x + 24, self.y+25, 35, 31)

    def draw(self, win):
        
        if self.walkCount  >= len(self.images):
            self.walkCount = 0
            self.active=False
        if self.active==True:
            win.blit(self.images[self.walkCount], (self.x-cameraX,self.y))
            self.walkCount += 1
        else:
            win.blit(self.images[0],(self.x-cameraX,self.y))
        self.hitbox = (self.x + 24-cameraX, self.y+25, 35, 31)
        #pygame.draw.rect(win,(240,0,255),self.hitbox)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def hit(self):
        print("hit")
  
class Coin(object):
    def __init__(self, x, y,radius,color=(200,150,0)):
        self.x = x
        self.y = y
        self.radius=radius
        self.walkCount = 0
        self.vel = 3
        self.radius=radius
        self.color=color
        self.hitbox = (self.x -self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)

    def draw(self, win):
        self.hitbox = (self.x -self.radius-cameraX, self.y-self.radius, 2*self.radius, 2*self.radius)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        pygame.draw.circle(win,self.color,(self.x-cameraX,self.y),self.radius)
class Box(object):
    #we give radius because the box is square
    def __init__(self, x, y,radius,color=(100,40,0)):
        self.x = x
        self.y = y
        self.radius=radius
        self.walkCount = 0
        self.vel = 3
        self.radius=radius
        self.color=color
        self.hitbox = (self.x -self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)

    def draw(self, win):
        self.hitbox = (self.x -self.radius-cameraX, self.y-self.radius, 2*self.radius, 2*self.radius)
        pygame.draw.rect(win,self.color,self.hitbox)
        pygame.draw.rect(win,(0,0,0),self.hitbox,3)
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
        #if self.x==500 and man.x >=890 and man.x <=920:
        #    print("foooook",self.manOnBlock(man))
        if self.manOnBlock(man):
            return False
        
        return pygame.Rect.colliderect(rectA,rectB)

def redrawGameWindow():
    win.blit(bg, (bgx,bgy))
    for b in blocks:
        b.draw(win)
    for e in enemies:
        e.draw(win)
    for fe in flyingEnemies:
        fe.draw(win)
    for wb in WoodenBlocks:
        wb.draw(win)
    for b in boxes:
        b.draw(win)
    for c in coins:
        c.draw(win)
    for b in balls:
        b.draw(win)
    for pl in platforms:
        pl.draw(win)
    goalCoin.draw(win)
    man.draw(win)
    #pygame.draw.rect(win,(255,0,0),redRect)
    pygame.display.update()
def scrollX(screenSurf, offsetX):
    width, height = screenSurf.get_size()
    copySurf = screenSurf.copy()
    screenSurf.blit(copySurf, (offsetX, 0))
    if offsetX < 0:
        screenSurf.blit(copySurf, (width + offsetX, 0), (0, 0, -offsetX, height))
    else:
        screenSurf.blit(copySurf, (0, 0), (width - offsetX, 0, offsetX, height))
    screenSurf=copySurf
    print("please")
    return copySurf
#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(50, 200, 64,64)

cameraX=man.x-200
run = True
blocks=[]
spikes=[]
coins=[]      
enemies=[]
flyingEnemies=[]
coins=[]
WoodenBlocks=[]
boxes=[]
balls=[]
platforms=[]
platforms.append(platform(1485,300,64,64))
ball=Ball(3150,240,64,140,3700)
balls.append(ball)
blocks.append(Block(-350,360,6350,300,hard=True))

blocks.append(Block(-350,320,1150+230+350,80,hard=True))

blocks.append(Block(200,200,200,160))
coins.append(Coin(400,180,10))
coins.append(Coin(430,150,10))
coins.append(Coin(450,120,20))
coins.append(Coin(460,150,10))
coins.append(Coin(490,180,10))

blocks.append(Block(500,190,400,170,hard=True))
boxes.append(Box(550,100,15))
boxes.append(Box(580,100,15))
boxes.append(Box(610,100,15))

coins.append(Coin(660,60,10))
coins.append(Coin(690,60,10))
coins.append(Coin(720,60,10))
coins.append(Coin(660,35,10))
coins.append(Coin(690,35,10))
coins.append(Coin(720,35,10))

blocks.append(Block(900,220,200,140,hard=True))
coins.append(Coin(950,100,20))
blocks.append(Block(1100,250,150,110,hard=True))

for x in [1420,1450,1480,1510,1540,1570]:
    for y in [190,160,130,100,70,40]:
        coins.append(Coin(x,y,10))

blocks.append(Block(1600,320,600,80,hard=True))
WoodenBlocks.append(WoodenBlock(1660,220,75,100))
flyingEnemies.append(flyingEnemy(1660,150,50,25,230))

blocks.append(Block(1800,180,300,140,hard=False))
for w in [2170,2200,2230,2260]:
    for h in [150,120]:
        coins.append(Coin(w,h,10))
#coins.append(Coin(2150,160,10))
blocks.append(Block(2200,330,20,70,hard=True))
blocks.append(Block(2220,340,20,70,hard=True))
blocks.append(Block(2240,350,20,70,hard=True))

blocks.append(Block(2400,320,200,80,hard=True))
blocks.append(Block(2600,300,200,280,hard=True))
blocks.append(Block(2800,280,300,280,hard=True))
for w in [2850,2890,2930,2970]:
    boxes.append(Box(w,190,20))
for w in [3010,3040,3070,3100]:
    coins.append(Coin(w,190,10))
    coins.append(Coin(w,160,10))


blocks.append(Block(3100,300,50,280,hard=True))
blocks.append(Block(3150,320,1000,280,hard=True))

WoodenBlocks.append(WoodenBlock(3750,225,75,95))
enemies.append(enemy(3800,200,50,50,3950))

WoodenBlocks.append(WoodenBlock(4000,250,75,70))

blocks.append(Block(4450,300,1000,140,hard=True))
for w in [4510,4550,4590,4630]:
    boxes.append(Box(w,200,20))
WoodenBlocks.append(WoodenBlock(4700,230,75,70))
flyingEnemies.append(flyingEnemy(4700,150,50,25,250))
WoodenBlocks.append(WoodenBlock(4900,205,75,95))
flyingEnemies.append(flyingEnemy(5060,160,50,25,80))
coins.append(Coin(5100,90,20))

blocks.append(Block(5450,100,1000,500,hard=True))

for w in [5200,5230,5270,5300]:
    coins.append(Coin(w,170,10))

goalCoin=Coin(5400,220,10,color=(0,255,255))
#blocks.append(Block(1700,130,300,140,hard=False))




#blocks.append(Block(0,140,400,120,hard=True))
#blocks.append(Block(450,140,400,120,hard=True))

onBlock=False

enemies.append(enemy(180,130,50,50,330))

e=enemy(700,140,50,500,500)
e.path=[500,1600]
e.vel=-3
enemies.append(e)

e=enemy(800,140,50,500,500)
e.path=[500,1600]
e.vel=-3
enemies.append(e)

e=enemy(850,140,50,500,500)
e.path=[500,1600]
e.vel=-3
enemies.append(e)

e=enemy(950,170,50,500,500)
e.path=[900,1600]
e.vel=-3
enemies.append(e)

#enemies.append(enemy(800,100,50,500,500))
#enemies.append(enemy(900,100,50,500,500))
enemies.append(enemy(1800,100,50,50,2000))

e=enemy(2600,170,150,500,500)
e.path=[1000,2600]
e.vel=-3
e.vel=0
enemies.append(e)

e=enemy(2800,170,150,500,500)
e.path=[900,3000]
e.vel=-3
e.vel=0
enemies.append(e)

e=enemy(3100,250,50,50,3500)
e.path=[3100,3550]
enemies.append(e)
e=enemy(3200,250,50,50,3500)
e.path=[3100,3550]
enemies.append(e)

e=enemy(3300,250,50,50,3500)
e.path=[3100,3550]
enemies.append(e)

enemies.append(enemy(4900,200,50,50,5600))

maxX=5700
level=1
ymin=300




print("NUMBER OF ENEMIES=",len(enemies),len(flyingEnemies),len(coins))
while run:

    clock.tick(27)


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    

    keys = pygame.key.get_pressed()
  
    if keys[pygame.K_LEFT] and man.x > -30:
        man.x -= man.vel
        cameraX-=man.vel
        man.left = True
        man.right = False
        man.standing = False
        man.movingLeft=True
        man.movingRight=False
    elif keys[pygame.K_RIGHT] :#and man.x < 580 - man.width - man.vel:
        man.x += man.vel
        cameraX+=man.vel
        man.right = True
        man.left = False 
        man.standing = False
        man.movingLeft=False
        man.movingRight=True

    else:
        man.movingLeft=False
        man.movingRight=False
        man.standing = True
        man.walkCount = 0
    if not(man.isJump):
        if keys[pygame.K_UP] and man.y >=20 and (onBlock==True or man.y>=300):
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0

    else:
        if man.jumpCount >= 0 :
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.65 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 8



    #check if man is on block to cancell out gravity
    onBlock=False
    for block in blocks:
        if block.manOnBlock(man): 
            onBlock=True
    for wb in WoodenBlocks:
        if wb.manOnBlock(man):
            onBlock=True
    for b in boxes:
        if b.manOnBlock(man):
            onBlock=True
    #gravity
    if onBlock==False and man.y<ymin and man.isJump==False:
        man.y+=man.vel
                
    for e in enemies:
        rectA=pygame.Rect(man.hitbox)
        rectB=pygame.Rect(e.hitbox)
        if pygame.Rect.colliderect(rectA,rectB):
            if (man.y <=e.y-0.5*man.hitbox[3])  and man.isJump==False:
                print("Enemy dead")
                enemies.remove(e)
            else:
                print("GAME OVER")
                pygame.quit()
                exit()
    for e in flyingEnemies:
        rectA=pygame.Rect(man.hitbox)
        rectB=pygame.Rect(e.hitbox)
        if pygame.Rect.colliderect(rectA,rectB):
            if (man.y <=e.y-0.5*man.hitbox[3])  and man.isJump==False and onBlock==False:
                print("Enemy dead")
                flyingEnemies.remove(e)
            else:
                print("GAME OVER")
                pygame.quit()
                exit()
    for b in blocks:
        if b.hard==True:
            if b.manCollides(man):
                if man.movingRight==True and b.x >=man.x:
                    man.x-=man.vel*2
                    cameraX-=man.vel*2
                elif man.movingLeft==True and b.x <=man.x:
                    man.x+=man.vel*2
                    cameraX+=man.vel*2
    for wb in WoodenBlocks:
        if wb.manCollides(man):
            if man.movingRight==True and wb.x >=man.x:
                man.x-=man.vel*2
                cameraX-=man.vel*2
            elif man.movingLeft==True and wb.x <=man.x:
                man.x+=man.vel*2
                cameraX+=man.vel*2
    for b in boxes:
        if b.manCollides(man):
            if not onBlock and (man.isJump==True): 
                man.isJump=False
                man.jumpCount=8
                movingDownwards=True
            if man.movingRight==True and b.x >=man.x:
                man.x-=man.vel*2
                cameraX-=man.vel*2
            elif man.movingLeft==True and b.x <=man.x:
                man.x+=man.vel*2
                cameraX+=man.vel*2
            

    if maxX - man.width - man.vel<=man.x<=maxX - man.width - man.vel+10:
        man.x-=man.vel

    """
    user animation is okk now time to handle enemy animation
    """
    for e in enemies:
        enemyOnBlock=False
        for b in blocks:
            if b.manOnBlock(e):
                enemyOnBlock=True
            if b.manCollides(e):
                e.vel=e.vel*(-1)
        #if e.x >=500:
        #    print("ON BLOCK=",enemyOnBlock)
        if enemyOnBlock==False :
            e.y+=10
        if e.vel==0 and man.x >=2000:
            e.vel=-3
    """
    time to remove coins (and ad score)
    """
    for c in coins:
        rectA=pygame.Rect(man.hitbox)
        rectB=pygame.Rect(c.hitbox)
        if pygame.Rect.colliderect(rectA,rectB):
            coins.remove(c)
    """
    finaly before the end of the loop check end condition
    """
    rectA=pygame.Rect(man.hitbox)
    rectB=pygame.Rect(goalCoin.hitbox)
    if pygame.Rect.colliderect(rectA,rectB):
        print("VICTORY")
        break
    """
    now deal with ball collision
    """
    for ball in balls:
        rectB=pygame.Rect(ball.hitbox)
        if pygame.Rect.colliderect(rectA,rectB):
            if man.hitbox[1]<=ball.hitbox[1]-man.hitbox[3]/2:
                if abs(ball.vel)==3.5*4:
                    balls.remove(ball)
                else:
                    ball.vel=ball.vel*4
                    ball.x+=ball.vel*5
                    man.y-=100
                    break
            else:
                print("GAME OVER")
                pygame.quit()
                exit()
        if abs(ball.vel)==3.5*4:
            for e in enemies:
                rectA=pygame.Rect(e.hitbox)
                if pygame.Rect.colliderect(rectA,rectB):
                    enemies.remove(e)
        for pl in platforms:
            rectA=pygame.Rect(man.hitbox)
            rectB=pygame.Rect(pl.hitbox)
            if pygame.Rect.colliderect(rectA,rectB):
                #man.y-=200
                man.jumpCount=11
                man.y-=20
                man.isJump=True
                pl.active=True
    redrawGameWindow()

pygame.quit()


