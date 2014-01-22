import pygame, sys, os
from pygame.locals import *
from random import randrange, uniform

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
g_spaces = [ Rect( 0, 0, WIDTH, HEIGHT ) ]

g_obcColor = [ 240, 0, 0 ]
g_obcThickness = 2;
g_spaceColor = [ 0, 150, 0 ]
g_spaceThickness = 3;
g_recordFile = "path.txt"

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
	plotFile = open( "Plot"+filename, 'w' )
	formattedData = ""
	plotData = ""
	for vector in vectors1:
		formattedData = formattedData + "1 1:{0} 2:{1} 3:{2} 4:{3}\n".format(str(vector[0]),str(vector[1]),str(vector[2]),str(vector[3]))
		plotData = plotData + "{0}\t{1}\t{2}\t{3}\n".format(str(vector[0]),str(vector[1]),str(vector[2]),str(vector[3]))
		pass

	for vector in vectors2:
		formattedData = formattedData + "2 1:{0} 2:{1} 3:{2} 4:{3}\n".format(str(vector[0]),str(vector[1]),str(vector[2]),str(vector[3]))
		#plotData = plotData + "{0}\t{1}\t{2}\t{3}\n".format(str(vector[0]),str(vector[1]),str(vector[2]),str(vector[3]))
		pass

	file2write.write( formattedData );
	file2write.close();

	plotFile.write( plotData );
	plotFile.close();

def isPathFeasible( x1, y1, x2,y2 ):
	isfeasible = False;
	for space in g_spaces:
		if space.isInside( x1, y1 ) and space.isInside( x2, y2 ):
			isfeasible = True;
			# Begin to test obstacles
			for obc in g_obstacles:
				if obc.isInside( x1, y1 ) or obc.isInside( x2, y2 ):
					isfeasible = False
					break;
			# both (x1, y1) and (x2, y2) are not in any obstacles
			# This is a feasible path
			if isfeasible:
				break;
			else:
				break;
			pass
		elif space.isInside( x1, y1 ) and not space.isInside( x2, y2 ):
			ifFeasible = False;
			break;
		else:
			continue;
		pass
	return isfeasible;

def samplePath(num):
	i = 0;

	feasiblePath = []
	infeasiblePath = []
	pathImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
	pathImage.fill( (255, 255, 255) );


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
		if isPathFeasible( irand_1, irand_2, irand_3,irand_4 ):
			feasiblePath = feasiblePath + [(irand_1, irand_2, irand_3, irand_4)]
		else:
			infeasiblePath = infeasiblePath + [ (irand_1, irand_2, irand_3, irand_4) ];
		i = i + 1;


	print "Sampling Finished!"
	print "Got " + str( len(feasiblePath) ) + " feasible samples";
	print "and " + str(len(infeasiblePath)) + " infeasible samples\n"

	print "Draw to image...."
	drawSpacePartitionToPic(pathImage)
	drawObstaclesToPic(pathImage)
	pygame.display.flip()
	#for path in feasiblePath:
	#	pygame.draw.line( pathImage, (0, 255, 0), (path[0],path[1]), (path[2],path[3]) );
	for path in infeasiblePath:
		pygame.draw.line( pathImage, (255, 0, 0), (path[0],path[1]), (path[2],path[3]) );
	pygame.image.save( pathImage, "pathImage.png" );
	print "DONE!!!"
	pass

def samplePathAndDoSVM( num ):
	i = 0;

	feasiblePath = []
	infeasiblePath = []

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
		if isPathFeasible( irand_1, irand_2, irand_3,irand_4 ):
			feasiblePath = feasiblePath + [(irand_1, irand_2, irand_3, irand_4)]
		else:
			infeasiblePath = infeasiblePath + [ (irand_1, irand_2, irand_3, irand_4) ];
		
		i = i + 1;
		"""
		isfeasible = False;
		for space in g_spaces:
			if space.isInside( irand_1, irand_2 ) and space.isInside( irand_3, irand_4 ):
				isfeasible = True;
				# Begin to test obstacles
				for obc in g_obstacles:
					if obc.isInside( irand_1, irand_2 ) or obc.isInside( irand_3, irand_4 ):
						isfeasible = False
						break;
				# both (irand_1, irand_2) and (irand_3, irand_4) are not in any obstacles
				# This is a feasible path
				if isfeasible:
					feasiblePath = feasiblePath + [(irand_1, irand_2, irand_3, irand_4)];
					break;
				else:
					break;
				pass
			elif space.isInside( irand_1, irand_2 ) and not space.isInside( irand_3, irand_4 ):
				ifFeasible = False;
				break; 
			else:
				continue;
			pass
		if not isfeasible:
			infeasiblePath = infeasiblePath + [ (irand_1, irand_2, irand_3, irand_4) ];
		"""

	print "Sampling Finished!"
	print "Got " + str( len(feasiblePath) ) + " feasible samples";
	print "and " + str(len(infeasiblePath)) + " infeasible samples\n"

	print "Writing to file...."
	writeVectorsToFile( feasiblePath, infeasiblePath,  g_recordFile )
	print "DONE!!!"
	pass

def main():
	myImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
	myImage.fill( (255, 255, 255) );

	global g_obstacles;
	g_obstacles = generateObstacles( 4, 5 );

	drawObstaclesToPic( myImage );
	drawSpacePartitionToPic( myImage );

	pygame.image.save( myImage, "2D.PNG" );

	samplePath( 400 )
	return;

	samplePathAndDoSVM( 3000 );

	print "Start training data...."
	classifier = SVMClassifier()
	classifier.train( g_recordFile )
	print "Training Finished!\n"


	pathImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
	pathImage.fill( (255, 255, 255) );
	drawSpacePartitionToPic(pathImage)
	drawObstaclesToPic(pathImage)

	for i in range( 0, 200 ):
		irand_1 = randrange( 0, WIDTH );
		irand_2 = randrange( 0, HEIGHT );
		irand_3 = randrange( 0, WIDTH );
		irand_4 = randrange( 0, HEIGHT );
		testData = ( irand_1, irand_2, irand_3, irand_4 )
		label, acc, val = classifier.predict( testData );
		ifFeasible = "";
		checkResult = isPathFeasible(irand_1, irand_2, irand_3, irand_4);
		if (label[0]==1.0 and checkResult==True):
			pygame.draw.line( pathImage, (0, 0, 255), (irand_1,irand_2), (irand_3,irand_4) );
		elif(label[0]==2.0 and checkResult==False):
			pygame.draw.line( pathImage, (0, 255, 0), (irand_1,irand_2), (irand_3,irand_4) );
		else:
			pygame.draw.line( pathImage, (255, 0, 0), (irand_1,irand_2), (irand_3,irand_4) );

		print( "Result: {0} path. \t{1} to {2}".format( label, (irand_1, irand_2), (irand_3, irand_4) ) );

	pygame.image.save( pathImage, "pathImage.png" )

	
"""
	testData = [[379,355,334,384],[17,6,155,279],[227,351,129,341]];
	for i in range(0,3):
		label, acc, val = classifier.predict( testData[i] );
		print( "Result: Label: {0}, accuracy:{1}, Val:{2}\t".format( label, acc,val ) );
"""

if __name__ == "__main__":

	main()