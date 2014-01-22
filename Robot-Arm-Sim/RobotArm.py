

import pygame
from pygame.locals import *

import Box2D # The main library
from Box2D.b2 import * # This maps Box2D.b2Vec2 to vec2 (and so on)
b2_pi=3.14159265359


class TriJointArm:
	def __init__( self, box2Dworld, initPos ):
		self.mWorld = box2Dworld;
		self.mLength = 10.0;
		self.mInitPos = initPos;

		self.mBase = self.mWorld.CreateStaticBody( position = self.mInitPos, angle = 0 )
		self.mBase.CreatePolygonFixture( box = ( 10, 2 ),  density = 1, friction=0.3 );

		self.mColors = [(51,153,255,255),(128,255,0,255),(255,153,51,255)]

		self.mSkelentons = []
		self.mJoints = []

		# Craete the first skelenton
		pos = (self.mInitPos[0], self.mInitPos[1]+self.mLength/2+2)
		sktOne = self.mWorld.CreateStaticBody( position = pos, angle = 0 ) 
		sktOne.CreatePolygonFixture( box = (1,self.mLength), density = 0.1, friction=0.0 );
		self.mSkelentons = self.mSkelentons + [sktOne]
		#Joint the base and the first skeleton
		joint1 = self.mWorld.CreateRevoluteJoint( bodyA = self.mBase, bodyB = sktOne, 
			anchor = self.mBase.worldCenter, 
			lowerAngle = -0.5 * b2_pi, supperAngle = 0.5 * b2_pi,
			enableMotor = True, enableLimit = True, maxMotorTorque = 1000.0, referenceAngle = 10
			);


		# Craete the second skelenton
		pos = (self.mInitPos[0], self.mInitPos[1]+(self.mLength)*(1.5)+10)
		jointPos = (pos[0],pos[1]-1*self.mLength)
		sktTwo = self.mWorld.CreateDynamicBody( position = pos, angle = 0 ) 
		sktTwo.CreatePolygonFixture( box = (1,self.mLength+1), density = 0.1, friction=0.0 );
		self.mSkelentons = self.mSkelentons + [sktTwo]
		#Joint the base and the second skeleton
		joint2 = self.mWorld.CreateRevoluteJoint( bodyA = sktOne, bodyB = sktTwo, anchor = jointPos);
		
		
		# Craete the third skelenton
		pos = (self.mInitPos[0], self.mInitPos[1]+(self.mLength+8)*(2.5))
		jointPos = (pos[0],pos[1]-1*self.mLength)
		sktThree = self.mWorld.CreateDynamicBody( position = pos, angle = 0 ) 
		sktThree.CreatePolygonFixture( box = (1,self.mLength+1), density = 0.1, friction=0.0 );
		self.mSkelentons = self.mSkelentons + [sktThree]
		#Joint the base and the second skeleton
		joint3 = self.mWorld.CreateRevoluteJoint( bodyA = sktTwo, bodyB = sktThree, anchor = jointPos );
		joint3.motorSpeed = -10
		self.mJoints = self.mJoints + [joint1, joint2, joint3];

		#pos = (self.mInitPos[0]-5, self.mInitPos[1]+(self.mLength+8)*(3.5))
		#sktThree = self.mWorld.CreateDynamicBody( position = pos, angle = 0.2*b2_pi ) 
		#sktThree.CreatePolygonFixture( box = (3,3), density = 1, friction=0.3 );

	def collisionDetection( self, obstacles ):
		return;

	def updateJoints( self, angle1, angle2, angle3 ):
		self.mJoints[0].referenceAngle = angle1;
		return;


		angleError = self.mJoints[0].angle - angle1
		gain = 0.1
		self.mJoints[0].motorSpeed = (-gain * angleError)
		
		if( self.mJoints[1].angle > angle2 ):
			self.mJoints[1].motorSpeed = -1
		elif self.mJoints[1].angle < angle2:
			self.mJoints[1].motorSpeed =1
		if( self.mJoints[2].angle > angle3 ):
			self.mJoints[2].motorSpeed = -1
		elif self.mJoints[2].angle < angle3:
			self.mJoints[2].motorSpeed =1

		if self.mJoints[0].angle==angle1 and self.mJoints[1].angle==angle2 and self.mJoints[2].angle==angle3:
			return True;
		else:
			return False;

	def render(self, screen, ppm):
		PPM = ppm
		SCREEN_HEIGHT = 600

		# Render basement
		baseFixtures = self.mBase.fixtures;
		for fixture in baseFixtures:
			baseShape   = fixture.shape;
			baseVertices=[(self.mBase.transform*v)*PPM for v in baseShape.vertices]
			baseVertices=[(v[0], SCREEN_HEIGHT-v[1]) for v in baseVertices]
			pygame.draw.polygon(screen, (230,230,230,200), baseVertices);
		
		idx = 0

		# Draw the world
		for body in self.mSkelentons: # or: world.bodies
			# The body gives us the position and angle of its shapes
			for fixture in body.fixtures:
				shape = fixture.shape
				vertices=[(body.transform*v)*PPM for v in shape.vertices]
				vertices=[(v[0], SCREEN_HEIGHT-v[1]) for v in vertices]
				pygame.draw.polygon(screen, self.mColors[idx], vertices)
			idx = idx+1
