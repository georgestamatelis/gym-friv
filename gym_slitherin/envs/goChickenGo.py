import numpy as np 
import cv2 
import matplotlib.pyplot as plt
import PIL.Image as Image
import gym
import random
import os 
from gym import Env, spaces
import time
import random
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

    
class Chicken(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(Chicken, self).__init__(name, x_max, x_min, y_max, y_min)
        img_name="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/bird.png"
        self.icon = cv2.imread(img_name)/ 255.0
        self.icon_w = 20
        self.icon_h = 20
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))
class Truck(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(Truck, self).__init__(name, x_max, x_min, y_max, y_min)
        img_name="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/pinkTruck.png"
        self.icon = cv2.imread(img_name)/ 255.0
        self.icon_w = 70
        self.icon_h = 55
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))

class backwardsTruck(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(backwardsTruck, self).__init__(name, x_max, x_min, y_max, y_min)
        img_name="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/backwardsTruck.png"
        self.icon = cv2.imread(img_name)/ 255.0
        self.icon_w = 70
        self.icon_h = 55
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))
class log(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(log, self).__init__(name, x_max, x_min, y_max, y_min)
        img_name="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/largeLog.png"
        self.icon = cv2.imread(img_name)/ 255.0
        self.icon_w = 75
        self.icon_h = 50
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))


