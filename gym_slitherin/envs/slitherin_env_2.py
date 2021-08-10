
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

        self.positions=[25,150,300]

        self.viewer=None
        
    def draw_elements_on_canvas(self):
        # Init the canvas 
        self.canvas = np.ones(self.observation_shape) *0

        # Draw the agent on canvas
        for elem in self.elements:
            elem_shape = elem.icon.shape
            x,y = elem.x, elem.y
            self.canvas[y : y + elem_shape[1], x:x + elem_shape[0]] = elem.icon
        #self.canvas[280:310,self.x_min:self.x_max]=0
 
        
    def reset(self):
        


        self.canvas = np.ones(self.observation_shape) * 0

        # Draw elements on the canvas
        self.draw_elements_on_canvas()

        self.soldier=Soldier("Soldier",self.x_max,self.x_min,self.y_max,self.y_min)
        self.pos=self.positions[1] #midle
        self.soldier.set_position(10,self.pos)
        # return the observation
        self.elements.append(self.soldier)
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
       
        #action mapping 
        """
        0) nothing
        1) up
        2) down
        3) shoot
        """
        if action==1: #move up
            if self.pos==self.positions[2]: #is at botom
                self.pos=self.positions[1]
            elif self.pos==self.positions[1]: #is at middle
                self.pos=self.positions[0]
        if action==2: #move down
            if self.pos==self.positions[0]: #is at top
                self.pos=self.positions[1]
            elif self.pos==self.positions[1]: #is at middle
                self.pos=self.positions[2]
        self.soldier.set_position(10,self.pos)
        #return self.canvas, reward, done, {}
        self.draw_elements_on_canvas()

        return self.canvas,0,False,{}
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