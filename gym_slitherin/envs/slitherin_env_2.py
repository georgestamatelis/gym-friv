
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
class Dino(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(Dino, self).__init__(name, x_max, x_min, y_max, y_min)
        img_name="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/dino.png"
        if not os.path.isfile(img_name):
            raise Exception("File doesn't exist")

        image = cv2.imread(img_name)
        if image is not None:
            bg = image / 255
        self.icon = cv2.imread(img_name) / 255.0
        self.icon_w = 64
        self.icon_h = 64
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))

#make a class double obstacle and a class tripple obstacle and 
class Obstacle(Point):
    def __init__(self, name, x_max, x_min, y_max, y_min):
        super(Obstacle, self).__init__(name, x_max, x_min, y_max, y_min)
        img_name="/home/georgestamatelis/gym-slitherin/gym_slitherin/envs/square.png"
        self.icon = cv2.imread(img_name)/ 255.0
        self.icon_w = 32
        self.icon_h = 32
        self.icon = cv2.resize(self.icon, (self.icon_h, self.icon_w))


####################################################################
##environment class
##environment class
class SlitherinEnv2(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 5
    }
    def __init__(self):
        

        #define Action space 
       
        self.action_space=spaces.Discrete(2,)
        #define Observation space
        self.observation_shape = (400, 800,3)
        self.observation_space = spaces.Box(low = np.zeros(self.observation_shape), 
                                            high = np.full(self.observation_shape,255),
                                            dtype = np.uint8)
        self.canvas = np.ones(self.observation_shape) * 1
        
        # Define elements present inside the environment
        self.elements = []
        
         # Permissible for agents to be
        self.y_min = int (self.observation_shape[0] * 0.1)
        self.x_min = 0
        self.y_max = int (self.observation_shape[0] * 0.9)
        self.x_max = self.observation_shape[1]
    def draw_elements_on_canvas(self):
        # Init the canvas 
        self.canvas = np.ones(self.observation_shape) * 1

        # Draw the heliopter on canvas
        for elem in self.elements:
            elem_shape = elem.icon.shape
            x,y = elem.x, elem.y
            self.canvas[y : y + elem_shape[1], x:x + elem_shape[0]] = elem.icon
        self.canvas[280:310,self.x_min:self.x_max]=0
 
        
    def reset(self):
        self.episode_return=0
        self.obstacle_count=0
        self.dinoJumping=0
        self.dinoHeight=250
        self.u=120
        
        self.g=9.98
        self.t=0
        self.h=0
        # Determine a place to intialise the chopper in
        x = random.randrange(int(self.observation_shape[0] * 0.05), int(self.observation_shape[0] * 0.10))
        y = self.dinoHeight
    
        # Intialise the chopper
        self.dino = Dino("Dino", self.x_max, self.x_min, self.y_max, self.y_min)
        self.dino.set_position(x,y)

        # Intialise the elements 
        self.elements = [self.dino]



        self.canvas = np.ones(self.observation_shape) * 1

        # Draw elements on the canvas
        self.draw_elements_on_canvas()


        # return the observation
        return self.canvas 


    def render(self, mode = "human"):
        assert mode in ["human", "rgb_array"], "Invalid mode, must be either \"human\" or \"rgb_array\""
        if mode == "human":
            cv2.imshow("Game", self.canvas)
            cv2.waitKey(10)
    
        elif mode == "rgb_array":
            return self.canvas

    def close(self):
        cv2.destroyAllWindows()
    def get_action_meanings(self):
        return {0:"Stay",1:"Move"}
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
    def newObstacle(self):
        # create an obstacle
        new_obstacle = Obstacle("obstacle{}".format(self.obstacle_count), self.x_max, self.x_min, self.y_max, self.y_min)
        self.obstacle_count += 1
        obstacle_x = self.x_max 
        obstacle_y = self.dinoHeight
        new_obstacle.set_position(self.x_max, obstacle_y)
        self.elements.append(new_obstacle)   
            
###########STEP FUNCTION
    def step(self, action):
        # Flag that marks the termination of an episode
        done = False
        self.episode_return+=1
        # Assert that it is a valid action 
        assert self.action_space.contains(action), "Invalid Action"

    
        reward = 0.1      
        
        # apply the action to dino
        if self.dinoJumping==0:
            if action == 0: #dino keeps running
                self.dino.move(0,0)
            elif action == 1: #dino jumps
                if self.dinoJumping==0:
                    self.dinoJumping=1
                    self.t=0
                    #self.dino.move(0,-10)
        else: #dyno is allready in the air

            self.t+=0.01
            if self.u >=0.5:
                #upward movement
                #equations are derived from basic high school mechanics but with a 
                #small coeffiecient infront of the decelleration to slow the animation down
                self.u=self.u - self.g * self.t 
                self.h=100*self.t - 0.0000001*0.5 * self.g *self.t *self.t
                self.dino.move(0,-int(self.h))
                if self.u <0.5:
                    self.h0=self.h
            else:
                #free fall
                self.h=-0.0000001*0.5*self.g*self.t *self.t
                self.dino.move(0,-int(self.h))
            if self.h <=0.1:
                self.dinoJumping=0
                self.h=0
                self.t=0
                self.dino.set_position(self.dino.get_position()[0],self.dinoHeight)
                self.u=120
        # Spawn a bird at the right edge with prob 0.01
        if self.episode_return % 100 ==0:
            self.newObstacle()
        
            # Append the spawned bird to the elements currently present in Env. 
        #update elements and set rewards
         # For elements in the Ev
        for elem in self.elements:
            if isinstance(elem, Obstacle):
                # If the obstacle has reached the left edge, remove it from the Env
                if elem.get_position()[0] <= self.x_min:
                    self.elements.remove(elem)
                    continue
                else:
                    # Move the bird left by 5 pts.
                    elem.move(-5,0)
            
                # If the bird has collided.
                if self.has_collided(self.dino, elem):
                    # Conclude the episode and remove the chopper from the Env.
                    done = True
                    reward = -1
                    self.elements.remove(self.dino)
        #print("END OF FOOKIN LOOP")


        # Draw elements on the canvas
        self.draw_elements_on_canvas()
        return self.canvas, reward, done, {}