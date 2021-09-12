import math,sys

import numpy as np
import random

import Box2D
#from Box2D.b2 import (edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener)
from Box2D import (b2ContactListener, b2DestructionListener, b2DrawExtended)
from Box2D import (b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)
from Box2D.examples.bridge import create_bridge
import cv2

from math import sqrt
from gym.envs.classic_control import rendering

import gym
from gym import spaces
from gym.utils import seeding,EzPickle
import pyglet

pyglet.options["debug_gl"] = False
from pyglet import gl


#THIS CLASS DEALS WITH COLISION DETECTION
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
        
        if (actorA=="ball" and actorB=="goalPost") or (actorA=="goalPost" and actorB=="ball"):
            self.env.scoredGoal=True       
    def EndContact(self, contact):
        pass
    def PreSolve(self, contact, oldManifold):
        pass
    def PostSolve(self, contact, impulse):
        pass
VIEWPORT_W = 500
VIEWPORT_H = 500
STATE_W= 100
STATE_H = 100
FPS=1
class spinSoccerEnv2(gym.Env,EzPickle):
   

    metadata = {
        "render.modes": ["human", "rgb_array", "state_pixels"],
        "video.frames_per_second": FPS,
    }
    def __init__(self):
       
        EzPickle.__init__(self)
        self.seed()

        self.viewer = rendering.Viewer(VIEWPORT_W, VIEWPORT_H)
        self.contactListener=myContactListener(self)

        self.world = Box2D.b2World(contactListener=self.contactListener)
        self.world.gravity=(0.0,-20.0)

        self.observation_space = spaces.Box(low=0,high=255,shape=(STATE_H, STATE_H, 3), dtype=np.uint8)

        """
        actions are :
        0 do nothing 
        1 spin(all platforms) counterClock wise
        2 spin(all platforms) clock wise 
        """
       
        self.action_space = spaces.Discrete(3)

        """
        BUILDING THE STATIC BODIES IN HERE SINCE THEY DO NOT CHANGE
        """
        #obs contain all objects to draw 
        #dynamicObs contains dynamic objects to create/destroy
        self.obs=[]
        #ground                  
        self.ground=self.world.CreateStaticBody(position=(0,0))
        ground_vertices = [
                (200,100),
                (350,100),
                (200,125),
                (350,125)
            ]
        self.ground.CreateFixture(b2FixtureDef(
                shape=b2PolygonShape(vertices=ground_vertices)))
        self.ground.CreateFixture(b2FixtureDef(
            shape=b2PolygonShape(
                vertices=[
                   (175,200),
                   (175,225),
                   (375,200),
                   (375,225) 
                ]
            )
        ))
        self.ground.color=Box2D.b2Color(0, 0, 0)
        self.ground.userData="ground"
        self.obs.append(self.ground)
        #goal post
        self.goalPost=self.world.CreateStaticBody(position=(0,0))
        goalPost_vertices = [
            (335,125),
            (335,170),
            (350,170),
            (350,125)
        ]
        self.goalPost.CreateFixture(b2FixtureDef(
                shape=b2PolygonShape(vertices=goalPost_vertices)))
        self.goalPost.userData="goalPost"
        self.obs.append(self.goalPost)
        
        self.topGoalPost=self.world.CreateStaticBody(position=(0,0))
        self.topGoalPost.CreateFixture(b2FixtureDef(
                shape=b2PolygonShape(vertices=[ 
                    (335,170),
                    (335,155),
                    (320,170),
                    (320,155)
                ])))
        self.obs.append(self.topGoalPost)

        self.dynamicObs=[]
    def destroy(self):
        if not self.dynamicObs:
            return
        #destroy joint

        self.world.DestroyJoint(self.joint)
        self.world.DestroyJoint(self.joint2)
        self.world.DestroyJoint(self.joint3)

        #destroy teeters
        for f in self.body.fixtures:
            self.body.DestroyFixture(f)
        self.world.DestroyBody(self.body)
        self.obs.remove(self.body)
        for f in self.body2.fixtures:
            self.body2.DestroyFixture(f)
        self.world.DestroyBody(self.body2)
        self.obs.remove(self.body2)

        for f in self.body3.fixtures:
            self.body3.DestroyFixture(f)
        self.world.DestroyBody(self.body3)
        self.obs.remove(self.body3)


        #destroy ball
        for f in self.ball.fixtures:
            self.ball.DestroyFixture(f)
        self.world.DestroyBody(self.ball)
        self.obs.remove(self.ball)

        
        self.dynamicObs=[]

    def reset(self):

        self.timeSteps=0
         # Teeter platform on which we will put the ball
        self.destroy()
        self.dynamicObs=[]
        self.scoredGoal=False
        # first Teeter platform on which we will put the ball
        self.body = self.world.CreateDynamicBody(
            position=(415,325),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(40, 2.5)),
                density=1.0,
            )
        )
        self.body.color=Box2D.b2Color(0.0, 0.2, 0.6)
        self.obs.append(self.body)
        self.dynamicObs.append(self.body)
        
        self.joint=self.world.CreateRevoluteJoint(
            bodyA=self.ground,
            bodyB=self.body,
            anchor=self.body.position,
            lowerAngle=-2.0 * b2_pi,
            upperAngle=2.0* b2_pi ,
            enableLimit=False,
            motorSpeed =0,
            maxMotorTorque =   10000000,
            enableMotor =True
        )
        self.dynamicObs.append(self.joint)

        #second Teeter platform on which we will put the ball
        self.body2 = self.world.CreateDynamicBody(
            position=(125,225),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(40, 2.5)),
                density=1.0,
            )
        )
        self.body2.color=Box2D.b2Color(0.0, 0.2, 0.6)
        self.obs.append(self.body2)
        self.dynamicObs.append(self.body2)
        
        self.joint2=self.world.CreateRevoluteJoint(
            bodyA=self.ground,
            bodyB=self.body2,
            anchor=self.body2.position,
            lowerAngle=-2.0 * b2_pi,
            upperAngle=2.0* b2_pi ,
            enableLimit=False,
            motorSpeed =0,
            maxMotorTorque =   10000000,
            enableMotor =True
        )
        self.dynamicObs.append(self.joint2)

        #third teeter
        self.body3 = self.world.CreateDynamicBody(
            position=(150,145),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(2.5, 40)),
                density=1.0,
            )
        )
        self.body3.color=Box2D.b2Color(0.0, 0.2, 0.6)
        self.obs.append(self.body3)
        self.dynamicObs.append(self.body3)
        
        self.joint3=self.world.CreateRevoluteJoint(
            bodyA=self.ground,
            bodyB=self.body3,
            anchor=self.body3.position,
            lowerAngle=-2.0 * b2_pi,
            upperAngle=2.0* b2_pi ,
            enableLimit=False,
            motorSpeed =0,
            maxMotorTorque =   10000000,
            enableMotor =True
        )
        self.dynamicObs.append(self.joint3) 


        #ball

        self.ball=self.world.CreateDynamicBody(
            position=(415,335),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=10),
                density=3.0,
            )

        )
        self.ball.userData="ball"
        self.ball.color=Box2D.b2Color(0.9, 0, 0)
        self.dynamicObs.append(self.ball)
        self.obs.append(self.ball)

        return self.step(None)[0]



    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
   

    def step(self, action):
        """
        actions are :
        0 do nothing 
        1 spin(all platforms) counterClock wise
        2 spin(all platforms) clock wise 
        """
        self.timeSteps+=1
        if action==1:
            self.joint.motorSpeed=1.5
            self.joint2.motorSpeed=1.5
            self.joint3.motorSpeed=1.5

        elif action==2:
            self.joint.motorSpeed=-1.5
            self.joint2.motorSpeed=-1.5
            self.joint3.motorSpeed=-1.5
        else:
            self.joint.motorSpeed=0
            self.joint2.motorSpeed=0
            self.joint3.motorSpeed=0
        timeStep = 1.0/40
        vel_iters, pos_iters = 6, 3
        for i in range(3):
            self.world.Step(timeStep, vel_iters, pos_iters)
            self.world.ClearForces()

        state=self.render(mode="rgb_array")
        done=False
        reward=0
        if self.scoredGoal==True and self.ball.position[1]<=255:
            done=True
            reward=1
            print("GOAL")
        if self.ball.position[1] <=0 or self.ball.position[0]<=0 or self.ball.position[0]>=500:
            done=True
            reward=-0.7
            print("LOSS")
        if self.timeSteps >=1000:
            print("TIME OUT")
            done=True
            reward=-1
        return state,reward,done,{}
    

        
    def render(self, mode="human"):
        
        #pyglet.gl.glClearColor(0.5,0,0,1) # Note that these are values 0.0 - 1.0 and not (0-255).

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
                    if hasattr(obj,'color'):
                        self.viewer.draw_polygon(tv,color=obj.color)
                    else:
                        self.viewer.draw_polygon(tv)
            
        if mode=="rgb_array":       
            arr= self.viewer.render(return_rgb_array=True)
            arr=cv2.resize(arr,(STATE_H,STATE_W))
            return arr 
        if mode=="human":
            return self.viewer.render()
    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

"""""""""""""""""""""
HUMAN GAME PLAY
"""""""""""""""""""""
"""
    actions are :
    0 do nothing 
    1 spin(all platforms) counterClock wise
    2 spin(all platforms) clock wise 
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
      

    def key_release(k, mod):
        if k == key.LEFT and a == 1:
            a[0] = 0
        if k == key.RIGHT and a == 2:
            a[0] = 0
        

    env = spinSoccerEnv2()
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
                s=env.reset()
    env.close()
