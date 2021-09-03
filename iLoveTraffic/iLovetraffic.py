import pygame
pygame.init()

WINDOW_W=500
WINDOW_H=500

win = pygame.display.set_mode((WINDOW_H,WINDOW_W))

pygame.display.set_caption("I Love Traffic")

assetsPath="/home/georgestamatelis/gym-slitherin/iLoveTraffic/"

bg = pygame.image.load(assetsPath+'background.png')
bg = pygame.transform.scale(bg,(WINDOW_H,WINDOW_W))
clock = pygame.time.Clock()


class Car(object):
    def __init__(self,x,y,width,height,color=(0,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cleared=False
        self.color=color
        self.hitbox = (self.x, self.y,self.width,self.height)
        self.HP=500
    def draw(self,win):
        self.hitbox = (self.x, self.y,self.width,self.height)
        pygame.draw.rect(win, self.color, self.hitbox)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
def redrawGameWindow():
    win.blit(bg, (0,0))
    #draw black lines surounding the roads
    pygame.draw.rect(win,(1,1,1),(265,0,10,500))
    pygame.draw.rect(win,(1,1,1),(275+45,0,10,500))
    pygame.draw.rect(win,(1,1,1),(0,240,500,10))
    pygame.draw.rect(win,(1,1,1),(0,285+20+35,500,10))

    #draw the roads
    road1=(275,0,45,500)
    pygame.draw.rect(win, (127,127,127), road1)
    road2=(0,250,500,45)
    pygame.draw.rect(win, (127,127,127), road2)
    lane=(0,285,500,20)
    pygame.draw.rect(win, (255,255,255), lane)
    road3=(0,285+20,500,35)
    pygame.draw.rect(win, (127,127,127), road3)

    #draw traffic light
    pygame.draw.rect(win,(1,1,1),(210,195,40,40))
    if isRed:
        pygame.draw.circle(win,(255,0,0),(230,215),12.5)
    else:
        pygame.draw.circle(win,(0,255,0),(230,215),12.5)
    for c in verticalCars:
        c.draw(win)
    for c in leftCars:
        c.draw(win)
    for c in rightCars:
        c.draw(win)
    pygame.display.update()

verticalCars=[]
leftCars=[]
rightCars=[]
verticalCars.append(Car(285,10,25,40,(240,0,255)))
leftCars.append(Car(465,255,40,25,(240,0,255)))
rightCars.append(Car(5,285+25,40,25,(240,0,255)))
isRed=True

run=True
numSteps=0
numCleared=0
mouseDelay=0
while run:
    numWaiting=0
    numSteps+=1
    if numSteps %90==0:
        leftCars.append(Car(465,255,40,25,(240,0,255)))
        rightCars.append(Car(5,285+25,40,25,(240,0,255)))
        verticalCars.append(Car(285,10,25,40,(240,0,255)))

    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #for better user experience
    if mouseDelay >0:
        mouseDelay+=1
    if mouseDelay >3 :
        mouseDelay=0
    #user action
    if pygame.mouse.get_pressed()[0]==1 and mouseDelay==0:
        mx,my=pygame.mouse.get_pos()
        if 210<=mx<=250 and 190 <=my<=230:
            isRed=not isRed
            mouseDelay=1
    #animate existing verticalCars
    for c in verticalCars:
        if c.y<=205 or  isRed==False or c.y >=220:
            willCollide=False
            for c2 in verticalCars:
                if c2.y == c.y+40:
                    willCollide=True
                    numWaiting+=1
            if not willCollide:
                c.y+=5
        if c.y >=270 and c.cleared==False:
            c.cleared=True
            numCleared+=1
        if c.y >=500:
            verticalCars.remove(c)
    for c in leftCars:
        c.x-=5    
        if c.x <=0:
            leftCars.remove(c)
    for c in rightCars:
        c.x+=5    
        if c.x <=0:
            rightCars.remove(c)
    #now time to check collisions
    for c1 in verticalCars:
        rectA=pygame.Rect(c1.hitbox)
        for c2 in leftCars:
            rectB=pygame.Rect(c2.hitbox)
            if pygame.Rect.colliderect(rectA,rectB)==True:
                print("GAME OVER")
                pygame.quit()
                exit()
        for c2 in rightCars:
            rectB=pygame.Rect(c2.hitbox)
            if pygame.Rect.colliderect(rectA,rectB)==True:
                print("GAME OVER")
                pygame.quit()
                exit()
    if numWaiting >=4:
        print("TO MUCH TRAFFIC")
        break
    #check end/victory condition
    if numCleared >=10:
        print("VICTORY")
        break    

    redrawGameWindow()
pygame.quit()
exit()