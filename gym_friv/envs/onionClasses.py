import pygame

assetsPath="./Game/assets/"
walkRight = [pygame.image.load(assetsPath+'R1.png'), pygame.image.load(assetsPath+'R2.png'), pygame.image.load(assetsPath+'R3.png'), pygame.image.load(assetsPath+'R4.png'), pygame.image.load(assetsPath+'R5.png'), pygame.image.load(assetsPath+'R6.png'), pygame.image.load(assetsPath+'R7.png'), pygame.image.load(assetsPath+'R8.png'), pygame.image.load(assetsPath+'R9.png')]
walkLeft = [pygame.image.load(assetsPath+'L1.png'), pygame.image.load(assetsPath+'L2.png'), pygame.image.load(assetsPath+'L3.png'), pygame.image.load(assetsPath+'L4.png'), pygame.image.load(assetsPath+'L5.png'), pygame.image.load(assetsPath+'L6.png'), pygame.image.load(assetsPath+'L7.png'), pygame.image.load(assetsPath+'L8.png'), pygame.image.load(assetsPath+'L9.png')]
bg = pygame.image.load(assetsPath+'onionBoyBG2.png')
bg = pygame.transform.scale(bg,(600,500))
bgx=0
bgy=0
char = pygame.image.load(assetsPath+'standing.png')

clock = pygame.time.Clock()


"""
CLASSES USED BY THE ACTUAL ENVIRONMENT / GAME
"""
#onion boy
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
        self.jumpCount = 8
        self.standing = True
        self.flying = False
        self.fuelLeft=100
        self.hitbox = (self.x +7, self.y + 11, 48, 52)
        self.movingRight=True
        self.movingLeft=False

    def draw(self, win,env):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x-env.cameraX,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x-env.cameraX,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x-env.cameraX, self.y))
            else:
                win.blit(walkLeft[0], (self.x-env.cameraX, self.y))
        self.hitbox = (self.x + 7-env.cameraX, self.y + 11,48, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
class WoodenBlock(object):
    def __init__(self,x,y,width,height,color=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color=color
        self.hitbox = (self.x, self.y,self.width,self.height)
    def draw(self,win,env):
        self.hitbox = (self.x-env.cameraX, self.y,self.width,self.height)
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

    def draw(self,win,env):
        self.hitbox = (self.x-env.cameraX, self.y,self.width,self.height)
        win.blit(self.img,(self.x-env.cameraX,self.y))
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
        self.vel = 3.5
        self.hitbox = (self.x + 4, self.y, 45, 60)

    def draw(self, win,env):
        self.move()
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x-env.cameraX,self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x-env.cameraX,self.y))
            self.walkCount += 1
        self.hitbox = (self.x + 4-env.cameraX, self.y, 45, 60)
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

    def draw(self, win,env):
        self.move()
        if self.walkCount + 1 >= 21:
            self.walkCount = 0
            
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x-env.cameraX,self.y))
            self.walkCount += 1
            self.hitbox = (self.x + 4-env.cameraX, self.y+35, self.width, 60)
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x-env.cameraX,self.y))
            self.walkCount += 1
            self.hitbox = (self.x + 34-env.cameraX, self.y+35, self.width, 60)

        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
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

    def draw(self, win,env):
        self.move()
        
        if self.walkCount  >= 3:
            self.walkCount = 0
        
        if self.vel > 0:
            win.blit(self.images[self.walkCount], (self.x-env.cameraX,self.y))
            self.walkCount += 1
        else:
            win.blit(self.images[self.walkCount], (self.x-env.cameraX,self.y))
            self.walkCount += 1
        
        self.hitbox = (self.x + 24-env.cameraX, self.y, 35, 60)
        #pygame.draw.rect(win,(240,0,255),self.hitbox)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
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

    def draw(self, win,env):
        
        if self.walkCount  >= len(self.images):
            self.walkCount = 0
            self.active=False
        if self.active==True:
            win.blit(self.images[self.walkCount], (self.x-env.cameraX,self.y))
            self.walkCount += 1
        else:
            win.blit(self.images[0],(self.x-env.cameraX,self.y))
        self.hitbox = (self.x + 24-env.cameraX, self.y+25, 35, 31)
        #pygame.draw.rect(win,(240,0,255),self.hitbox)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
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

    def draw(self, win,env):
        self.hitbox = (self.x -self.radius-env.cameraX, self.y-self.radius, 2*self.radius, 2*self.radius)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        pygame.draw.circle(win,self.color,(self.x-env.cameraX,self.y),self.radius)
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

    def draw(self, win,env):
        self.hitbox = (self.x -self.radius-env.cameraX, self.y-self.radius, 2*self.radius, 2*self.radius)
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