from random import randrange, uniform

import sys, os, datetime
import math
from Ray import *
from CSpaceWorld import *
from SpacePartition import *
from ObstSurfSearcher import *
from RobotCar import *
#import pygame
from Queue import Queue
from collections import defaultdict


class ClearSample:
	"""Clearance sample class. A clearance sample contains: 
	1. A safe sphere centered at a point, where a car can travel from one point to another in the sphere with some constrains on orientation changes.
	2. Actually clearance at the point
	3. Required clearance for a car to travel in the safe sphere with any orientation change."""

	def __init__(self, point, innerR, outerR):
		"""@param point: the position of the point.
		@param innerR: radius of the safe sphere.
		@param outerR: actual clearance at the point"""
		self.mSafeSphere = Sphere( point[0], point[1], innerR );
		self.mActualClearance = Sphere(point[0], point[1], outerR);
		if( self.mActualClearance - self.mSafeSphere >= math.pi/2 ):
			requiredClearance = self.mActualClearance;
		else:
			requiredClearance = innerR + math.pi/2 * RobotCar.minRadius;
		self.mRequiredClearance = Sphere( point[0], point[1], requiredClearance );