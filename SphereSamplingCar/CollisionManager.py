from RobotCar import *
import math


class CollisionManager(object):
    """Collision Detector in C-Space"""

    def __init__(self, robot):
        self.mRobot = robot;
    
    def ifCollide( self, config ):
        return self.mRobot.setParams( config );

    def isOutOfBound(self, config, maxDimLens):
        """Check if the configuration is out of bound of configuration space"""
        for i in range(0, len(config)-1):
            if( config[i] < 0 or config[i] > maxDimLens[i] ):
                return True;
        return False;

    def isPathFree(self, start, end):
        """Check if the path between start --> end is free.
		@param start:	start position of the path
		@param end:		end position of the path
         """
        if len(start) != len(end):
            raise Exception( "Wrong parameters!! Dimensions should be the same." );

        deltas = [0] * len(start);
        length = 0;
        for i in range( 0, len(start) ):
            deltas[i] = start[i] - end[i];
            length += deltas[i]**2;

        length = math.sqrt( length );
        if length < 1:
            return True;

        stepNum = int(length / 4.0);
        stepLen = [0] * len( start );

        for i in range(0, len(start)):
            stepLen[i] = deltas[i] / stepNum;

        nextCheckPoint = [0] * len( start );
        for i in range(0, len(start)):
            nextCheckPoint[i] = start[i]+ 1*stepLen[i];

        for i in range(2, stepNum):
            if self.ifCollide( nextCheckPoint ):
                return False;
            for i in range(0, len(start)):
                nextCheckPoint[i] = start[i]+ i*stepLen[i];
        return True;