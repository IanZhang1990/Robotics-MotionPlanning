import pygame, sys, os
from pygame.locals import *
from Obstacle import *

from SampleManager import *
from PRM import *


pygame.init()
WIDTH = 1366
HEIGHT = 768
#DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))

sampleWorld = World( WIDTH, HEIGHT );
sampleMgr = SampleManager( sampleWorld );

# segment obstacles
g_obstacles = []#[Rect( 40,40, 100, 150 ), Circle( 300, 200, 50 ), Circle( 520, 200, 50 )]

# The space is partitioned into several
# Each part is not connected with others
# g_spaces = [ Rect( 0, 5, 300, 200 ), Rect( 320, 5, 200, 200 ), Circle( 100, 300, 90 ), Circle( 300, 300, 80 ), Circle( 500, 300, 80 ) ]
g_spaces = [ Rect( 1, 1, WIDTH-1, HEIGHT-1 ) ]

g_recordFile = "path.txt"


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

def main():

	global sampleWorld, sampleMgr;

	myImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
	myImage.fill( (255, 255, 255) );

	#sampleWorld.buildWorld();
	#sampleWorld.saveWorld("world.txt");
	sampleWorld.loadWorld("world.txt");
	sampleWorld.drawSpacesToPic( myImage );
	sampleWorld.drawObstaclesToPic( myImage );

	#rayShooter = RayShooter( 247, 260, sampleWorld.mObstMgr );
	#dist, ray = rayShooter.randShoot(36);
	#print "Smallest {0}".format(dist);
	#ray.drawRay(myImage);
	#pygame.draw.circle( myImage, ( 0, 250, 0 ), (247, 260), int(dist), 1 );

	sampleMgr.sampleWithMoreInfo( 20 );
	sampleMgr.writeSamplesToFile( "distSample.txt" );
	sampleMgr.drawDistSampleToPic( myImage );

	pygame.image.save( myImage, "World.PNG" );

	return;

if __name__ == "__main__":

	main()