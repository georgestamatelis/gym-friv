
#in here i will build the dyno game
import numpy as np 
import cv2 
import matplotlib.pyplot as plt
import PIL.Image as Image
import gym
import random
import os
from numpy.core.fromnumeric import reshape 
from scipy import ndimage


from gym import Env, spaces
import time

font = cv2.FONT_HERSHEY_COMPLEX_SMALL 

#helper classes 
class Point(object):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        self.x = 0
        self.y = 0
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.name = name
    
    def set_position(self, x, y):
        self.x = self.clamp(x, self.x_min, self.x_max - self.icon_w)
        self.y = self.clamp(y, self.y_min, self.y_max - self.icon_h)
    
    def get_position(self):
        return (self.x, self.y)
    
    def move(self, del_x, del_y):
        self.x += del_x
        self.y += del_y
        
        self.x = self.clamp(self.x, self.x_min, self.x_max - self.icon_w)
        self.y = self.clamp(self.y, self.y_min, self.y_max - self.icon_h)

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)
#soldier shooting zombies
class Soldier(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(Soldier, self).__init__(name, x_max, x_min, y_max, y_min)
        img_name="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/humanAgent.png"
        if not os.path.isfile(img_name):
            raise Exception("File doesn't exist")

        image = cv2.imread(img_name)
        if image is not None:
            bg = image / 255
        self.icon = cv2.imread(img_name) / 255.0
        self.icon_w = 64
        self.icon_h = 64
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))

#crate
class Crate(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(Crate, self).__init__(name, x_max, x_min, y_max, y_min)
        img_name="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/crate.png"
        if not os.path.isfile(img_name):
            raise Exception("File doesn't exist")

        image = cv2.imread(img_name)
        if image is not None:
            bg = image / 255
        self.icon = cv2.imread(img_name) / 255.0
        self.icon_w = 40
        self.icon_h = 40
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))
        self.HP=100


#small zombie
class smallZombie(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(smallZombie, self).__init__(name, x_max, x_min, y_max, y_min)
        img_name="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/zombie.png"
        if not os.path.isfile(img_name):
            raise Exception("File doesn't exist")

        image = cv2.imread(img_name)
        if image is not None:
            bg = image / 255
        self.icon = cv2.imread(img_name) / 255.0
        self.icon_w = 40
        self.icon_h = 40
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))
        self.HP=20
#strong zombie
class strongZombie(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(strongZombie, self).__init__(name, x_max, x_min, y_max, y_min)
        img_name="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/strongZombie.png"
        if not os.path.isfile(img_name):
            raise Exception("File doesn't exist")

        image = cv2.imread(img_name)
        if image is not None:
            bg = image / 255
        self.icon = cv2.imread(img_name) / 255.0
        self.icon_w = 40
        self.icon_h = 40
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))
        self.HP=100
#bullet
class bullet(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(bullet, self).__init__(name, x_max, x_min, y_max, y_min)
        img_name="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/fuel.png"
        if not os.path.isfile(img_name):
            raise Exception("File doesn't exist")

        image = cv2.imread(img_name)
        if image is not None:
            bg = image / 255
        self.icon = cv2.imread(img_name) / 255.0
        self.icon_w = 10
        self.icon_h = 10
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))
        self.damage=10
