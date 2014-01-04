import pygame

import pygame, sys, os
from pygame.locals import *
from random import randrange, uniform


pygame.init()
WIDTH = 600
HEIGHT = 400
#DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))

class Obstacle:
	def __init__(self):
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


# segment obstacles
g_obstacles = []

# The space is partitioned into several
# Each part is not connected with others
g_spaces = [ Rect( 0, 5, 300, 200 ), Rect( 320, 5, 200, 200 ), Circle( 100, 300, 90 ), Circle( 300, 300, 80 ), Circle( 500, 300, 80 ) ]

g_obcColor = [ 240, 0, 0 ]
g_obcThickness = 1;
g_spaceColor = [ 0, 150, 0 ]
g_spaceThickness = 2;

def generateObstacles( rectNum, cirNum ):
	obs = []
	for i in range( 0, rectNum ):
		w = randrange( 10, 70 );
		h = randrange( 10, 60 );
		x = randrange( 0, WIDTH-w );
		y = randrange( 0, HEIGHT-h );
		obs = obs + [Rect(x,y,w,h)];
		pass;

	for i in range( 0, cirNum ):
		r = randrange( 10, 50 );
		x = randrange( r, WIDTH-r );
		y = randrange( r, HEIGHT-r );
		obs = obs + [Circle(x, y, r)];
		pass;
	return obs;



def drawSpacePartitionToPic( ImgSurface ):
	for space in g_spaces:
		space.render( ImgSurface, g_spaceColor, g_spaceThickness );

def drawObstaclesToPic(ImgSurface):
	for obc in g_obstacles:
		obc.render( ImgSurface, g_obcColor, g_obcThickness );

def writeVectorsToFile( vectors, filename ):
	file2write = open( filename, 'w' );
	formattedData = ""
	for vector in vectors:
		formattedData = formattedData + "{0}\t{1}\t{2}\t{3}\n".format(str(vector[0]),str(vector[1]),str(vector[2]),str(vector[3]))
		pass
	file2write.write( formattedData );
	file2write.close();

def samplePath( num ):
	i = 0;

	feasiblePath = []

	print "Begin to sample...."

	while( i < num ):
		irand_1 = randrange( 0, WIDTH );
		irand_2 = randrange( 0, HEIGHT );
		irand_3 = randrange( 0, WIDTH );
		irand_4 = randrange( 0, HEIGHT );

		## Assuming the 2D pace is partitioned into several parts
		#   ---------------------
		#   |		  |			|
		#   |		  |			|
		#   |		  |			|
		#   |--------------------
		#   |		 			|
		#   |					|
		#   ---------------------
		# Each part is not connected with others.
		# These parts are stored in list spaces[] 
		for space in g_spaces:
			if space.isInside( irand_1, irand_2 ) and space.isInside( irand_3, irand_4 ):
				# Begin to test obstacles
				for obc in g_obstacles:
					if obc.isInside( irand_1, irand_2 ) or obc.isInside( irand_3, irand_4 ):
						break;
				# both (irand_1, irand_2) and (irand_3, irand_4) are not in any obstacles
				# This is a feasible path
				feasiblePath = feasiblePath + [ ( irand_1, irand_2, irand_3, irand_4 ) ];
				break;
				pass
			pass

		i = i + 1;


	print "Sampling Finished!"
	print "Got " + str( len(feasiblePath) ) + " samples";

	print "Write to file"
	writeVectorsToFile( feasiblePath, "feasiblePath.txt" )
	print "DONE!!!"
	pass


if __name__ == "__main__":

	myImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
	myImage.fill( (255, 255, 255) );

	g_obstacles = generateObstacles( 20, 10 );

	drawObstaclesToPic( myImage );
	drawSpacePartitionToPic( myImage );

	pygame.image.save( myImage, "2D.PNG" );

	samplePath( 4000 );
