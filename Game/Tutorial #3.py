import sys, pygame
pygame.init()

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0
screenWidth=500
screenHeight=480
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption(("I hate niggers"))
left=False
right=False
fps=27
clock=pygame.time.Clock()
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

x=50
y=400
width=40
height=60
vel=5 

isJump=False
jumpCount=10


def redraw_game_window():
    global walkCount
    screen.fill((0,0,0))
    screen.blit(bg,(0,0)) #background
    #pygame.draw.rect(screen,(255,0,0),(x,y,width,height))
    if walkCount +1  >= 27:
        walkCount=0
    if left:
        #integer division
        screen.blit(walkLeft[walkCount//3],(x,y))
        walkCount+=1
    elif right:
        screen.blit(walkRight[walkCount//3],(x,y))
        walkCount+=1
    else:
        screen.blit(char,(x,y))
    pygame.display.update()
#main loop
run = True
while run:
    clock.tick(27)
    #event is anything that happens from the user e.g click
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > vel:
        x-=vel
        left=True
        right=False
    elif keys[pygame.K_RIGHT] and x < screenWidth - width:
        x+=vel
        right=True
        left=False
    else:
        right=False
        left=False
        walkCount=0
    if not isJump:
        #if keys[pygame.K_UP] and y > vel :
        #    y-=vel
        #if keys[pygame.K_DOWN] and y < screenHeight - height -vel:
        #    y+=vel
        if keys[pygame.K_SPACE]:
            isJump=True
            right=False
            left=False
            walkCount=0
    else:
        if jumpCount >= -10:
            neg=1
            if jumpCount<0:
                neg=-1
            y-=0.5*(jumpCount**2)*neg
            jumpCount-=1
        else:
            isJump=False
            jumpCount=10
    #screen.fill((0,0,0))
    #pygame.draw.rect(screen,(255,0,0),(x,y,width,height))
    redraw_game_window()
pygame.quit()



