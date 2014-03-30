

import pygame, sys, os
import math


class Ray:
    def __init__( self, x, y, theta ):
        """@param x: 		ray origin x position
         @param y: 		ray origin y position
         @param theta: 	ray direction angle ( compare to level )
         """
        self.mOrigin = (x, y);
        self.mTheta = theta;
        self.mEnd = (-1,-1)
        
    def getOrigin(self):
        return (self.mOrigin[0], self.mOrigin[1])
    
    def getTheta(self):
        return self.mTheta;
    
    def shoot(self, collisionMgr, cSpace):
        
        stepLength = 1;
        
        init_alpha, init_phi = cSpace.map2UnscaledSpace( self.mOrigin[0], self.mOrigin[1] );
        isInitiallyInside = collisionMgr.ifCollide( (init_alpha, init_phi) );
        
        nextCheckPoint = ( (self.mOrigin[0] + stepLength*math.cos( self.mTheta )), self.mOrigin[1]+stepLength*math.sin( self.mTheta ))
        alpha, phi = cSpace.map2UnscaledSpace( nextCheckPoint[0], nextCheckPoint[1] );
        nextCheckPointInCSpace = (alpha, phi);
        
        i = 1;
        while( isInitiallyInside == collisionMgr.ifCollide( nextCheckPointInCSpace )):
            if( math.fabs(nextCheckPoint[0]-self.mOrigin[0]) >= 900 or math.fabs(nextCheckPoint[1]-self.mOrigin[1]) >= 900 ):
                self.mEnd = nextCheckPoint;
                return 1000000000000000000000;
            i+=1;
            nextCheckPoint = [ self.mOrigin[0] + stepLength*i*math.cos( self.mTheta ), self.mOrigin[1]+stepLength*i*math.sin( self.mTheta ) ];
            alpha, phi = cSpace.map2UnscaledSpace( nextCheckPoint[0], nextCheckPoint[1] );
            nextCheckPointInCSpace = (alpha, phi);
            pass;
        
        self.mEnd = ( nextCheckPoint[0], nextCheckPoint[1] )
        dx = nextCheckPoint[0] - self.mOrigin[0];
        dy = nextCheckPoint[1] - self.mOrigin[1];
        dist = math.sqrt( dx**2 + dy**2 );
        
        if isInitiallyInside:
            return dist*(-1);
        else:
            return dist;

    def drawRay( self, imgSurf ):
        pygame.draw.line( imgSurf, (0,250,0), self.mOrigin, self.mEnd, 1 );


class RayShooter:
    """Class to manager ray operations"""
    def __init__( self, x, y, collisionManager, cSpace ):
        self.mOrigin = [x,y];
        self.mCollisionMgr = collisionManager;
        self.mCSpace = cSpace;
        self.mOriginInObst = collisionManager.ifCollide( self.mOrigin );

    def randShoot(self, num):
        """Randomly shoot rays from one origin.
        @param num: number of rays you want to shoot from one point
		"""
        dlt_ang = (2*math.pi) / float(num); # increment of angle;
        
        minDist = 1000000000000.0;
        chosenRay = None;

        for i in range(1, num+1):
            theta = dlt_ang * i;
            ray = Ray( self.mOrigin[0],self.mOrigin[1], theta );
            dist = ray.shoot(self.mCollisionMgr, self.mCSpace);
            if math.fabs(dist) < math.fabs(minDist):
                minDist = dist;

        return minDist;


