
import sys, os
import math
import random
from CollisionManager import *
import pygame;

class CSpaceWorld:
    g_obcColor = [ 150, 150, 150 ]
    g_obcThickness = 0;
    g_spaceColor = [ 0, 150, 0 ]
    g_spaceThickness = 3;

    def __init__( self, robot ):
        self.mRobot = robot;
        self.mRatio = 100;
        self.mScaledWidth = 900;
        self.mScaledHeight = 900;
        self.mCollisionMgr = CollisionManager( robot );

    def renderCSpace( self ):

        imgSurface = pygame.display.set_mode((self.mScaledHeight, self.mScaledWidth));
        imgSurface.fill((255,255,255));
        ObstacleColor = ( 50, 50, 50 );
        obstaclePoints = [];

        # Randomly sample and draw in the image
        for i in range( 0, 300000 ):
            scaledAlpha = random.randint( 0, self.mScaledWidth );
            scaledPhi = random.randint( 0, self.mScaledHeight );
            alpha, phi = self.map2UnscaledSpace( scaledAlpha, scaledPhi );
            collide = self.mCollisionMgr.ifCollide( (alpha, phi) );
            if collide:
                obstaclePoints.append( (scaledAlpha, scaledPhi) );
                pygame.draw.line( imgSurface, ObstacleColor, (scaledAlpha, scaledPhi), (scaledAlpha, scaledPhi));
                
                
        # Save Data
        worldFile = open( "CSpace.txt", 'w' );
        worldFile.write( "WIDTH\t{0}\nHEIGHT\t{1}\n".format( self.mScaledWidth, self.mScaledHeight ) );
        for pair in obstaclePoints:
            worldFile.write( "{0}\t{1}\n".format(pair[0], pair[1]) );

        return imgSurface;
            
    def map2UnscaledSpace( self, alpha, phi ):
        """The given parameters are scaled, we want to map them to -1.5~1.5PI"""
        retAlpha = ((alpha-self.mScaledWidth/2) / float(self.mScaledWidth))  * math.pi * 2;
        retPhi   = ((phi-self.mScaledHeight/2)  / float(self.mScaledHeight)) * math.pi * 2;
        return retAlpha, retPhi;

    def loadCSpace(self, filename):
        """Load C space info from file. Return rendered image"""

        imgSurface = None;
        ObstacleColor = ( 50, 50, 50 );
        obstaclePoints = [];

        CSpaceFile = open(filename, 'r');
        for line in CSpaceFile:
            info = line.split('\t');
            if(info[0]=="WIDTH"):
                self.mScaledWidth = int(info[1]);
            elif info[0] == "HEIGHT":
                self.mScaledHeight = int(info[1]);
            elif len(info)==2:
                if( imgSurface == None ):
                    imgSurface = pygame.display.set_mode((self.mScaledHeight, self.mScaledWidth));
                    imgSurface.fill((255,255,255));
                pygame.draw.line( imgSurface, ObstacleColor, (int(info[0]),int(info[1])), (int(info[0]),int(info[1])));
        
        return imgSurface;