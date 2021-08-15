import sys, pygame
pygame.init()

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0
screenWidth=500
screenHeight=500
screen = pygame.display.set_mode((screenHeight,screenWidth))
pygame.display.set_caption(("I hate niggers"))
ball = pygame.image.load("gym_slitherin/envs/redBullet.png")


x=50
y=425
width=40
height=60
vel=5 

isJump=False
jumpCount=10
#main loop
run = True
while run:
    pygame.time.delay(100)
    #event is anything that happens from the user e.g click
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > vel:
        x-=vel
    if keys[pygame.K_RIGHT] and x < screenWidth - width:
        x+=vel
    if not isJump:
        if keys[pygame.K_UP] and y > vel :
            y-=vel
        if keys[pygame.K_DOWN] and y < screenHeight - height -vel:
            y+=vel
        if keys[pygame.K_SPACE]:
            isJump=True
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
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(255,0,0),(x,y,width,height))
    pygame.display.update()
pygame.quit()



