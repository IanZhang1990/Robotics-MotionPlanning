import pygame, sys, os
from pygame.locals import *
from Obstacle import *
from random import randrange, uniform

pygame.init()
WIDTH = 1366
HEIGHT = 768
#DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))


# segment obstacles
g_obstacles = []#[Rect( 40,40, 100, 150 ), Circle( 300, 200, 50 ), Circle( 520, 200, 50 )]

# The space is partitioned into several
# Each part is not connected with others
# g_spaces = [ Rect( 0, 5, 300, 200 ), Rect( 320, 5, 200, 200 ), Circle( 100, 300, 90 ), Circle( 300, 300, 80 ), Circle( 500, 300, 80 ) ]
g_spaces = [ Rect( 1, 1, WIDTH-1, HEIGHT-1 ) ]

g_obcColor = [ 240, 0, 0 ]
g_obcThickness = 2;
g_spaceColor = [ 0, 150, 0 ]
g_spaceThickness = 3;
g_recordFile = "path.txt"



def drawSpacePartitionToPic( ImgSurface ):
	for space in g_spaces:
		space.render( ImgSurface, g_spaceColor, g_spaceThickness );

def drawObstaclesToPic(ImgSurface):
	for obc in g_obstacles:
		obc.render( ImgSurface, g_obcColor, g_obcThickness );

def writeVectorsToFile( vectors, filename ):
	file2write = open( filename, 'w' );
	plotFile = open( "Plot"+filename, 'w' )
	formattedData = ""
	plotData = ""
	for vector in vectors:
		currentData = ""
		for feature in vector:
			currentData += "{0}\t".format( str(feature) );
		formattedData += currentData + "\n";
		pass

	file2write.write( formattedData );
	file2write.close();


def sample(num):
	"""Randomly sample configurations in the c-space
	@param num: termination conditon. num times failed to find a new point, then terminate.
	"""
	
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