import pygame, sys, os
from pygame.locals import *
from random import randrange, uniform
import numpy
from Triangulation import *
from SVMClassification import *

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
g_obstacles = []#[Rect( 40,40, 100, 150 ), Circle( 300, 200, 50 ), Circle( 520, 200, 50 )]

# The space is partitioned into several
# Each part is not connected with others
# g_spaces = [ Rect( 0, 5, 300, 200 ), Rect( 320, 5, 200, 200 ), Circle( 100, 300, 90 ), Circle( 300, 300, 80 ), Circle( 500, 300, 80 ) ]
g_spaces = [ Rect( 10, 5, 270, 380 ), Rect( 360, 5, 230, 180 ),Rect( 360, 230, 230, 150 ) ]

g_obcColor = [ 240, 0, 0 ]
g_obcThickness = 2;
g_spaceColor = [ 0, 150, 0 ]
g_spaceThickness = 3;
g_recordFile = "2DSamples.txt"

def generateObstacles( rectNum, cirNum ):
	obs = []
	for i in range( 0, rectNum ):
		w = randrange( 50, 100 );
		h = randrange( 50, 100 );
		x = randrange( 0, WIDTH-w );
		y = randrange( 0, HEIGHT-h );
		obs = obs + [Rect(x,y,w,h)];
		pass;

	for i in range( 0, cirNum ):
		r = randrange( 30, 60 );
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

def writeVectorsToFile( vectors1, vectors2, filename ):
	file2write = open( filename, 'w' );
	#plotFile = open( "Plot"+filename, 'w' )
	formattedData = ""
	#plotData = ""
	for vector in vectors1:
		formattedData = formattedData + "1 1:{0} 2:{1}\n".format(str(vector[0]),str(vector[1]))
		#plotData = plotData + "{0}\t{1}\t{2}\t{3}\n".format(str(vector[0]),str(vector[1]),str(vector[2]),str(vector[3]))
		pass

	for vector in vectors2:
		formattedData = formattedData + "2 1:{0} 2:{1}\n".format(str(vector[0]),str(vector[1]))
		#plotData = plotData + "{0}\t{1}\t{2}\t{3}\n".format(str(vector[0]),str(vector[1]),str(vector[2]),str(vector[3]))
		pass

	file2write.write( formattedData );
	file2write.close();

	#plotFile.write( plotData );
	#plotFile.close();

def isInFreeSpace( x1, y1 ):
	isInFreeSpace = False;
	for space in g_spaces:
		if space.isInside( x1, y1 ):
			isInFreeSpace = True;
			# Begin to test obstacles
			for obc in g_obstacles:
				if obc.isInside( x1, y1 ):
					isInFreeSpace = False
					break;
			# both (x1, y1) and (x2, y2) are not in any obstacles
			# This is a feasible path
			if isInFreeSpace:
				break;
			else:
				break;
			pass
		else:
			continue;
		pass
	return isInFreeSpace;

def sampleSpace(num):
	i = 0;

	freePoints = []
	obstPoints = []


	print "Begin to sample...."

	while( i < num ):
		irand_1 = randrange( 0, WIDTH );
		irand_2 = randrange( 0, HEIGHT );

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
		if isInFreeSpace( irand_1, irand_2 ):
			freePoints = freePoints + [[irand_1, irand_2]]
		else:
			obstPoints = obstPoints + [[irand_1, irand_2]];
		i = i + 1;

	print "Sampling Finished!"
	print "Got " + str( len(freePoints) ) + " samples in free spaces";
	print "and " + str(len(obstPoints)) + " samples in obstacles\n"

	print "Draw to image...."
	sampleImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
	sampleImage.fill( (255, 255, 255) );
	drawSpacePartitionToPic(sampleImage)
	drawObstaclesToPic(sampleImage)
	pygame.display.flip()
	for point in freePoints:
		pygame.draw.circle( sampleImage, (0, 255, 0), (point[0],point[1]), 1 );
	for point in obstPoints:
		pygame.draw.circle( sampleImage, (255, 0, 0), (point[0],point[1]), 1 );
	pygame.image.save( sampleImage, "sampleImage.png" );
	print "DONE!!!"

	print "Write to file..."
	writeVectorsToFile( freePoints, obstPoints,  g_recordFile )
	print "Done Writing"

	return freePoints, obstPoints

def main():
	global g_obstacles;
	g_obstacles = generateObstacles( 10, 5 );

	freePoints, obstPoints = sampleSpace( 2000 )	



	allPoints = np.array(freePoints + obstPoints);
	triangulator = Triangulator();
	triangulator.triangulate( allPoints );
	triangles = triangulator.triangles;

	triImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
	triImage.fill( (255, 255, 255) )
	drawSpacePartitionToPic(triImage)
	drawObstaclesToPic(triImage)

	for triangle in triangles:
		point1 = [int(triangle.points[0][0]), int(triangle.points[0][1])]
		point2 = [int(triangle.points[1][0]), int(triangle.points[1][1])]
		point3 = [int(triangle.points[2][0]), int(triangle.points[2][1])]
		
		inObsCount = 0;
		if point1 in obstPoints:
			inObsCount = inObsCount + 1;
		if point2 in obstPoints:
			inObsCount = inObsCount + 1;	
		if point3 in obstPoints:
			inObsCount = inObsCount + 1;

		if inObsCount == 3:
			triangle.render( triImage, (255, 0, 0) )
		else:
			triangle.render( triImage, (0, 255, 0) )

	pygame.image.save( triImage, "Triangulation.PNG" )


	freespaceTriImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
	freespaceTriImage.fill( (255, 255, 255) );

	for triangle in triangles:
		point1 = [int(triangle.points[0][0]), int(triangle.points[0][1])]
		point2 = [int(triangle.points[1][0]), int(triangle.points[1][1])]
		point3 = [int(triangle.points[2][0]), int(triangle.points[2][1])]

		inObsCount = 0;
		if point1 in obstPoints:
			inObsCount = inObsCount + 1;
		if point2 in obstPoints:
			inObsCount = inObsCount + 1;	
		if point3 in obstPoints:
			inObsCount = inObsCount + 1;

		if inObsCount == 3:
			pass
		else:
			triangle.render( freespaceTriImage, (0, 255, 0) )

	pygame.image.save( freespaceTriImage, "FreespaceTriangulation.PNG" )
	return

	print "Start training data...."
	classifier = SVMClassifier()
	classifier.train( g_recordFile )
	print "Training Finished!\n"


if __name__ == "__main__":

	main()