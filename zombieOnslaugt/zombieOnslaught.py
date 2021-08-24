import pygame
pygame.init()

WINDOW_W=500
WINDOW_H=500
win = pygame.display.set_mode((WINDOW_H,WINDOW_W))

pygame.display.set_caption("First Game")

assetsPath="/home/georgestamatelis/gym-slitherin/zombieOnslaugt/"

bg = pygame.image.load(assetsPath+'backround.png')
bg = pygame.transform.scale(bg,(WINDOW_H,WINDOW_W))
clock = pygame.time.Clock()


from zombieClasses  import *
    

def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    for cr in Crates:
        cr.draw(win)
    for wz in weakZombies:
        wz.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()


#mainloop
positions=[400,300,200]
Crates=[]
Crates.append(Crate(75,positions[0]+40,30,40,color=(100,40,0)))
Crates.append(Crate(75,positions[1]+40,30,40,color=(100,40,0)))
Crates.append(Crate(75,positions[2]+40,30,40,color=(100,40,0)))

weakZombies=[]
bullets=[]
#player 
man=player(10,positions[0],50,50)
#weak zombies
weakZombies.append(weakZombie(500,positions[0],64,64))
weakZombies.append(weakZombie(500,positions[1],64,64))
weakZombies.append(weakZombie(500,positions[2],64,64))

shootReset=0
run = True
goalPos=man.y
moveReset=0
shootReset=0
zombiesToKill=3
zombiesKilled=0
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    """
    ANIMATE BULLETS
    """
    for bullet in bullets:
        if bullet.x <=500 and bullet.x >0:
            bullet.x +=bullet.vel
        else:
            bullets.pop(bullets.index(bullet)) 
        for z in weakZombies:
            rectA=pygame.Rect(z.hitbox)
            rectB=pygame.Rect(bullet.hitbox)
            if pygame.Rect.colliderect(rectA,rectB)==True:
                z.HP-=50
                if z.HP<=0:
                    weakZombies.remove(z)
                    zombiesKilled+=1
                bullets.remove(bullet)
    if zombiesKilled==zombiesToKill:
        print("VICTORY")
    """
    now check collision between zombies and creates
    """
    for wz in weakZombies:
        for cr in Crates:
            if cr.manCollides(wz):
                cr.HP-=50
                wz.vel=0
                if cr.HP<=0:
                    Crates.remove(cr)
                    wz.vel=+3
        if wz.x<=0:
            print("GAME OVER")
    keys = pygame.key.get_pressed()
    if shootReset>=7:
        shootReset=0
    if shootReset >0:
        shootReset+=1
    if moveReset>0:
        moveReset+=1
    if moveReset >3:
        moveReset=0
    if (not man.isMoving ) :
        if moveReset >0:
            continue
        if keys[pygame.K_UP]:
            man.isMoving=True
            if man.y==positions[0]:
                goalPos=positions[1]
                man.vel=-5
            elif man.y==positions[1]:
                goalPos=positions[2]
                man.vel=-5
            else:
                man.isMoving=False
        elif keys[pygame.K_DOWN]:
            man.isMoving=True
            if man.y==positions[2]:
                goalPos=positions[1]
                man.vel=+5
            elif man.y==positions[1]:
                goalPos=positions[0]
                man.vel=+5
            else:
                man.isMoving=False
        elif keys[pygame.K_a]:
            if shootReset>0:
                continue
            if len(bullets)<=15:
                facing=1
                bullet=projectile(
                    round(man.x+man.width+5),round(man.y+man.height//2),6,(0,0.2,0.6),facing)
                bullets.append(bullet)
                shootReset+=1
                shooting=True
    else:
        #print("goalPos=",goalPos,"man.y=",man.y)
        man.y+=man.vel 
        man.walkCount+=1
        if man.y==goalPos and man.isMoving:
            man.isMoving=False
            man.walkCount=0
            if moveReset==0:
                moveReset=1
          
    redrawGameWindow()

pygame.quit()