####################################################################
##environment class
##environment class
class zombieOnslaught(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 5
    }
    def __init__(self):


        #define Action space 
        """
        0)do nothing
        1)up
        2)down
        3)shoot
        """
        self.action_space=spaces.Discrete(4)
        #define Observation space
        self.observation_shape = (500, 800,3)
        self.observation_space = spaces.Box(low = np.zeros(self.observation_shape), 
                                            high = np.full(self.observation_shape,255),
                                            dtype = np.uint8)
        backroundPath="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/backround.png"      
        
        if not os.path.isfile(backroundPath):
            raise Exception("File doesn't exist")
        self.background=cv2.imread(backroundPath)/255.0
        self.canvas= cv2.resize(self.background, (800,500))  
        
        # Define elements present inside the environment
        self.elements = []
        
         # Permissible for agents to be
        self.y_min = int (self.observation_shape[0] * 0.1)
        self.x_min = 0
        self.y_max = int (self.observation_shape[0] * 0.9)
        self.x_max = self.observation_shape[1]

        self.positions=[175,275,375]
        """
        the following lists are used to simplify contact detection algorithm
        """
        
        self.zombiesToKill=10
        self.viewer=None
        
    def draw_elements_on_canvas(self):
        # Init the canvas 
        #self.canvas = np.ones(self.observation_shape) *0
        self.canvas= cv2.resize(self.background, (800,500))  

        # Draw the objects on canvas
        for elem in self.elements:
            elem_shape = elem.icon.shape
            x,y = elem.x, elem.y
            self.canvas[y : y + elem_shape[1], x:x + elem_shape[0]] = elem.icon
        #self.canvas[280:310,self.x_min:self.x_max]=0
 
        
    def reset(self):
        self.zombiesKilled=0
        self.timeSteps=0
        self.isSoldierMoving=False
        self.crates=[]
        self.zombies=[]
        self.bullets=[]
        self.elements=[]
        self.canvas = np.ones(self.observation_shape) * 0

        # Draw elements on the canvas
        self.draw_elements_on_canvas()

        #soldier
        self.soldier=Soldier("Soldier",self.x_max,self.x_min,self.y_max,self.y_min)
        self.pos=self.positions[1] #midle
        self.soldier.set_position(10,self.pos)
        self.elements.append(self.soldier)

        #crate 1
        self.crate1=Crate("Create1",self.x_max,self.x_min,self.y_max,self.y_min)
        self.crate1.set_position(80,self.positions[0]+30)
        self.elements.append(self.crate1)
        
        
        #crate 2
        self.crate2=Crate("Create2",self.x_max,self.x_min,self.y_max,self.y_min)
        self.crate2.set_position(80,self.positions[1]+30)
        self.elements.append(self.crate2)


        #crate 3
        self.crate3=Crate("Create3",self.x_max,self.x_min,self.y_max,self.y_min)
        self.crate3.set_position(80,self.positions[2]+30)
        self.elements.append(self.crate3)

        self.crates=[self.crate1,self.crate2,self.crate3]
        self.zombies=[]
        self.lastBullet=-1
        self.lastMove=-1
        # return the observation
        return self.canvas 


    def render(self, mode = "human"):
        assert mode in ["human", "rgb_array"], "Invalid mode, must be either \"human\" or \"rgb_array\""
        if mode == "human":
            cv2.imshow("Game", self.canvas)
            cv2.waitKey(10)
            #from gym.envs.classic_control import rendering
            #if self.viewer is None:
            #    self.viewer = rendering.SimpleImageViewer(maxwidth=self.canvas.shape[1])
            #self.viewer.imshow(self.canvas)
        elif mode == "rgb_array":
            return self.canvas

    def close(self):
        cv2.destroyAllWindows()
    
    def has_collided(self, elem1, elem2):
        x_col = False
        y_col = False

        elem1_x, elem1_y = elem1.get_position()
        elem2_x, elem2_y = elem2.get_position()

        if 2 * abs(elem1_x - elem2_x) <= (elem1.icon_w + elem2.icon_w):
            x_col = True

        if 2 * abs(elem1_y - elem2_y) <= (elem1.icon_h + elem2.icon_h):
            y_col = True

        if x_col and y_col:
            return True
    
