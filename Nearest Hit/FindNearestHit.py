import pygame, sys, os, datetime
from pygame.locals import *
from Obstacle import *
from World import *


pygame.init()
WIDTH = 1366
HEIGHT = 768

sampleWorld = World( WIDTH, HEIGHT );

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
	global sampleWorld;

	initSampleImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
	initSampleImage.fill( (255, 255, 255) );

	sampleWorld.loadWorld("world.txt");
	sampleWorld.renderCSpace( initSampleImage );
	sampleWorld.renderObstacles( initSampleImage );

	pygame.image.save( initSampleImage, "SamplingImage.PNG" );

	return;

if __name__ == "__main__":
	main();
	pygame.quit();
