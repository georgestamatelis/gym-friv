"""
http://incompleteideas.net/sutton/MountainCar/MountainCar1.cp
permalink: https://perma.cc/6Z2N-PFWC
"""
import math,sys

import numpy as np

import Box2D
#from Box2D.b2 import (edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener)
from Box2D import (b2ContactListener, b2DestructionListener, b2DrawExtended)
from Box2D import (b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)
from math import sqrt
from gym.envs.classic_control import rendering

import gym
from gym import spaces
from gym.utils import seeding,EzPickle
import pyglet

pyglet.options["debug_gl"] = False
from pyglet import gl


class myContactListener(b2ContactListener):
    def __init__(self,env):
        b2ContactListener.__init__(self)
        self.env=env
    def BeginContact(self, contact):
        fixtureA = contact.fixtureA
        bodyA = fixtureA.body
        actorA = bodyA.userData
        bodyB=contact.fixtureB.body
        actorB=bodyB.userData
        if actorA=="Passenger" and actorB=="Ground":
            print("COLISION")
            self.env.gameOver=True
        if actorB=="Passenger" and actorA=="Ground":
            print("COLISION")
            self.env.gameOver=True
        #print(bodyA,bodyB)
        pass
    def EndContact(self, contact):
        pass
    def PreSolve(self, contact, oldManifold):
        pass
    def PostSolve(self, contact, impulse):
        pass


SCALE = 5.0   # affects how fast-paced the game is, forces should be adjusted as well


VIEWPORT_W = 700
VIEWPORT_H = 300

