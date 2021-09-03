from os import fwalk
from numpy.lib.function_base import trim_zeros
import pygame
pygame.init()

win = pygame.display.set_mode((900,700))

assetsPath="/home/georgestamatelis/gym-slitherin/Game/"
walkRight = [pygame.image.load(assetsPath+'R1.png'), pygame.image.load(assetsPath+'R2.png'), pygame.image.load(assetsPath+'R3.png'), pygame.image.load(assetsPath+'R4.png'), pygame.image.load(assetsPath+'R5.png'), pygame.image.load(assetsPath+'R6.png'), pygame.image.load(assetsPath+'R7.png'), pygame.image.load(assetsPath+'R8.png'), pygame.image.load(assetsPath+'R9.png')]
walkLeft = [pygame.image.load(assetsPath+'L1.png'), pygame.image.load(assetsPath+'L2.png'), pygame.image.load(assetsPath+'L3.png'), pygame.image.load(assetsPath+'L4.png'), pygame.image.load(assetsPath+'L5.png'), pygame.image.load(assetsPath+'L6.png'), pygame.image.load(assetsPath+'L7.png'), pygame.image.load(assetsPath+'L8.png'), pygame.image.load(assetsPath+'L9.png')]
bg = pygame.image.load('/home/georgestamatelis/gym-slitherin/eyeCopter/EyeCopterBG.png')
bg = pygame.transform.scale(bg,(900,700))
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

def redrawGameWindow():
    win.blit(bg, (0,0))
    pygame.draw.rect(win, (255,0,0), (10,10, 50, 20))
    pygame.draw.rect(win, (0,128,0), (10,10, 50 - (5 * (10 -0.1*man.fuelLeft )), 20))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (390, 10))
    for b in blocks:
        b.draw(win)
    for s in spikes:
        s.draw(win)
    for v in vacums:
        v.draw(win)
    for c in coins:
        c.draw(win)
    man.draw(win)
    goalBlock.draw(win)
    #redRect=(10,10,50,20)
    #pygame.draw.rect(win,(255,0,0),redRect)
    pygame.display.update()


#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(50, 20, 64,64)
run = True
blocks=[]
spikes=[]
vacums=[]
coins=[]

coins.append(Coin(230,230,10))
coins.append(Coin(260,230,10))
coins.append(Coin(785,620,10))
coins.append(Coin(785,590,10))
coins.append(Coin(785,560,10))
coins.append(Coin(785,530,10))


blocks.append(Block(300,0,50,400))
blocks.append(Block(225,250,75,50))
blocks.append(Block(350,350,75,50))
blocks.append(Block(400,400,75,50))
blocks.append(Block(500,250,75,50))

blocks.append(Block(440,270,40,20,color=(255,255,255)))


blocks.append(Block(650,200,100,50))

#spikes in air
blocks.append(Block(200,525,50,50))
spikes.append(Spikes(250,525,50,50))
blocks.append(Block(300,525,50,50))

goalBlock=Block(675,175,25,25,color=(255,255,255))
movingDownwards=True

spikes.append(Spikes(650,650,50,50))
spikes.append(Spikes(700,650,50,50))


vacums.append(Vacum(675,250,50,300))


blocks.append(Block(475,500,50,50))
vacums.append(Vacum(525,500,50,150))
blocks.append(Block(575,500,50,50))

vel=1
while run:
    clock.tick(27)


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    

    keys = pygame.key.get_pressed()



    if keys[pygame.K_LEFT] and man.x > 30:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
        man.movingRight=False
        man.movingLeft=True
    elif keys[pygame.K_RIGHT] and man.x < 850 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False 
        man.standing = False
        man.movingLeft=False
        man.movingRight=True

    else:
        man.movingRight=False
        man.movingLeft=False
        man.standing = True
        man.walkCount = 0
    if keys[pygame.K_UP] and man.y >=10 and man.fuelLeft>0:
        manCollides=False
        for b in blocks:
            if b.manCollides(man):
                manCollides=True
        if manCollides==False:
            man.y=man.y-man.vel -10 # 10 is to undo gravity    
            inVacum=False
            rectB=pygame.Rect(man.hitbox)
            for v in vacums:
                rectA=pygame.Rect(v.hitbox)
                if pygame.Rect.colliderect(rectA,rectB):
                    inVacum=True 
            if inVacum==False:
                man.fuelLeft-=2
            man.flying=True
    else:
        if man.fuelLeft<100:
            man.fuelLeft+=1
    if not(man.isJump) :
        if keys[pygame.K_SPACE] and man.y >=120 and (onBlock==True or man.y>=580): 
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
            movingDownwards=False
    else:
        if man.jumpCount >= 0:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
                
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            movingDownwards=True
            man.isJump = False
            man.jumpCount = 10
    #gravity
    onBlock=False
    for block in blocks:
        if block.manOnBlock(man): 
            #man.y=-man.height+block.y
            onBlock=True
    for block in blocks:
        if block.manCollides(man):
            print("Man Colides")
            if not onBlock and (man.isJump==True or man.flying==True): 
                #man.y +=25
                if man.isJump==True:
                    man.isJump=False
                    man.jumpCount=10
                    movingDownwards=True
                
            if man.movingRight==True and block.x >=man.x:
                man.x-=man.vel*2
            elif man.movingLeft==True and block.x <=man.x:
                man.x+=man.vel*2
    ymin=580
    if 630<=man.x<=720:
        ymin=650 
    if man.y <=ymin and man.isJump==False and onBlock==False:
        man.y += 10
    if goalBlock.manOnBlock(man):
        print("Victory")
        pygame.quit()
        exit()
    for spike in spikes:
        if spike.manDown(man):
            print("GAME OVER")
            pygame.quit()
            exit()
    #move the small mobile white platform
    for b in blocks:
        if b.color==(255,255,255):
            if b.x>=460:
                vel=-1
            if b.x <= 380:
                vel=1
            b.x=b.x+2*vel
            if b.manOnBlock(man):
                man.x=man.x+2*vel
            #print("b.x=",b.x,"vel=",vel)
    #check coins collected
    for c in coins:
        rectA=pygame.Rect(man.hitbox)
        rectB=pygame.Rect(c.hitbox)
        if pygame.Rect.colliderect(rectA,rectB):
            coins.remove(c)

    redrawGameWindow()

pygame.quit()


