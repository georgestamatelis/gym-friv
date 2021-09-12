#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Based on Chris Campbell's tutorial from iforce2d.net:
http://www.iforce2d.net/b2dtut/top-down-car
"""

from Box2D.examples.framework import (Framework, Keys, main)
from Box2D import (b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)
import math





class spinSoccer (Framework):
    name = "Spin Soccer"

    def __init__(self):
        super(spinSoccer, self).__init__()
        self.world.gravity=(0.0,-20.0)
        self.key_map = {Keys.K_w: 'up',
                        Keys.K_s: 'down',
                        
                        }

        # Keep track of the pressed keys
        self.pressed_keys = set()

        # The walls
        #boundary = self.world.CreateStaticBody(position=(0, 20))
        """
        boundary.CreateEdgeChain([(-30, -30),
                                  (-30, 30),
                                  (30, 30),
                                  (30, -30),
                                  (-30, -30),
                                  
                                  ]
        )
        """    
        #ground                  
        ground=self.world.CreateStaticBody(position=(0,0))
        ground_vertices = [
                (-20,10),
                (20,10),
                (-20,-30),
                (20,-30)
            ]
        ground.CreateFixture(b2FixtureDef(
                shape=b2PolygonShape(vertices=ground_vertices)))
        ground.userData="ground"
        #goal post
        goalPost=self.world.CreateStaticBody(position=(-10,0))
        goalPost_vertices = [
            (-10,10),
            (-10,20),
            (-7.5,10),
            (-7.5,20)
        ]
        goalPost.CreateFixture(b2FixtureDef(
                shape=b2PolygonShape(vertices=goalPost_vertices)))
        goalPost.CreateFixture(b2FixtureDef(
                shape=b2PolygonShape(vertices=[ 
                    (-7.5,20),
                    (-7.5,17.5),
                    (-5,20),
                    (-5,17.5)
                ])))
        goalPost.userData="goalPost"
        
        # Teeter platform on which we will put the ball
        
        body = self.world.CreateDynamicBody(
            position=(20, 29.75),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(10, 0.25)),
                density=1.0,
            )
        )
        """background=self.world.CreateStaticBody(position=(0,0))
        background.CreateFixture(b2FixtureDef(
                shape=b2PolygonShape(vertices=[ 
                    (19,30),
                    (19,29.75),
                    (20.5,30),
                    (20.5,29.75)
                ])))
        """
        self.joint=self.world.CreateRevoluteJoint(
            bodyA=ground,
            bodyB=body,
            anchor=body.position,
            lowerAngle=-2.0 * b2_pi,
            upperAngle=2.0* b2_pi ,
            enableLimit=False,
            motorSpeed =0,
            maxMotorTorque =   10000000,
            enableMotor =True
        )
        #ball

        self.ball=self.world.CreateDynamicBody(
            position=(20,31),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=1),
                density=2.0,
            )

        )
        self.ball.userData="ball"


    def Keyboard(self, key):
        if key == Keys.K_a: #spin left
            self.joint.motorSpeed=1.5
        elif key == Keys.K_d: #spin right
            self.joint.motorSpeed=-1.5
        else:
            self.joint.motorSpeed=0
 
     
        

    def KeyboardUp(self, key):
        self.joint.motorSpeed=0


    def handle_contact(self, contact, began):
        # A contact happened -- see if a wheel hit a
        # ground area
        fixture_a = contact.fixtureA
        fixture_b = contact.fixtureB

        body_a, body_b = fixture_a.body, fixture_b.body
        ud_a, ud_b = body_a.userData, body_b.userData
        if not ud_a or not ud_b:
            return

        """tire = None
        ground_area = None
        for ud in (ud_a, ud_b):
            obj = ud['obj']
            if isinstance(obj, TDTire):
                tire = obj
            elif isinstance(obj, TDGroundArea):
                ground_area = obj

        if ground_area is not None and tire is not None:
            if began:
                tire.add_ground_area(ground_area)
            else:
                tire.remove_ground_area(ground_area)

    def BeginContact(self, contact):
        self.handle_contact(contact, True)

    def EndContact(self, contact):
        self.handle_contact(contact, False)

    def Step(self, settings):
        self.car.update(self.pressed_keys, settings.hz)
        super(TopDownCar, self).Step(settings)

        tractions = [tire.current_traction for tire in self.car.tires]
        self.Print('Current tractions: %s' % tractions)
    """

if __name__ == "__main__":
    main(spinSoccer)