import pygame

import pygame, sys, os
from pygame.locals import *
from random import randrange, uniform

from SVMClassification_1D import *


pygame.init()
WIDTH = 600
HEIGHT = 400
#DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))

# One dimension range
WIDTH_RANGE = [0, WIDTH]

# segment obstacles
obstacles = [ (100,120), (350,370), (450, 470) ]

g_ImageSurface = None

def writeVectorsToFile( vectors1, vectors2, filename ):
        file2write = open( filename, 'w' );
        formattedData = ""
        for vector in vectors1:
                formattedData = formattedData + "1 1:{0} 2:{1}\n".format(str(vector[0]),str(vector[1]))
                pass

        for vector in vectors2:
                formattedData = formattedData + "2 1:{0} 2:{1}\n".format(str(vector[0]),str(vector[1]))
                pass

        file2write.write( formattedData );
        file2write.close();

def drawObstaclesToPic(ImgSurface):
        ImgSurface.fill( (255,255,255) )
        pygame.draw.line( ImgSurface, ( 0, 0, 0 ), ( 0, HEIGHT/2 ), (WIDTH, HEIGHT/2) );
        for obc in obstacles:
                minX = obc[0]
                maxX = obc[1]
                pygame.draw.rect( ImgSurface, ( 255, 0, 0 ), (minX, HEIGHT/2-10, (maxX-minX), 10), 4 );

def sample( num ):
        i = 0;
        imgW = 600;
        imageSurface = pygame.display.set_mode( (imgW, imgW) )
        g_ImageSurface = imageSurface;
        imageSurface.fill( (255,255,255) )

        feasiblePath = []
        infeasiblePath = []

        print "Begin to sample...."

        while( i < num ):
                irand_1 = randrange( WIDTH_RANGE[0], WIDTH_RANGE[1] );
                irand_2 = randrange( WIDTH_RANGE[0], WIDTH_RANGE[1] );


                if (irand_1 < obstacles[0][0] and irand_2 < obstacles[0][0]):
                        feasiblePath = feasiblePath + [(irand_1, irand_2)];
                        pass
                elif irand_1 > obstacles[0][1] and irand_2 > obstacles[0][1] and irand_1 < obstacles[1][0] and irand_2 < obstacles[1][0]:
                        feasiblePath = feasiblePath + [(irand_1, irand_2)];
                        pass
                elif irand_1 > obstacles[1][1] and irand_2 > obstacles[1][1] and irand_1 < obstacles[2][0] and irand_2 < obstacles[2][0]:
                        feasiblePath = feasiblePath + [(irand_1, irand_2)];
                elif irand_1 > obstacles[2][1] and irand_2 > obstacles[2][1]:
                        feasiblePath = feasiblePath + [(irand_1, irand_2)];
                else:
                        infeasiblePath = infeasiblePath + [(irand_1, irand_2)];
                i = i + 1;

        print "Sampling Finished!"
        print "Got " + str( len(feasiblePath) ) + " feasible samples\n And" + str(len(infeasiblePath)) + "infeasible pathes.";

        
        print "Write to image"
        for point in feasiblePath:        
                x_val = point[0]
                y_val = point[1]
                #print str(x_val) + "\t" + str(y_val)
                pygame.draw.rect( imageSurface, ( 100, 100, 100 ), (x_val, y_val,2,2), 1 )
        for point in infeasiblePath:        
                x_val = point[0]
                y_val = point[1]
                #print str(x_val) + "\t" + str(y_val)
                pygame.draw.rect( imageSurface, ( 255, 0, 0 ), (x_val, y_val,2,2), 1 )
                        
        pygame.display.update()

        print "Write to file"
        writeVectorsToFile( feasiblePath, infeasiblePath, "1DSampling.txt" )
        print "DONE!!!"


        # SVM Begins to work 
        classifier = SVMClassifier();
        classifier.train( "1DSampling.txt" );

        for x in range( 0, WIDTH ):
                for y in range( 0, WIDTH ):
                        #labels[x][y] = classifier.predict( (x/WIDTH, y/HEIGHT) );
                        label = classifier.predict( (x, y) );
                        print label
                        #print 'x: ' + str(x) + '\ty: ' + str(y) + '\t' + str(label)
                        if label == 1 and imageSurface.get_at((x, y)) == (255,255,255):
                                pygame.draw.line( imageSurface, ( 200, 200, 200), (x, y), (x, y) );
                pygame.display.update();
        print 'Finished!'

        pygame.image.save( imageSurface, "1DSampling.PNG" );
        
        

        return feasiblePath, infeasiblePath


def classify( vectors1, vectors2, trainFilepath ):
        g_ImageSurface = pygame.display.set_mode( (WIDTH, WIDTH) )
        g_ImageSurface.fill( (255,255,255) )

        classifier = SVMClassifier();
        classifier.train( trainFilepath );

        for x in range( 0, WIDTH ):
                for y in range( 0, HEIGHT ):
                        #labels[x][y] = classifier.predict( (x/WIDTH, y/HEIGHT) );
                        label = classifier.predict( (x, y) );
                        #print 'x: ' + str(x) + '\ty: ' + str(y) + '\t' + str(label)
                        if label == 0 and g_ImageSurface.get_at((x, y)) == Colors.WHITE:
                                pygame.draw.line( g_ImageSurface, Colors.GRAY_TRANS, (x, y), (x, y) );
                #pygame.display.update();
        print 'Finished!'
        pygame.image.save( g_ImageSurface, "1DSampling_SVM.PNG" )


if __name__ == "__main__":

        myImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
        #myImage.convert();

        drawObstaclesToPic( myImage );

        pygame.image.save( myImage, "1D.PNG" );

        feasible, infeasible = sample( 3000 );

        #classify( feasible, infeasible, "1DSampling.txt" )