class chickenGoEnv(Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 10
    }
    def __init__(self):
        super(chickenGoEnv, self).__init__()
        

        
        # Define a 2-D observation space
        self.observation_shape = (500, 800)
        self.observation_space = spaces.Box(low = np.zeros(self.observation_shape), 
                                            high = np.full(self.observation_shape,255),
                                            dtype = np.uint8)
    
        
        # Define an action space ranging from 0 to 5
        # 0 = do nothing
        # 1 = move forwards
        # 2 = move backwards
        # 3 = jump
        # 4 = up
        # 5 = down
        self.action_space = spaces.Discrete(6,)
                        



        # Create a canvas to render the environment images upon 

        backroundPath="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/chickenRoad2.png"      
        
        if not os.path.isfile(backroundPath):
            raise Exception("File doesn't exist")
        self.background=cv2.imread(backroundPath)/255.0
        self.canvas= cv2.resize(self.background, (800,500))  

        # Permissible for agents to be
        self.y_min = int (self.observation_shape[0] * 0.1)
        self.x_min = 0
        self.y_max = int (self.observation_shape[0] * 0.9)
        self.x_max = self.observation_shape[1]
        # Define elements present inside the environment
        self.elements = []
        
       
    def draw_elements_on_canvas(self):
        # Init the canvas 
        self.canvas= cv2.resize(self.background, (800,500))  

        # Draw the heliopter on canvas
        for elem in self.elements:
            elem_shape = elem.icon.shape
            x,y = elem.x, elem.y
            self.canvas[y : y + elem_shape[0], x:x + elem_shape[1]] = elem.icon
        elem=self.chickens[0]
        elem_shape = elem.icon.shape
        x,y = elem.x, elem.y
        self.canvas[y : y + elem_shape[0], x:x + elem_shape[1]] = elem.icon


    def reset(self):

        self.forwardCars=[]
        self.backwardCars=[]
        self.elements=[]
        self.chickens=[]
        self.logs=[]
        self.timeStep=0
        self.facingBackwards=False

        chicken=Chicken("chicken",self.x_max,self.x_min,self.y_max,self.y_min)
        self.chickens.append(chicken)
        self.elements.append(chicken)


        self.draw_elements_on_canvas()
        

    def render(self, mode = "human"):
        assert mode in ["human", "rgb_array"], "Invalid mode, must be either \"human\" or \"rgb_array\""
        if mode == "human":
            cv2.imshow("Game", self.canvas)
            cv2.waitKey(10)
    
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
    def step(self, action):
        self.timeStep+=1
        """
        first manage action
        """
        # 0 = do nothing
        # 1 = move forwards
        c=self.chickens[0]
        x,y=c.get_position()
        if action==1:
            c.set_position(x+4,y)
            self.facingBackwards=False
        # 2 = move backwards
        if action == 2 :
            c.set_position(x-4,y)
            self.facingBackwards=True
        # 3 = jump
        if action ==3:
            if self.facingBackwards==False:
                c.set_position(x+15,y)
            else:
                c.set_position(x-15,y)

        # 4 = up
        if action == 4 :
            c.set_position(x,y-4)
        # 5 = down
        if action == 5 :
            c.set_position(x,y+4)
        """
        add forward cars
        """
        
        if self.timeStep % 170==0 or self.timeStep==50 or self.timeStep == 120:
            car=Truck("Car",self.x_max,self.x_min,self.y_max,self.y_min)
            car.set_position(150,-10)
            self.forwardCars.append(car)
            self.elements.append(car)
        if self.timeStep % 270 ==0 or self.timeStep in [20,90,150]:
            car=Truck("Car",self.x_max,self.x_min,self.y_max,self.y_min)
            car.set_position(200,-10)
            self.forwardCars.append(car)
            self.elements.append(car)
        if self.timeStep % 327 == 0 or self.timeStep in  [30,100,150]:
            car=Truck("Car",self.x_max,self.x_min,self.y_max,self.y_min)
            car.set_position(270,-10)
            self.forwardCars.append(car)
            self.elements.append(car)
        #backward cars 
        if self.timeStep % 150 ==0  or self.timeStep in [30,90]:
            car=backwardsTruck("Car",self.x_max,self.x_min,self.y_max,self.y_min)
            car.set_position(480,440)
            self.backwardCars.append(car)
            self.elements.append(car)
        if self.timeStep % 220 ==0 :
            car=backwardsTruck("Car",self.x_max,self.x_min,self.y_max,self.y_min)
            car.set_position(530,440)
            self.backwardCars.append(car)
            self.elements.append(car)
        if self.timeStep % 270 ==0 :
            car=backwardsTruck("Car",self.x_max,self.x_min,self.y_max,self.y_min)
            car.set_position(590,440)
            self.backwardCars.append(car)
            self.elements.append(car)
        
        if self.timeStep % 140 ==0 :
            l= log("log",self.x_max,self.x_min,self.y_max,self.y_min)
            l.set_position(350,440)
            self.elements.append(l)
            self.logs.append(l)
        if self.timeStep % 170 ==0 :
            l= log("log",self.x_max,self.x_min,self.y_max+20,self.y_min-20)
            #l.icon=cv2.rotate(l.icon,cv2.cv2.ROTATE_180)
            l.set_position(400,-10)
            self.elements.append(l)
            self.logs.append(l)


        """
        Animate car movements
        """
        reward=0
        done=False
        for car in self.forwardCars:
            x,y=car.get_position()
            y=y+2
            car.set_position(x,y)
            if y>=390:
                self.forwardCars.remove(car)
                self.elements.remove(car)
            if self.has_collided(c,car):
                done=True
                reward=-1
        
        for car in self.backwardCars:
            x,y=car.get_position()
            y=y-2
            car.set_position(x,y)
            if y<=50:
                self.backwardCars.remove(car)
                self.elements.remove(car)
            if self.has_collided(c,car):
                done=True
                reward=-1
        if c.get_position()[0]>=700:
            reward=1
            done=True
        #animate logs
        for l in self.logs:
            x,y = l.get_position()
            if x==400:
                y=y+1
            else:
                y=y-1
            l.set_position(x,y)
            #print("fookin y again",y)
            if y>400 or  (y <=50 and x!=400):
                self.logs.remove(l)
                self.elements.remove(l)
        if 330<=c.get_position()[0]<=440:
            floating=False
            for l in self.logs:
                if self.has_collided(l,c):
                    floating=True
                    break
            if floating==False:
                print("Drawn")
                done=True
            else:
                x,y=c.get_position()
                if x<=385:
                    y=y-1
                else:
                    y=y+1
                c.set_position(x,y)

        self.draw_elements_on_canvas()
        #print("CHICKEN ->",c.get_position())
        return self.canvas,reward,done,{}


if __name__ == "__main__":
    from pyglet.window import key

    a = np.array([0,0]) 
    #a[0] is about actions
    # 0 = do nothing
    # 1 = move forwards
    # 2 = move backwards
    # 3 = jump
    # 4 = up
    # 5 = down
   
    
    def getActionFromKey(key):
        if key==32: #jump
            return 3
        
        if key==82: #up 
            return 4
        if key==84: #down
            return 5
        if key==81: #left
            return 2
        if key==83: #right
            return 1

        return 0
    env = chickenGoEnv()
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