import pygame
import random


pygame.init()

win = pygame.display.set_mode((700,700))

assetsPath="bossLevelPumpkin/"
walkRight = [pygame.image.load(assetsPath+'R1.png'), pygame.image.load(assetsPath+'R2.png'), pygame.image.load(assetsPath+'R3.png'), pygame.image.load(assetsPath+'R4.png'), pygame.image.load(assetsPath+'R5.png'), pygame.image.load(assetsPath+'R6.png'), pygame.image.load(assetsPath+'R7.png'), pygame.image.load(assetsPath+'R8.png'), pygame.image.load(assetsPath+'R9.png')]
walkLeft = [pygame.image.load(assetsPath+'L1.png'), pygame.image.load(assetsPath+'L2.png'), pygame.image.load(assetsPath+'L3.png'), pygame.image.load(assetsPath+'L4.png'), pygame.image.load(assetsPath+'L5.png'), pygame.image.load(assetsPath+'L6.png'), pygame.image.load(assetsPath+'L7.png'), pygame.image.load(assetsPath+'L8.png'), pygame.image.load(assetsPath+'L9.png')]
bg = pygame.image.load(assetsPath+'bg.png')
bg = pygame.transform.scale(bg,(700,700))

clock = pygame.time.Clock()

score = 0

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 7.5
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
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
               
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x 
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing #+-1
        self.vel=8*facing
        self.hitbox=(self.x-self.radius,self.y-self.radius,2*self.radius,2*self.radius)
    def draw(self,win):
        self.hitbox=(self.x-self.radius,self.y-self.radius,2*self.radius,2*self.radius)
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius) #,1 for not filled
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)

        
class Enemy(object):
    img=pygame.image.load(assetsPath+"ghost.png")
    def __init__(self,x,y):
        self.x=x
        self.y=y 
        self.hitbox = (self.x +25 , self.y+25, 110,105)
        self.vel=4
        self.HP=500

    def draw(self,win):
        if self.x >=560:
            self.vel=-4
        if self.x<=-60:
            self.vel=4
            
        self.x=self.x+self.vel
        self.hitbox = (self.x +25 , self.y+25, 110,105)
        win.blit(self.img,(self.x,self.y))
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
class evilcat(object):
    img=pygame.image.load(assetsPath+"evilCat.png")
    def __init__(self,x,y):
        self.x=x
        self.y=y 
        self.hitbox = (self.x+2 , self.y+5, 92,85)

        self.vel=4
        self.lifeSpan=75
    def getHitbox(self):
        return self.hitbox
    def draw(self,win):
        self.lifeSpan=self.lifeSpan-1
        if self.y <=520:
            self.y=self.y+10
        self.hitbox = (self.x+2 , self.y+5, 92,85)
        win.blit(self.img,(self.x,self.y))
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)




def redrawGameWindow():
    win.blit(bg, (0,0))
    textsurface = font.render('ENEMY', False, (0, 0, 0))
    textsurface2 = font.render('PLAYER', False, (0, 0, 0))

    win.blit(textsurface,(20,0))
    win.blit(textsurface2,(520,0))

    pygame.draw.rect(win, (0,255.0,0), (10,40,0.4*ghost.HP, 25))
    pygame.draw.rect(win, (0,255.0,0), (450,40,2*man.HP, 25))

    man.draw(win)
    for b in bullets:
        b.draw(win)
    for c in evilcats:
        c.draw(win)
    ghost.draw(win)
    pygame.display.update()

    

#mainloop
pygame.font.init()
font = pygame.font.SysFont('comicsans', 30, True)
man = player(50, 560, 64,64)
ghost = Enemy(random.randrange(0,400),50)
ghost.vel=random.choice([-4,4,-4.5,4.5])
bullets=[]
evilcats=[]
run=True
shootReset=0
catReset=0

while run:
    clock.tick(27)


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    
    #animate the bullets
    for b in bullets:
        if b.y <=5:
            bullets.pop(bullets.index(b))
        else:
            b.y=b.y -12
            rectA=pygame.Rect(b.hitbox)
            rectB=pygame.Rect(ghost.hitbox)
            if pygame.Rect.colliderect(rectA,rectB)==True:
                ghost.HP=ghost.HP-5
                if ghost.HP <=0:
                    print("VICTORY")    
                    run=False
    #animate the cats
    if catReset >=20:
        catReset=0
    if catReset>0:
        catReset+=1
    if catReset==0:
        #c=evilcat(ghost.x,ghost.y)
        evilcats.append(evilcat(ghost.x,ghost.y))
        catReset=1
    for c in evilcats:
        if c.lifeSpan<0:
            evilcats.pop(evilcats.index(c))
        else:
            hitbox=c.hitbox
            rectA=pygame.Rect(hitbox)
            rectB=pygame.Rect(man.hitbox)
            if pygame.Rect.colliderect(rectA,rectB)==True:
                man.HP=man.HP-25
                if man.HP <=0:
                    print("GAME OVER")  
                    run=False
                evilcats.pop(evilcats.index(c))
    
    keys = pygame.key.get_pressed()

    if shootReset>=16:
        shootReset=0
    if shootReset >0:
        shootReset+=1
    if keys[pygame.K_x]:
       
        if shootReset <=0 and len(bullets)<=15:
            facing=1
            bullet=projectile(
                    round(man.x+man.width+5),round(man.y+man.height//2),15,(0,0.2,0.6),facing)
            bullets.append(bullet)
            shootReset+=1
            shooting=True

    if keys[pygame.K_LEFT] and man.x > 10:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
        man.movingRight=False
        man.movingLeft=True
    elif keys[pygame.K_RIGHT] and man.x < 650 - man.width - man.vel:
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
   
    if not(man.isJump) :
        if keys[pygame.K_UP]: 
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
            movingDownwards=False
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
                
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            movingDownwards=True
            man.isJump = False
            man.jumpCount = 10
       

    redrawGameWindow()

pygame.quit()


