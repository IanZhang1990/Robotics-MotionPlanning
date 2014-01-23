

import pygame, sys, os
import math
from Obstacle import *


clsss Ray:
	def __init__( self, x, y, theta ):
		"""
		@param x: 		ray origin x position
		@param y: 		ray origin y position
		@param theta: 	ray direction angle ( compare to level )
		"""
		self.mOrigin = [x, y];
		self.mTheta = theta;

	def getOrigin(self):
		return (self.mOrigin[0], self.mOrigin[1])

	def getTheta(self):
		return self.mTheta;

	def shoot(self, obstMgr):
		stepLength = 1.0

		isInitiallyInside = obstMgr.isConfigInObstacle( self.mOrigin );

		nextCheckPoint = [ sample[0] + stepLength*math.cos( self.mTheta ), sample[1]+stepLength*math.sin( self.mTheta ) ]
		
		tries = 1;
		while( isInitiallyInside != obstMgr.isConfigInObstacle( nextCheckPoint ) ):
			i+=1;
			nextCheckPoint = [ sample[0] + stepLength*i*math.cos( self.mTheta ), sample[1]+stepLength*i*math.sin( self.mTheta ) ];
			pass;

		dx = nextCheckPoint[0] - self.mOrigin[0];
		dy = nextCheckPoint[1] - self.mOrigin[1];
		dist = math.sqrt( dx**2 + dy**2 );

		if isInitiallyInside:
			return dist;
		else:
			return dist*(-1);
		

class RayShooter:
	"""Class to manager ray operations"""
	def __init__( self, x, y, obstMgr ):
		self.mOrigin = [x,y];
		self.mObstMgr = obstMgr;
		self.mOriginInObst = obstMgr.isConfigInObstacle( self.mOrigin );

	def randShoot(self, num):
		"""Randomly shoot rays from one origin.
		@param num: number of rays you want to shoot from one point
		"""

		dlt_ang = math.pi / (float)num; # increment of angle;

		minDist = 1000000000000.0f;

		for i in range(1, num+1):
			theta = dlt_ang * i;
			ray = Ray( self.mOrigin[0],self.mOrigin[1], theta );
			dist = ray.shoot(self.mObstMgr);
			if math.fabs(dis) < math.fabs(minDis):
				minDist = dist;

		return minDist;


