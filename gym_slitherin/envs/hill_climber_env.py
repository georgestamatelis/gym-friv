"""
http://incompleteideas.net/sutton/MountainCar/MountainCar1.cp
permalink: https://perma.cc/6Z2N-PFWC
"""
import math,sys

import numpy as np
import random

import Box2D
#from Box2D.b2 import (edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener)
from Box2D import (b2ContactListener, b2DestructionListener, b2DrawExtended)
from Box2D import (b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)
from Box2D.examples.bridge import create_bridge

from math import sqrt
from gym.envs.classic_control import rendering

import gym
from gym import spaces
from gym.utils import seeding,EzPickle
import pyglet

pyglet.options["debug_gl"] = False
from pyglet import gl

#THIS CLASS TAKES CARE OF COLLISION DETECTION AND COLISSION RESOLUTION

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
        
    def EndContact(self, contact):
        pass
    #just before colision => destroy fuel tanks without slowing down the car
    def PreSolve(self, contact, oldManifold):
        fixtureA = contact.fixtureA
        bodyA = fixtureA.body
        actorA = bodyA.userData
        bodyB=contact.fixtureB.body
        actorB=bodyB.userData
        if ((actorA=="Car" or actorA=="wheel")  and actorB=="fuelTank") or (actorA=="fuelTank" and (actorB=="Car" or actorB=="wheel")):
            self.env.fuelLeft=5000
            if actorB=="fuelTank":
                self.env.toDestroy.append(bodyB)
            else:
                self.env.toDestroy.append(bodyA)
            contact.enabled=False
    def PostSolve(self, contact, impulse):
        pass


SCALE = 17.5   # affects how fast-paced the game is, forces should be adjusted as well


VIEWPORT_W = 700
VIEWPORT_H = 500