###########STEP FUNCTION
    def step(self, action):
        self.timeSteps+=1
        #action mapping 
        """
        0) nothing
        1) up
        2) down
        3) shoot
        """
        if not self.isSoldierMoving:
            if action==1: #move up
                if self.pos==self.positions[2]: #is at botom
                    self.pos=self.positions[1]
                    self.isSoldierMoving=True
                    self.lastMove=self.timeSteps
                elif self.pos==self.positions[1]: #is at middle
                    self.pos=self.positions[0]
                    self.isSoldierMoving=True
                    self.lastMove=self.timeSteps

            if action==2: #move down
                if self.pos==self.positions[0]: #is at top
                    self.pos=self.positions[1]
                    self.isSoldierMoving=True
                    self.lastMove=self.timeSteps

                elif self.pos==self.positions[1]: #is at middle
                    self.pos=self.positions[2]
                    self.isSoldierMoving=True
                    self.lastMove=self.timeSteps

            if action==3:
                if self.timeSteps-self.lastBullet>=25:
                    b=bullet("bullet",self.x_max,self.x_min,self.y_max,self.y_min)
                    b.set_position(70,self.soldier.get_position()[1])
                    self.bullets.append(b)
                    self.elements.append(b)
                    self.lastBullet=self.timeSteps
        else:
            if self.timeSteps-self.lastMove >=15:
                self.isSoldierMoving=False
        self.soldier.set_position(10,self.pos)
        #print("soldier=",self.soldier.get_position())
        #add a zombie
        """
        the following 3 ifs spawn the first three zombies
        """
        reward=0
        if self.timeSteps==50:
            zombie=smallZombie("Zombie",self.x_max,self.x_min,self.y_max,self.y_min)
            zombie.set_position(800,self.positions[0])
            #print("zombie=",zombie.get_position())

            self.zombies.append(zombie)
            self.elements.append(zombie)
        if self.timeSteps==70:
            zombie=smallZombie("Zombie",self.x_max,self.x_min,self.y_max,self.y_min)
            zombie.set_position(800,self.positions[1])
            #print("zombie=",zombie.get_position())

            self.zombies.append(zombie)
            self.elements.append(zombie)
        if self.timeSteps==90:
            zombie=smallZombie("Zombie",self.x_max,self.x_min,self.y_max,self.y_min)
            zombie.set_position(800,self.positions[2])
            #print("zombie=",zombie.get_position())

            self.zombies.append(zombie)
            self.elements.append(zombie)
        if self.timeSteps==300:
            zombie=smallZombie("Zombie",self.x_max,self.x_min,self.y_max,self.y_min)
            zombie.set_position(800,self.positions[2])
            #print("zombie=",zombie.get_position())

            self.zombies.append(zombie)
            self.elements.append(zombie)

            zombie2=strongZombie("Zombie",self.x_max,self.x_min,self.y_max,self.y_min)
            zombie2.set_position(800,self.positions[1])
            #print("zombie=",zombie.get_position())

            self.zombies.append(zombie2)
            self.elements.append(zombie2)

            zombie3=smallZombie("Zombie",self.x_max,self.x_min,self.y_max,self.y_min)
            zombie3.set_position(800,self.positions[0])
            #print("zombie=",zombie.get_position())

            self.zombies.append(zombie3)
            self.elements.append(zombie3)
        if self.timeSteps==550:
            zombie=smallZombie("Zombie",self.x_max,self.x_min,self.y_max,self.y_min)
            zombie.set_position(800,self.positions[2])
            #print("zombie=",zombie.get_position())

            self.zombies.append(zombie)
            self.elements.append(zombie)

            zombie2=smallZombie("Zombie",self.x_max,self.x_min,self.y_max,self.y_min)
            zombie2.set_position(800,self.positions[0])
            #print("zombie=",zombie.get_position())

            self.zombies.append(zombie2)
            self.elements.append(zombie2)
        if self.timeSteps==600:
            zombie=strongZombie("Zombie",self.x_max,self.x_min,self.y_max,self.y_min)
            zombie.set_position(800,self.positions[2])
            #print("zombie=",zombie.get_position())

            self.zombies.append(zombie)
            self.elements.append(zombie)

            zombie2=strongZombie("Zombie",self.x_max,self.x_min,self.y_max,self.y_min)
            zombie2.set_position(800,self.positions[0])
            #print("zombie=",zombie.get_position())

            self.zombies.append(zombie2)
            self.elements.append(zombie2)
            
        """
        
        now time to check the zombies and the bullets
        
        """
        done=False
        for z in self.zombies:
            #check colision with crates
            move=True
            for crate in self.crates:
                if self.has_collided(z,crate):
                    move=False
                    crate.HP=crate.HP-1
                    if crate.HP<=0:
                        self.crates.remove(crate)
                        self.elements.remove(crate)
            for b in self.bullets:
                #print("Bullet Position=",b.get_position(),"Zombie=",z.get_position())
                if self.has_collided(b,z):
                    z.HP-=2
                x,y=b.get_position()
                x=x+2
                b.set_position(x,y)
                if x >=790:
                    self.elements.remove(b)
                    self.bullets.remove(b)
            if z.HP<=0:
                self.elements.remove(z)
                self.zombies.remove(z)
                self.zombiesKilled+=1
                reward=reward+1.0/self.zombiesToKill
                continue
            #if a zombie hasn't collided with a crate update it's animation
            if move==True:
                x,y=z.get_position()
                z.set_position(x-1,y)
            if z.get_position()[0]<=5:
                done=True
                print("GAME OVER")
                reward=-1


        self.draw_elements_on_canvas()
        if self.zombiesToKill == self.zombiesKilled:
            print("VICTORY")
            done=True
        return self.canvas,reward,done,{}
#######################################################################################

#   CODE BELLOW ONLY USED FOR USER PLAY


########################################################################################
    


if __name__ == "__main__":
    from pyglet.window import key

    a = np.array([0,0]) 
    #a[0] is about actions
    """
    0)nothing
    1)up
    2)down
    3)shoot
    """
   
    def key_press(k, mod):
        global restart
        #if k == 0xFF0D:
        #    restart = True
        if k == key.DOWN:
            a[0] = 2 #down
        if k == key.UP:
            a[0] = 1 #up

    def key_release(k, mod):
        
        if k == key.DOWN and a[0]==2:
            a[0] = 0
        if k == key.UP and a[0]==1:
            a[0] = 0
    def getActionFromKey(key):
        if key==97:
            return 3
        if key==82:
            return 1
        if key==84:
            return 2
        return 0
    env = zombieOnslaught()
    img=env.render(mode="rgb_array")
    """
    env.viewer.window.on_key_press = key_press
    env.viewer.window.on_key_release = key_release
    record_video = False
    if record_video:
        from gym.wrappers.monitor import Monitor

        env = Monitor(env, "/tmp/video-test", force=True)
    """
    isopen = True
    while isopen:
        env.reset()
        total_reward = 0.0
        steps = 0
        restart = False
        while True:
            cv2.imshow("Game",img)
            key=cv2.waitKey(10)
            
            action=getActionFromKey(key)
            s, r, done, info = env.step(action)
            total_reward += r
            if steps % 200 == 0 or done:
                print("action= ",action)
                print("step {} total_reward {:+0.2f}".format(steps, total_reward))
            steps += 1
            img=env.render("rgb_array")
            #isopen = env.render()
            if done:
                break
            #if done or restart or isopen == False:
            #    break
    env.close()