FPS=50
class Hill_Climber_Env(gym.Env,EzPickle):
   

    metadata = {
        "render.modes": ["human", "rgb_array", "state_pixels"],
        "video.frames_per_second": FPS,
    }

    def __init__(self, goal_velocity=0):
       
        EzPickle.__init__(self)
        self.seed()
        #self.viewer = None
        
        self.viewer = rendering.Viewer(VIEWPORT_W, VIEWPORT_H)
        self.viewer.set_bounds(-20/5.0, (VIEWPORT_W-20)/5.0, -40/5.0, (VIEWPORT_H-40)/5.0)
        self.contactListener=myContactListener(self)
        self.world = Box2D.b2World(contactListener=self.contactListener)

        self.prev_reward = None

        self.observation_space = spaces.Box(low=0,high=255,shape=(VIEWPORT_H, VIEWPORT_W, 3), dtype=np.uint8)

        #possible actions are : [do nothing,stop,left,right]
        self.action_space = spaces.Discrete(4)

        self.obs=[]
        self.springs=[]
        self.wheels=[]
        #self.reset()


    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
    """ ACTION MAPING
    0 = STOP
    1 = ACCELERATE LEFT
    2 = ACCELERATE RIGHT
    3 = DO NOTHING
    """
    def step(self, action):
        """
        """
        timeStep = 1.0 / 60
        vel_iters, pos_iters = 6, 2
        if action==0: 
            self.springs[0].motorSpeed=0 
        if action==1: 
            self.springs[0].motorSpeed=50.0
        if action==2: 
            self.springs[0].motorSpeed=-50.0 
        self.world.Step(timeStep, vel_iters, pos_iters)
        #print("step")
        self.state=self.render(mode="rgb_array")
        done=False
        reward=0#.1
        if self.gameOver: #colision
            done=True
            reward=-1
        if self.car.GetLocalPoint((0,0))[0] <=-110: #finished track
            done=True
            reward=1
        self.timeStep+=1
        if self.timeStep >=1200: #time/gas out
            done=True
            reward=-1
        return self.state,reward,done,{}

    def destroy(self):
        """
            need to fix this
        """
        self.gameOver=False
        if not self.obs:
            return
        self.world.DestroyJoint(self.seat)
        for s in self.springs:
            self.world.DestroyJoint(s)
        for f in self.car.fixtures:
            self.car.DestroyFixture(f)
        self.world.DestroyBody(self.car)
        for f in self.ground.fixtures:
            self.ground.DestroyFixture(f)
        self.world.DestroyBody(self.ground)
        self.world.DestroyBody(self.passenger)
        for w in self.wheels:
            self.world.DestroyBody(w)

    def reset(self):
        self.destroy()
        # The ground -- create some terrain
        self.ground = self.world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(-20, 0), (20, 0)])
        )
        self.ground.userData="Ground"
        x, y1, dx = 20, 0, 4.5
        vertices = [-1,-3,-3,-1,0.25, 0.5,1,2.5, 4,5.5,9.5,7,3, 0, 0, -1, -2, -2, -1.25, 0,0,0]
        for y2 in vertices :  # iterate through vertices twice
            self.ground.CreateEdgeFixture(
                vertices=[(x, y1), (x + dx, y2)],
                density=0,
                friction=0.6,
                )
            y1 = y2
            x += dx
      
      
        self.car,self.wheels, self.springs,self.passenger,self.seat = self.create_car(self.world, offset=(
            0.0, 1.0), wheel_radius=0.4, wheel_separation=2.0, scale=(1, 1))
        self.obs=[]
        self.obs.append(self.car)
        self.obs.append(self.ground)
        for w in self.wheels:
            self.obs.append(w)
        for s in self.springs:
            self.obs.append(s)
        self.obs.append(self.passenger)        
        self.timeStep=0
        return self.step(None)[0]

    def render(self, mode="human"):
        
        #if mode=="rgb_array":       
        #    arr= self.viewer.get_array()#viewer.render(return_rgb_array=True)
        #    return arr 
        for obj in self.obs:
            if not hasattr( obj,'fixtures'):
                continue
            for f in obj.fixtures:
                trans = f.body.transform
                if type(f.shape) is b2CircleShape:
                    t = rendering.Transform(translation=trans*f.shape.pos)
                    self.viewer.draw_circle(f.shape.radius,color=obj.color).add_attr(t)
                if type(f.shape) is b2EdgeShape:
                    #for v in f.shape.vertices:
                    #    print(v)
                    self.viewer.draw_line(f.shape.vertices[0],f.shape.vertices[1])
                if type(f.shape) is b2PolygonShape:
                    tv = [trans*v for v in f.shape.vertices]
                    self.viewer.draw_polygon(tv)
        
        if mode=="rgb_array":       
            arr= self.viewer.get_array()#viewer.render(return_rgb_array=True)
            return arr 
        if mode=="human":
            return self.viewer.render()
       
    def get_keys_to_action(self):
        # Control with left and right arrow keys.
        return {(): 1, (276,): 0, (275,): 2, (275, 276): 1}

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
    def create_car(self,world, offset, wheel_radius, wheel_separation, density=1.0,
               wheel_friction=0.9, scale=(1.0, 1.0), chassis_vertices=None,
               wheel_axis=(0.0, 1.0), wheel_torques=[20.0, 10.0],
               wheel_drives=[True, False], hz=4.0, zeta=0.7, **kwargs):
    
        x_offset, y_offset = offset
        scale_x, scale_y = scale
        if chassis_vertices is None:
            chassis_vertices = [
                (-1.5, -0.5),
                (1.5, -0.5),
                (1.5, 0.0),
                (0.0, 0.9),
                (-1.15, 0.9),
                (-1.5, 0.2),
            ]

        chassis_vertices = [(scale_x * x, scale_y * y)
                        for x, y in chassis_vertices]
        radius_scale = sqrt(scale_x ** 2 + scale_y ** 2)
        wheel_radius *= radius_scale

        chassis = world.CreateDynamicBody(
            position=(x_offset, y_offset),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(vertices=chassis_vertices),
                density=density,
            )
        )
    
    
        passenger = world.CreateDynamicBody(
            position=(x_offset, y_offset+0.9),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=wheel_radius),
                density=density/25
            )

        )
        passenger.userData="Passenger"
        passenger.color=Box2D.b2Color(0.9, 0.2, 0.2)
        seat=world.CreateRevoluteJoint(
            bodyA=chassis,
            bodyB=passenger,
            anchor=passenger.position,
            #type=Box2D.b2Joint
        )
    
        wheels, springs = [], []
        wheel_xs = [-wheel_separation * scale_x /
                2.0, wheel_separation * scale_x / 2.0]
        for x, torque, drive in zip(wheel_xs, wheel_torques, wheel_drives):
            wheel = world.CreateDynamicBody(
                position=(x_offset + x, y_offset - wheel_radius),
                fixtures=b2FixtureDef(
                    shape=b2CircleShape(radius=wheel_radius),
                    density=density,
                )
            )
            wheel.color=Box2D.b2Color(0.5, 0.8, 0.8)

            spring = world.CreateWheelJoint(
                bodyA=chassis,
                bodyB=wheel,
                anchor=wheel.position,
                axis=wheel_axis,
                motorSpeed=0.0,
                maxMotorTorque=torque,
                enableMotor=drive,
                frequencyHz=hz,
                dampingRatio=zeta
            )

            wheels.append(wheel)
            springs.append(spring)
        return chassis, wheels, springs,passenger,seat