FPS=60
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
        self.viewer.set_bounds(-20/SCALE, (VIEWPORT_W-20)/SCALE, -150/SCALE, (VIEWPORT_H-150)/SCALE)
        self.contactListener=myContactListener(self)
        self.world = Box2D.b2World(contactListener=self.contactListener)

        self.prev_reward = None

        self.observation_space = spaces.Box(low=0,high=255,shape=(VIEWPORT_H, VIEWPORT_W, 3), dtype=np.uint8)

        #possible actions are : [do nothing,stop,left,right]
        self.action_space = spaces.Discrete(4)

        self.obs=[]
        self.springs=[]
        self.wheels=[]
        self.fuelTanks=[]
        #self.reset()
        self.ground = self.world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(-20, 0), (0, 0)])
            )
        self.ground.userData="Ground"

        self.groundEnd=0
        self.toDestroy=[]

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
        self.fuelLeft-=1 #remove a little fuel
        timeStep = 1.0 / 60 
        vel_iters, pos_iters = 6, 2
        #action are nothing,breaks,speed,reverse
        if action==0:  #break
            self.springs[0].motorSpeed=0 
        if action==1: #gass
            self.springs[0].motorSpeed=5000.0
        if action==2:  #reverse
            self.springs[0].motorSpeed=-5000.0 
        #make sure the car stays in the screen first
        self.viewer.transform.set_translation(-SCALE*(
            self.car.worldCenter[0]-20.0),
            self.viewer.transform.translation[1])
        #Run a step of physics simulation
        self.world.Step(timeStep, vel_iters, pos_iters)
        reward=self.car.worldCenter[0] #reward is how far the car has traveled
        #if the object has collided with a fuel tank, remove the tank
        for obj in self.toDestroy:
            for f in obj.fixtures:
                obj.DestroyFixture(f)
            for tank in self.fuelTanks:
                if tank==obj:
                    #print("found")
                    self.world.DestroyBody(tank) 
                    self.fuelTanks.remove(tank)       
        self.toDestroy=[]
        self.state=self.render(mode="rgb_array")
        done=False
        
        carx=self.car.worldCenter[0]
        if self.groundEnd-carx <=50:
            #print("CREATING GROUND")
            self.createGround()
        #print("fuel left=",self.fuelLeft)
        self.timeStep+=1
        if self.car.worldCenter[0] <=-20: #Car fell of
            done=True 
        if self.gameOver: #colision
            done=True
        if self.timeStep >=100000: #make sure episodes dont run forever
            done=True
            #reward=-1
        if self.fuelLeft<0: #out of fuel
            done=True
            #print("out of time")
        #print("reward=",reward,"action=",action)
        return self.state,reward,done,{}
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
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
        print("destroyed joints")
        for f in self.car.fixtures:
            self.car.DestroyFixture(f)
        self.world.DestroyBody(self.car)
        print("destroyed car")
        for f in self.ground.fixtures:
            self.ground.DestroyFixture(f)
        self.world.DestroyBody(self.ground)
        print("Destroyed ground ")
        self.world.DestroyBody(self.passenger)
        print("destroyed passenger")
        for w in self.wheels:
            self.world.DestroyBody(w)
        print("destroyed wheels")
        for tank in self.fuelTanks:
            for f in tank.fixtures:
                tank.DestroyFixture(f)
            self.world.DestroyBody(tank)
        self.fuelTanks=[]
    def createGround(self):
        # The ground -- create some terrain
        x, y1, dx = self.groundEnd, 0, 4.5
        
        for i in range(15):
            numVerticises=random.randint(5,30)

        if numVerticises % 2 >0 :
            numVerticises+=1
        vertices=[0 for i in range(numVerticises+2)]
        vertices[0]=0
        #vertices[1]=0
        disturbanceX=random.uniform(-0.5,1)
        disturbanceY=random.uniform(-1,3)
        disturbanceY2=random.uniform(-0.5,1)
        for j in range(1,numVerticises,2):
            #print("fook")
            vertices[j]=random.uniform(-1,4.5)
            vertices[j+1]=vertices[j]+disturbanceY
            #print(vertices[j])
        vertices[numVerticises]=0
        #vertices[numVerticises+1]=0
        for y2 in vertices *2 :  # iterate through vertices twice
    
            self.ground.CreateEdgeFixture(
                vertices=[(x, y1), (x + dx, y2)],
                density=0,
                friction=0.6,
            )
            y1 = y2
            x += dx
        self.groundEnd=x
        
        fuelTank=self.world.CreateKinematicBody(
            position=(x, y1+1),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=1),
                density=0.0001
            )
        )
        #print("FUEL TANK CREATED AT ",x,y1+1)
        fuelTank.userData="fuelTank"
        fuelTank.color=Box2D.b2Color(0.9, 0, 0)
        self.obs.append(fuelTank)
        self.fuelTanks.append(fuelTank)
        
    def reset(self):
        self.destroy()
        self.fuelLeft=5000
        self.obs=[]
        # The ground -- create some terrain
        random.seed(185)
        self.ground = self.world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(-20, 0), (0, 0)])
            )
        fuelTank=self.world.CreateKinematicBody(
            position=(5, 1),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=1),
                density=0.0001
            )
        )
        #print("FUEL TANK CREATED AT ",5,1)
        fuelTank.userData="fuelTank"
        fuelTank.color=Box2D.b2Color(0.9, 0, 0)
        self.obs.append(fuelTank)
        self.fuelTanks.append(fuelTank)
        self.ground.userData="Ground"
        self.groundEnd=0
        self.createGround()
        self.car,self.wheels, self.springs,self.passenger,self.seat = self.create_car(self.world, offset=(
            0.0, 1.0), wheel_radius=0.4, wheel_separation=2.0, scale=(1, 1))
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
                    #if obj.userData=="fuelTank":
                    #    print("rendering Tank")
                    t = rendering.Transform(translation=trans*f.shape.pos)
                    self.viewer.draw_circle(f.shape.radius,color=obj.color).add_attr(t)
                if type(f.shape) is b2EdgeShape:
                    #for v in f.shape.vertices:
                    #    print(v)
                    self.viewer.draw_line(f.shape.vertices[0],f.shape.vertices[1])
                if type(f.shape) is b2PolygonShape:
                    tv = [trans*v for v in f.shape.vertices]
                    self.viewer.draw_polygon(tv)
            #if obj.userData=="fuelTank":
            #    print("rendering Tank")
        
        if mode=="rgb_array":       
            arr= self.viewer.get_array()#viewer.render(return_rgb_array=True)
            return arr 
        if mode=="human":
            return self.viewer.render()
       

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
    
        chassis.userData="Car"
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
            wheel.userData="wheel"
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
"""""""""""""""""""""
HUMAN GAME PLAY
"""""""""""""""""""""
""" ACTION MAPING
    0 = STOP
    1 = ACCELERATE LEFT
    2 = ACCELERATE RIGHT
    3 = DO NOTHING
"""
if __name__ == "__main__":
    from pyglet.window import key

    a = np.array([3]) #do nothing
    def key_press(k, mod):
        global restart
        #if k == 0xFF0D:
        #    restart = True
        if k == key.LEFT:
            a[0] = 1
        if k == key.RIGHT:
            a[0] = 2
        if k == key.DOWN:
            a[0] = 0 #stop

    def key_release(k, mod):
        if k == key.LEFT and a == 1:
            a[0] = 3
        if k == key.RIGHT and a == 2:
            a[0] = 3
        #if k == key.DOWN:
        #    a = 0

    env = Hill_Climber_Env()
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
            s, r, done, info = env.step(a[0])
            total_reward += r
            if steps % 200 == 0 or done:
                print("action= ",a[0])
                print("step {} total_reward {:+0.2f}".format(steps, total_reward))
            steps += 1
            isopen = env.render()
            if done or restart or isopen == False:
                break
    env.close()
