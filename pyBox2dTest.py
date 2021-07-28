#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.box2d.org
# Python version by Ken Lauer / sirkne at gmail dot com
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from gym.spaces.box import Box
import numpy as np
import cv2
import matplotlib.pyplot as plt
import Box2D
from Box2D.examples.framework import (Framework, Keys, main)
from Box2D.examples.bridge import create_bridge
from Box2D import (b2ContactListener, b2DestructionListener, b2DrawExtended)

from math import sqrt

from Box2D import (b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)
from Box2D import b2Draw


SCALE = 5.0   # affects how fast-paced the game is, forces should be adjusted as well

VIEWPORT_W = 700
VIEWPORT_H = 300
gameOver=False
class myContactListener(b2ContactListener):
    def __init__(self):
        b2ContactListener.__init__(self)
    def BeginContact(self, contact):
        global gameOver
        fixtureA = contact.fixtureA
        bodyA = fixtureA.body
        actorA = bodyA.userData
        bodyB=contact.fixtureB.body
        actorB=bodyB.userData
        if actorA=="Passenger" and actorB=="Ground":
            print("COLISION")
            gameOver=True
        if actorB=="Passenger" and actorA=="Ground":
            print("COLISION")
            gameOver=True
        #print(bodyA,bodyB)
        pass
    def EndContact(self, contact):
        pass
    def PreSolve(self, contact, oldManifold):
        pass
    def PostSolve(self, contact, impulse):
        pass

def renderObjects(obs,viewer):
    for obj in obs:
        if not hasattr( obj,'fixtures'):
            continue
        for f in obj.fixtures:
            trans = f.body.transform
            if type(f.shape) is b2CircleShape:
                t = rendering.Transform(translation=trans*f.shape.pos)
                viewer.draw_circle(f.shape.radius,color=obj.color).add_attr(t)
            if type(f.shape) is b2EdgeShape:
                #for v in f.shape.vertices:
                #    print(v)
                viewer.draw_line(f.shape.vertices[0],f.shape.vertices[1])
            if type(f.shape) is b2PolygonShape:
                #print(f)
                #t = rendering.Transform(translation=trans*f.shape.pos)
                #print("-----------------------------------------------------------------------")
                #print(trans.position)
                #print("-----------------------------------------------------------------------")
                tv = [trans*v for v in f.shape.vertices]
                viewer.draw_polygon(tv)
               
    arr= viewer.render(return_rgb_array=True)
    #print(arr.shape)
    #plt.imshow(arr)
    #plt.show()

    
def create_car(world, offset, wheel_radius, wheel_separation, density=1.0,
               wheel_friction=0.9, scale=(1.0, 1.0), chassis_vertices=None,
               wheel_axis=(0.0, 1.0), wheel_torques=[20.0, 10.0],
               wheel_drives=[True, False], hz=4.0, zeta=0.7, **kwargs):
    """
    """
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



###########main
world=Box2D.b2World(contactListener=myContactListener())


# The ground -- create some terrain
ground = world.CreateStaticBody(
    shapes=b2EdgeShape(vertices=[(-20, 0), (20, 0)])
        )
ground.userData="Ground"
x, y1, dx = 20, 0, 4.5
vertices = [-1,-3,-3,-1,0.25, 0.5,1,2.5, 4,5.5,9.5,7,3, 0, 0, -1, -2, -2, -1.25, 0,0,0]
for y2 in vertices :  # iterate through vertices twice
    ground.CreateEdgeFixture(
        vertices=[(x, y1), (x + dx, y2)],
        density=0,
        friction=0.6,
        )
    y1 = y2
    x += dx
      
      
car, wheels, springs,passenger,seat = create_car(world, offset=(
            0.0, 1.0), wheel_radius=0.4, wheel_separation=2.0, scale=(1, 1))
#for fuck in car.fixtures:
#    print(fuck)
#help(car)
print("Car Created")
obs=[]
obs.append(car)
obs.append(ground)
for w in wheels:
    obs.append(w)
for s in springs:
    obs.append(s)
obs.append(passenger)
from gym.envs.classic_control import rendering
viewer = rendering.Viewer(VIEWPORT_W, VIEWPORT_H)
viewer.set_bounds(-20/5.0, (VIEWPORT_W-20)/5.0, -40/5.0, (VIEWPORT_H-40)/5.0)

#renderObjects(obs,viewer)


# Prepare for simulation. Typically we use a time step of 1/60 of a
# second (60Hz) and 6 velocity/2 position iterations. This provides a 
# high quality simulation in most game scenarios.
timeStep = 1.0 / 60
vel_iters, pos_iters = 6, 2
# This is our little game loop.
for i in range(6000):
    # Instruct the world to perform a single step of simulation. It is
    # generally best to keep the time step and iterations fixed.
    springs[0].motorSpeed=-95.0
    world.Step(timeStep, vel_iters, pos_iters)
    # Clear applied body forces. We didn't apply any forces, but you
    # should know about this function.
    #world.ClearForces()
 
    # Now print the position and angle of the body.
    #print(car.position, car.angle)
    renderObjects(obs,viewer)
    #print("---------------------springs---------------------------------------------")
    #print(car.angle)
    #print("wheels[0]",wheels[0].transform.position)
    #print("wheels[1]",wheels[1].transform.position)
    #print("car",car.transform.position)
    cary=car.transform.position[1]
    wheel0y=wheels[0].transform.position[1]
    wheel1y=wheels[1].transform.position[1]
    wheel0x=wheels[0].transform.position[0]
    wheel1x=wheels[1].transform.position[0]
    #print(car.GetLocalPoint((0,0)))
    #print(car.linearVelocity)
    #print("---------------------------------------------------------------------")

    #print(passenger)        
    #for f in ground.fixtures:
    #    if f in passenger.contacts:
    #        break
    #print("-------------------------------------------------------------------------")
    if gameOver:
        break
print("GAME OVER")