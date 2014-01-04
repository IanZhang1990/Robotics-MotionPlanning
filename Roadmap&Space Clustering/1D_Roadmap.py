import pygame

import pygame, sys, os
from pygame.locals import *
from random import randrange, uniform


pygame.init()
WIDTH = 600
HEIGHT = 400
#DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))

# One dimension range
WIDTH_RANGE = [0, 3]

# segment obstacles
obstacles = [ (1,1.2), (2,2.2) ]

def mapToImgCoord( x, imgmin, imgmax ):
        ratio = int( float(imgmax-imgmin) / float( WIDTH_RANGE[1] - WIDTH_RANGE[0] ) );
        return ( x * ratio )

def drawObstaclesToPic(ImgSurface):
        ImgSurface.fill( (255,255,255) )
        pygame.draw.line( ImgSurface, ( 0, 0, 0 ), ( 0, HEIGHT/2 ), (WIDTH, HEIGHT/2) );
        for obc in obstacles:
                minX = mapToImgCoord( obc[0], 0, WIDTH )
                maxX = mapToImgCoord( obc[1], 0, WIDTH )
                pygame.draw.rect( ImgSurface, ( 255, 0, 0 ), (minX, HEIGHT/2-10, (maxX-minX), 10), 4 );

def sample( num ):
        i = 0;
        imgW = 600;
        imageSurface = pygame.display.set_mode( (imgW, imgW) )
        imageSurface.fill( (255,255,255) )

        feasablePath = []

        print "Begin to sample...."

        while( i < num ):
                irand_1 = uniform( WIDTH_RANGE[0], WIDTH_RANGE[1] );
                irand_2 = uniform( WIDTH_RANGE[0], WIDTH_RANGE[1] );


                if (irand_1 < obstacles[0][0] and irand_2 < obstacles[0][0]):
                        feasablePath = feasablePath + [(irand_1, irand_2)];
                        pass
                elif irand_1 > obstacles[0][1] and irand_2 > obstacles[0][1] and irand_1 < obstacles[1][0] and irand_2 < obstacles[1][0]:
                        feasablePath = feasablePath + [(irand_1, irand_2)];
                        pass
                elif irand_1 > obstacles[1][1] and irand_2 > obstacles[1][1]:
                        feasablePath = feasablePath + [(irand_1, irand_2)];
                i = i + 1;
        print "Sampling Finished!"
        print "Got " + str( len(feasablePath) ) + " samples";

        print "Write to image"
        for point in feasablePath:        
                x_val = mapToImgCoord( point[0], 0, imgW )
                y_val = mapToImgCoord( point[1], 0, imgW )
                #print str(x_val) + "\t" + str(y_val)
                pygame.draw.rect( imageSurface, ( 100, 100, 100 ), (x_val, y_val,2,2), 1 )

        pygame.display.update()

        pygame.image.save( imageSurface, "1DSampling.PNG" );

        print "DONE!!!"
        pass


if __name__ == "__main__":

        myImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
        #myImage.convert();

        drawObstaclesToPic( myImage );

        pygame.image.save( myImage, "1D.PNG" );

        sample( 3000 );
