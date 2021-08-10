from gym_slitherin.envs.hill_climber_env import VIEWPORT_H, VIEWPORT_W
import sys
import math
import numpy as np

import Box2D
from Box2D.b2 import fixtureDef
from Box2D.b2 import polygonShape
from Box2D.b2 import contactListener
from Box2D import (b2ContactListener, b2DestructionListener, b2DrawExtended)
from Box2D import (b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,b2_pi)

import gym
from gym import spaces
from gym.envs.box2d.car_dynamics import Car
from gym.utils import seeding, EzPickle

import pyglet

pyglet.options["debug_gl"] = False
from pyglet import gl
from topDownCar import *

VIEWPORT_W = 1000
VIEWPORT_H = 800

SCALE = 6.0  
FPS = 60  # Frames per second



#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Based on Chris Campbell's tutorial from iforce2d.net:
http://www.iforce2d.net/b2dtut/top-down-car
"""

from Box2D.examples.framework import (Framework, Keys, main)
import math




class carParking2(gym.Env, EzPickle):
    metadata = {
        "render.modes": ["human", "rgb_array", "state_pixels"],
        "video.frames_per_second": FPS,
    }

    def __init__(self, verbose=1):
        EzPickle.__init__(self)
        self.seed()
        self.contactListener_keepref = myContactListener(self)
        self.world = Box2D.b2World((0, 0), contactListener=self.contactListener_keepref)
        self.world.gravity = (0, 0)
        self.viewer = None


        #steering : noop, left right
        #gass     : noop, forward backward

        self.action_space = spaces.Discrete(9)
        

        self.observation_space = spaces.Box(
            low=0, high=255, shape=(VIEWPORT_H, VIEWPORT_W, 3), dtype=np.uint8
        )
                # The walls
        self.obs=[]
        self.tires=[]
        self.cars=[]
        self.grounds=[]
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _destroy(self):
        """
       
        """
        if not self.obs:
            return
        for  obj in self.obs:
            for f in obj.fixtures:
                obj.DestroyFixture(f)
        self.world.DestroyBody(obj)
  
        self.obs=[]
        self.keysPressed=[]

    def reset(self):
        self._destroy()
        self.tires=[]
        self.cars=[]
        self.grounds=[]
        self.hasLost=False
        self.hasWon=False
        self.boundary = self.world.CreateStaticBody(position=(0, 0))
        self.boundary.CreateEdgeChain([(-50, -50),
                                  (-50, 50),
                                  (100, 50),
                                  (100, -50),
                                  (-50, -50)]
                                 )
        self.boundary.color=(0.5,0,0.5)
        self.boundary.userData="Boundary"
        self.obs.append(self.boundary)
        self.grounds.append(self.boundary)
        # A couple regions of differing traction
        self.car = TDCar(self.world,position=(90,-40))
        self.car.body.color=Box2D.b2Color(0.2,0.7, 0)

        self.obs.append(self.car.body)
        self.cars.append(self.car.body)
        for t in self.car.tires:
            t.color=Box2D.b2Color(0,0,0)
            self.obs.append(t.body)
            self.tires.append(t.body)
        #add aditional cars 
        #car 2
        self.car2 = TDCar(self.world,position=(-20,-30))
        self.car2.body.color=Box2D.b2Color(0.9,0.1, 0)
        self.car2.body.userData="Pavement"
        self.cars.append(self.car2.body)
        self.obs.append(self.car2.body)
        for t in self.car2.tires:
            t.color=Box2D.b2Color(0,0,0)
            self.obs.append(t.body)
            self.tires.append(t.body)
        #car 3
        self.car3 = TDCar(self.world,position=(-30,-30))
        self.car3.body.color=Box2D.b2Color(0.9,0.1, 0)
        self.car3.body.userData="Pavement"
    
        self.obs.append(self.car3.body)
        self.cars.append(self.car3.body)
        for t in self.car3.tires:
            t.color=Box2D.b2Color(0,0,0)
            self.obs.append(t.body)
            self.tires.append(t.body)
        #car 4
        self.car4 = TDCar(self.world,position=(-10,-30))
        self.car4.body.color=Box2D.b2Color(0.7,0.7, 0.7)
        self.car4.body.userData="Pavement"
    
        self.obs.append(self.car4.body)
        self.cars.append(self.car4.body)
        for t in self.car4.tires:
            t.color=Box2D.b2Color(0,0,0)
            self.obs.append(t.body)
            self.tires.append(t.body)
        #car 5
        self.car5 = TDCar(self.world,position=(-45,-50))
        self.car5.body.color=Box2D.b2Color(0.9,0.1, 0)
        self.car5.body.userData="Pavement"
    
        self.obs.append(self.car5.body)
        self.cars.append(self.car5.body)
        for t in self.car5.tires:
            t.color=Box2D.b2Color(0,0,0)
            self.obs.append(t.body)
            self.tires.append(t.body)
        #car 6
        self.car6 = TDCar(self.world,position=(-25,20))
        self.car6.body.color=Box2D.b2Color(0.0,0.7, 0)
        self.car6.body.userData="Pavement"
    
        self.obs.append(self.car6.body)
        self.cars.append(self.car6.body)
        for t in self.car6.tires:
            t.color=Box2D.b2Color(0,0,0)
            self.obs.append(t.body)
            self.tires.append(t.body)
        
        #this is the goal parking spot
        self.gnd1 = self.world.CreateStaticBody()
        fixture = self.gnd1.CreatePolygonFixture(
            box=(7,10, (-35, 25), math.radians(0)))
        self.gnd1.color=Box2D.b2Color(1, 1, 0)
        self.gnd1.userData="Spot"
        # Set as sensors so that the car doesn't collide
        fixture.sensor = True
        self.grounds.append(self.gnd1)
        self.obs.append(self.gnd1)
        #first obstacle
        self.gnd2 = self.world.CreateStaticBody()
        fixture = self.gnd2.CreatePolygonFixture(
            box=(10, 35, (10, 0), math.radians(0)))
        fixture.sensor = True
        self.gnd2.color=Box2D.b2Color(0, 0, 0.7)
        self.gnd2.userData="Pavement"
        self.grounds.append(self.gnd2)

        self.obs.append(self.gnd2)

        #sekecond obstacle
        self.gnd3 = self.world.CreateStaticBody()
        fixture = self.gnd3.CreatePolygonFixture(
            box=(10, 25, (-5,-40), math.radians(90))
        )
        fixture.sensor = True
        #fixture2= self.gnd3.CreatePolygonFixture(
         #  box=(10, 30, (-25,0), math.radians(00))
        #)
        #fixture2.sensor = True
        self.gnd3.color=Box2D.b2Color(0, 0, 0.7)
        self.gnd3.userData="Pavement"
        self.obs.append(self.gnd3)
        self.grounds.append(self.gnd3)

        #third obstacle 

        self.gnd4 = self.world.CreateStaticBody()
        fixture = self.gnd4.CreatePolygonFixture(
            box=(15, 10, (-35, 40), math.radians(0)))
        fixture.sensor = True
        self.gnd4.color=Box2D.b2Color(0, 0, 0.7)
        self.gnd4.userData="Pavement"
        self.obs.append(self.gnd4)
        self.grounds.append(self.gnd4)


        #fourth obstacle
        self.gnd5 = self.world.CreateStaticBody()
        fixture = self.gnd5.CreatePolygonFixture(
            box=(30, 5, (50, -20), math.radians(90)))
        fixture.sensor = True
        fixture2 =self.gnd5.CreatePolygonFixture(
            box=(15, 5, (50, 35), math.radians(90)))
        fixture2.sensor = True
        self.gnd5.color=Box2D.b2Color(0, 0, 0.7)
        self.gnd5.userData="Pavement"

        self.obs.append(self.gnd5)
        self.grounds.append(self.gnd5)

        #fifth obstacle
        self.gnd6 = self.world.CreateStaticBody()
        fixture = self.gnd6.CreatePolygonFixture(
            box=(30, 5, (80, -20), math.radians(90)))
        fixture.sensor = True
        self.gnd6.color=Box2D.b2Color(0, 0, 0.7)
        self.gnd6.userData="Pavement"
        self.obs.append(self.gnd6)
        self.grounds.append(self.gnd6)


        self.gnd7 = self.world.CreateStaticBody()
        fixture = self.gnd7.CreatePolygonFixture(
            box=(15, 5, (80,35), math.radians(90)))
        fixture.sensor = True
        self.gnd7.color=Box2D.b2Color(0, 0, 0.7)
        self.gnd7.userData="Pavement"
        self.obs.append(self.gnd7)
        self.grounds.append(self.gnd7)


        return self.step([2,2])[0]

    def step(self, action):
        #a[1] is about gass
        #a[0] is about wheel
        """
            0 = do nothing
            1 = left
            2 = right
            3 = forward
            4 = backward
            5 = forward left
            6 = forward right
            7 = backward left
            8 = backward right
        """    
        keys=[]
        if action == 1 :
            keys.append("left")
        if action == 2 :
            keys.append("right")
        if action == 3 :
            keys.append("up")
        if action == 4 :
            keys.append("down")
        if action == 5 :
            keys.append("up")
            keys.append("left")
        if action == 6 :
            keys.append("up")
            keys.append("right")
        if action == 7 :
            keys.append("down")
            keys.append("left")
        if action ==8 :
            keys.append("down")
            keys.append("right")
        self.car.update(keys,60)
        #run a step of physics simulation
        timeStep = 1.0 / 60 
        vel_iters, pos_iters = 6, 2
        self.world.Step(timeStep, vel_iters, pos_iters)

        self.state=self.render(mode="rgb_array")
        done=False
        reward=-0.1
        #try reward=0 ,+-1
        if self.hasLost==True:
            done=True
            reward=-1000
        if self.checkParking() ==True:
            done=True
            reward=1000
            print("VICTORY")
        
        return self.state,reward,done,{}


    def render(self, mode="human"):
        
        #if mode=="rgb_array":       
        #    arr= self.viewer.get_array()#viewer.render(return_rgb_array=True)
        #    return arr 
        if self.viewer == None:
            from gym.envs.classic_control import rendering

            self.viewer = rendering.Viewer(VIEWPORT_W, VIEWPORT_H)
            self.viewer.set_bounds(-350/SCALE, (VIEWPORT_W-350)/SCALE, -450/SCALE, (VIEWPORT_H-450)/SCALE)


        for obj in self.grounds:
            if obj.userData=="Car":
                continue
            if not hasattr( obj,'fixtures'):
                continue
            for f in obj.fixtures:
                trans = f.body.transform
                if type(f.shape) is b2CircleShape:
                    #if obj.userData=="fuelTank":
                    #    print("rendering Tank")
                    t = rendering.Transform(translation=trans*f.shape.pos)
                    self.viewer.draw_circle(f.shape.radius,color=obj.color).add_attr(t)
                if type(f.shape) is b2EdgeShape:
                    #for v in f.shape.vertices:
                    #    print(v)
                    self.viewer.draw_line(f.shape.vertices[0],f.shape.vertices[1],color=obj.color)
                if type(f.shape) is b2PolygonShape:
                    tv = [trans*v for v in f.shape.vertices]
                    if hasattr(obj,"color"):
                        self.viewer.draw_polygon(tv,color=obj.color)
                    else:
                        self.viewer.draw_polygon(tv)
            #if obj.userData=="fuelTank":
            #    print("rendering Tank")
            for obj in self.tires:
                if not hasattr( obj,'fixtures'):
                    continue
                for f in obj.fixtures:
                    trans = f.body.transform
                    if type(f.shape) is b2CircleShape:
                        #if obj.userData=="fuelTank":
                        #    print("rendering Tank")
                        t = rendering.Transform(translation=trans*f.shape.pos)
                        self.viewer.draw_circle(f.shape.radius,color=obj.color).add_attr(t)
                    if type(f.shape) is b2EdgeShape:
                        #for v in f.shape.vertices:
                        #    print(v)
                        self.viewer.draw_line(f.shape.vertices[0],f.shape.vertices[1],color=obj.color)
                    if type(f.shape) is b2PolygonShape:
                        tv = [trans*v for v in f.shape.vertices]
                        if hasattr(obj,"color"):
                            self.viewer.draw_polygon(tv,color=obj.color)
                        else:
                            self.viewer.draw_polygon(tv)
            for obj in self.cars:
                for f in obj.fixtures:
                    trans = f.body.transform
                    if type(f.shape) is b2CircleShape:
                        #if obj.userData=="fuelTank":
                        #    print("rendering Tank")
                        t = rendering.Transform(translation=trans*f.shape.pos)
                        self.viewer.draw_circle(f.shape.radius,color=obj.color).add_attr(t)
                    if type(f.shape) is b2EdgeShape:
                        #for v in f.shape.vertices:
                        #    print(v)
                        self.viewer.draw_line(
                            f.shape.vertices[0],f.shape.vertices[1],
                            color=obj.color)
                    if type(f.shape) is b2PolygonShape:
                        tv = [trans*v for v in f.shape.vertices]
                        if hasattr(obj,"color"):
                            self.viewer.draw_polygon(tv,color=obj.color)
                        else:
                            self.viewer.draw_polygon(tv)

        if mode=="rgb_array":       
            arr= self.viewer.get_array()#viewer.render(return_rgb_array=True)
            return arr 
        if mode=="human":
            return self.viewer.render()
    def checkParking(self):
        count=0
        for t in self.car.tires:
            for contact in t.body.contacts:
                #help(contact.contact)
                fixture_a = contact.contact.fixtureA
                fixture_b = contact.contact.fixtureB

                body_a, body_b = fixture_a.body, fixture_b.body
                ud_a, ud_b = body_a.userData, body_b.userData
                #print("fookin",ud_a,ud_b)
                if ud_b == "Spot" and ud_a== "Tire":
                    count+=1
                elif ud_a == "Spot" and ud_b=="Tire":
                    count+=1
        #print("fookin count=",count)
        if count==4 and -1 <= self.car.body.linearVelocity[0]<=1:
            return True
        return False
    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None
#######################################################################################

#   CODE BELLOW ONLY USED FOR USER PLAY


########################################################################################
    


if __name__ == "__main__":
    from pyglet.window import key

    a = np.array([2 , 2]) 
    #a[1] is about gass
    #a[0] is about wheel
   
    def key_press(k, mod):
        global restart
        #if k == 0xFF0D:
        #    restart = True
        if k == key.LEFT:
            a[0] = 0
        if k == key.RIGHT:
            a[0] = 1
        if k == key.DOWN:
            a[1] = 0 #backwards
        if k == key.UP:
            a[1] = 1

    def key_release(k, mod):
        if k == key.LEFT and a[0] == 0:
            a[0] = 2
        if k == key.RIGHT and a[0] == 1:
            a[0] = 2
        if k == key.DOWN and a[1]==0:
            a[1] = 2
        if k == key.UP and a[1]==1:
            a[1] = 2

    env = carParking2()
    env.render()
    env.viewer.window.on_key_press = key_press
    env.viewer.window.on_key_release = key_release
    record_video = False
    if record_video:
        from gym.wrappers.monitor import Monitor

        env = Monitor(env, "/tmp/video-test", force=True)
    isopen = True
    while isopen:
        env.reset()
        total_reward = 0.0
        steps = 0
        restart = False
        while True:
            """
            0 = do nothing
            1 = left
            2 = right
            3 = forward
            4 = backward
            5 = forward left
            6 = forward right
            7 = backward left
            8 = backward right
            """ 
            #for stering wheel 
            # 0 means left, 1 means right 2 means nothing
            # for gas
            # 0 means back 1 means forward 2 means nothing
            action=0 
            #left
            if a[0]==0: 
                if a[1]==0: #backwards left
                    action=7
                if a[1]==1: #forward left
                    action=5
                if a[1]==2: #left
                    action=1
            #right
            if a[0]==1:
                if a[1]==0: #backwards right
                    action=8
                if a[1]==1: #forward right
                    action=6
                if a[1]==2:#right
                    action=2
            #no steering
            if a[0]==2:
                if a[1]==0: #backwards
                    action=4
                if a[1]==1:# forward
                    action=3
                if a[1]==2: #nothing
                    action=0
            s, r, done, info = env.step(action)
            total_reward += r
            if steps % 200 == 0 or done:
                print("action= ",a[0],a[1])
                print("step {} total_reward {:+0.2f}".format(steps, total_reward))
            steps += 1
            isopen = env.render()
            if done or restart or isopen == False:
                break
    env.close()
