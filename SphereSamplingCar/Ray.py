

import sys, os
import math
from copy import copy;
from random import randint


class Ray:
    def __init__( self, pos, dir ):
        """
         @param pos: 		ray origin position.
         @param dir:     	ray direction.
         """
        self.mOrigin = pos;
        self.mDirect = self.__norm__(dir);
        self.mEnd = None;
    
    def __norm__(self, vector):
        """Normalize a vector"""
        length = 0;
        normVect = copy(vector);
        for i in range( 0, len(vector) ):
            length += vector[i]**2;
        length = math.sqrt( length );

        for i in range( 0, len(vector) ):
            normVect[i] = vector[i]/length;

        return normVect;

    def getOrigin(self):
        return self.mOrigin;
    
    def getDirection(self):
        return self.mDirect;
    
    def shoot(self, collisionMgr, cSpace):
        
        stepLength = 3;
        
        initAngle = cSpace.map2UnscaledSpace( self.mOrigin );
        isInitiallyInside = collisionMgr.ifCollide( initAngle );
        if( isInitiallyInside ):
            return None;
        
        nextCheckPoint = copy(self.mOrigin);
        for i in range( 0, len(nextCheckPoint) ):
            nextCheckPoint[i] = self.mOrigin[i] + self.mDirect[i]*stepLength;

        nextCheckPointInCSpace = cSpace.map2UnscaledSpace( nextCheckPoint );
        
        i = 1;
        while( isInitiallyInside == collisionMgr.ifCollide( nextCheckPointInCSpace )):
            for j in range(0, len(self.mOrigin)):
                if( math.fabs( nextCheckPoint[j]-self.mOrigin[j] ) > 1050 ):
                    return 10000000000000000000;
                pass;
            
            i+=1;
            for j in range( 0, len(nextCheckPoint) ):
                nextCheckPoint[j] = self.mOrigin[j] + self.mDirect[j]*stepLength*i;
            nextCheckPointInCSpace = cSpace.map2UnscaledSpace( nextCheckPoint );
            pass;
        
        self.mEnd = nextCheckPoint

        dist = 0;
        for j in range( 0, len(nextCheckPoint) ):
            dist += (nextCheckPoint[j]-self.mOrigin[j])**2;
        dist = math.sqrt( dist );
        
        if isInitiallyInside:
            return dist*(-1);
        else:
            return dist;


class RayShooter:
    """Class to manager ray operations"""
    def __init__( self, origin, collisionManager, cSpace ):
        """
         @param origin: origin position. We will shoot random rays from this position.
         """
        self.mOrigin = origin;
        self.mCollisionMgr = collisionManager;
        self.mCSpace = cSpace;
        self.mOriginInObst = collisionManager.ifCollide( self.mOrigin );

    def randShoot(self, num):
        """Randomly shoot rays from one origin.
         @param num: number of rays you want to shoot from one point
		"""
        minDist = 1000000000000.0;
        chosenRay = None;
        dim = len(self.mOrigin);

        for i in range(1, num+1):
            dir = [0] * dim;
            for j in range(0, dim ):
                dir[j] = randint( -500, 500 );
            ray = Ray( self.mOrigin, dir );
            dist = ray.shoot(self.mCollisionMgr, self.mCSpace);
            if dist is None:
                return -100000000000.0;
            if math.fabs(dist) < math.fabs(minDist):
                minDist = dist;

        return minDist;


