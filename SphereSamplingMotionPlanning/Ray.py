

import pygame, sys, os
import math


class Ray:
	def __init__( self, x, y, theta ):
		"""
		@param x: 		ray origin x position
		@param y: 		ray origin y position
		@param theta: 	ray direction angle ( compare to level )
		"""
		self.mOrigin = (x, y);
		self.mTheta = theta;
		self.mEnd = (-1,-1)

	def getOrigin(self):
		return (self.mOrigin[0], self.mOrigin[1])

	def getTheta(self):
		return self.mTheta;

	def shoot(self, collisionMgr):

		stepLength = math.pi / 100.0;

		isInitiallyInside = collisionMgr.ifCollide( self.mOrigin );

		nextCheckPoint = [ self.mOrigin[0] + stepLength*math.cos( self.mTheta ), self.mOrigin[1]+stepLength*math.sin( self.mTheta ) ]
		
		i = 1;
		while( isInitiallyInside == collisionMgr.ifCollide( nextCheckPoint ) and not collisionMgr.isOutOfBound(nextCheckPoint) ):
			i+=1;
			nextCheckPoint = [ self.mOrigin[0] + stepLength*i*math.cos( self.mTheta ), self.mOrigin[1]+stepLength*i*math.sin( self.mTheta ) ];
			pass;

		self.mEnd = ( nextCheckPoint[0], nextCheckPoint[1] )
		dx = nextCheckPoint[0] - self.mOrigin[0];
		dy = nextCheckPoint[1] - self.mOrigin[1];
		dist = math.sqrt( dx**2 + dy**2 );

		if isInitiallyInside:
			return dist*(-1);
		else:
			return dist;

	def drawRay( self, imgSurf ):
		pygame.draw.line( imgSurf, (0,250,0), self.mOrigin, self.mEnd, 1 );
		

class RayShooter:
	"""Class to manager ray operations"""
	def __init__( self, x, y, collisionManager ):
		self.mOrigin = [x,y];
		self.mCollisionMgr = collisionManager;
		self.mOriginInObst = collisionManager.ifCollide( self.mOrigin );

	def randShoot(self, num):
		"""Randomly shoot rays from one origin.
		@param num: number of rays you want to shoot from one point
		"""
		dlt_ang = (2*math.pi) / float(num); # increment of angle;

		minDist = 1000000000000.0;
		chosenRay = None;

		for i in range(1, num+1):
			theta = dlt_ang * i;
			ray = Ray( self.mOrigin[0],self.mOrigin[1], theta );
			dist = ray.shoot(self.mCollisionMgr);
			if math.fabs(dist) < math.fabs(minDist):
				minDist = dist;

		return minDist;


