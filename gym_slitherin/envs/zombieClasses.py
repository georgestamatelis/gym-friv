import pygame

assetsPath="/home/georgestamatelis/gym-slitherin/zombieOnslaugt/"
class player(object):
    images = [pygame.image.load(assetsPath+'R1.png'), pygame.image.load(assetsPath+'R2.png'), pygame.image.load(assetsPath+'R3.png'), pygame.image.load(assetsPath+'R4.png'), pygame.image.load(assetsPath+'R5.png'), pygame.image.load(assetsPath+'R6.png'), pygame.image.load(assetsPath+'R7.png'), pygame.image.load(assetsPath+'R8.png'), pygame.image.load(assetsPath+'R9.png')]

    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.walkCount = 0
        self.isMoving=False
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)


    def draw(self, win):
        if self.walkCount +1 >= 27:
            self.walkCount = 0
        if self.isMoving:
            win.blit(self.images[self.walkCount//3], (self.x,self.y))
             
        else:
            win.blit(self.images[0],(self.x,self.y))
            
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
class Crate(object):
    def __init__(self,x,y,width,height,color=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color=color
        self.hitbox = (self.x, self.y,self.width,self.height)
        self.HP=500
    def draw(self,win):
        self.hitbox = (self.x, self.y,self.width,self.height)
        pygame.draw.rect(win, (100,40,0), self.hitbox)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
    def manCollides(self,man):#a collision happened but man is not above the block
        rectA=pygame.Rect(self.hitbox)
        rectB=pygame.Rect(man.hitbox)
        
        return pygame.Rect.colliderect(rectA,rectB)
        

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
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)


class weakZombie(object):
    images = [pygame.image.load(assetsPath+'Z1.png'), pygame.image.load(assetsPath+'Z2.png'), pygame.image.load(assetsPath+'Z3.png'), pygame.image.load(assetsPath+'Z4.png'), pygame.image.load(assetsPath+'Z5.png'), pygame.image.load(assetsPath+'Z6.png'), pygame.image.load(assetsPath+'Z7.png'), pygame.image.load(assetsPath+'Z8.png'), pygame.image.load(assetsPath+'Z9.png'), pygame.image.load(assetsPath+'Z10.png')]
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0
        self.vel = 1
        self.hitbox = (self.x -5, self.y, 40, 57)
        self.HP=100

    def draw(self, win):
        self.move(win)
        if self.walkCount + 1 >= 30:
            self.walkCount = 0
        
        win.blit(self.images[self.walkCount//3], (self.x,self.y))
        self.walkCount += 1
        
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def move(self,win):
        self.x -=self.vel
        self.hitbox = (self.x -5, self.y, 40, 53)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)