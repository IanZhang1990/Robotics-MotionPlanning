import pygame

import pygame, sys, os
from pygame.locals import *


pygame.init()
WIDTH = 600
HEIGHT = 400
DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))

# One dimension range
WIDTH_RANGE = [0, 3]

# segment obstacles
obstacles = [ (1,1.2), (2,2.2) ]

def mapToImgCoord( x ):
	ratio = int( float(WIDTH) / float( WIDTH_RANGE[1] - WIDTH_RANGE[0] ) );
	return ( x * ratio )

def drawPic(ImgSurface):
	ImgSurface.fill( (255,255,255) )
	pygame.draw.line( ImgSurface, ( 0, 0, 0 ), ( 0, HEIGHT/2 ), (WIDTH, HEIGHT/2) );
	for obc in obstacles:
		minX = mapToImgCoord(obc[0])
		maxX = mapToImgCoord( obc[1] )
		pygame.draw.rect( ImgSurface, ( 255, 0, 0 ), (minX, HEIGHT/2-10, (maxX-minX), 10), 4 );




if __name__ == "__main__":

	myImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
	myImage.convert();

	drawPic( myImage );

	pygame.image.save( myImage, "1D.PNG" );