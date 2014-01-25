
from random import randrange, uniform
import pygame


class Obstacle:
	def __init__(self):
		self.Name = "obstacle"
		pass

	def render(self, surface, color, thickness):
		pass;

	def isInside(self, x, y):
		""" Virtual super class of obstacles """
		return False;

class Rect(Obstacle):
	def __init__(self, x, y, width, height):
		self.X = x
		self.Y = y
		self.Width = width
		self.Height = height
		self.Name = "Rectangle"
		pass;

	def render( self, surface, color, thickness ):
		pygame.draw.rect( surface, color, (self.X, self.Y, self.Width, self.Height), thickness );
		pass

	def isInside(self, x, y):
		"""Determine if 2D point (x, y) is in the rectangle"""
		if x > self.X and x < (self.X+self.Width) and y > self.Y and y < (self.Y+self.Height):
			return True;
		else:
			return False;

class Circle(Obstacle):
	def __init__( self, x, y, radius ):
		self.X = x
		self.Y = y
		self.Radius = radius
		self.Name = "Circle"
		pass

	def render( self, surface, color, thickness ):
		pygame.draw.circle( surface, color, (self.X, self.Y), self.Radius, thickness );
		pass

	def isInside( self, x, y ):
		dist2 = (self.X-x)*(self.X-x) + (self.Y-y)*(self.Y-y);
		if dist2<= self.Radius*self.Radius:
			return True;
		else:
			return False;

class ObstaclesManager:
	def __init__(self, scrWidth, scrHeight):
		self.mObstacles = []
		self.mScreenWidth = scrWidth;
		self.mScreenHeight = scrHeight;

	def generateObstacles( self, rectNum, cirNum, minWidth, maxWidth, minHeight, maxHeight ):
		obs = []
		for i in range( 0, rectNum ):
			w = randrange( 50, 150 );
			h = randrange( 50, 150 );
			x = randrange( minWidth, maxWidth-w );
			y = randrange( minHeight, maxHeight-h );
			obs = obs + [Rect(x,y,w,h)];
			pass;

		for i in range( 0, cirNum ):
			r = randrange( 30, 100 );
			x = randrange( r, maxWidth-r );
			y = randrange( r, maxHeight-r );
			obs = obs + [Circle(x, y, r)];
			pass;

		self.mObstacles = obs;

		return obs; 

	def getObstacles(self):
		return self.mObstacles;

	def addObstacle(self, obst):
		self.mObstacles += [obst];

	def isConfigInObstacle(self, sample):
		space = Rect( 0,0, self.mScreenWidth, self.mScreenHeight );

		if not space.isInside( sample[0], sample[1] ):
			return True;

		for obst in self.mObstacles:
			if( obst.isInside(sample[0], sample[1]) ):
				return True;
		return False;

	def isOutOfWorld(self, sample):
		space = Rect( 0,0, self.mScreenWidth, self.mScreenHeight );

		if not space.isInside( sample[0], sample[1] ):
			return True;