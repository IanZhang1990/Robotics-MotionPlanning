from RobotArm import *
import math


class CollisionManager(object):
    """Collision Detector in C-Space"""

    def __init__(self, robot):
        self.mRobot = robot;
    
    def ifCollide( self, config ):
        return self.mRobot.setParams( config[0], config[1] );

    def isOutOfBound(self, config):
        """Check if the configuration is out of bound of configuration space"""
        if len(config)>2:
            raise Exception( "This method is for 2D only now." );

        if config[0] > 3 * math.pi or config[1] > 3*math.pi:
            return True;

    def isPathFree(self, start, end):
        """Check if the path between start --> end is free.
		Note: This is for 2D only!
		@param start:	start position of the path
		@param end:		end position of the path
         """
        if len(start)>2 or len(end) > 2:
            raise Exception( "This method is for 2D only now." );

        dx = end[0] - start[0];
        dy = end[1] - start[1];
        length = math.sqrt( dx**2, dy**2 );
        if length < 0.0001:
            return True;
        cosTheta = dx / length;
        sinTheta = dy / length;
        stepLen = math.pi / 100.0;

        nextCheckPoint = ( start[0]+stepLen*cosTheta, start[1]+stepLen*sinTheta );
        dist2End = length - stepLen;
        i = 0;
        while(dist2End >= stepLen):
            if self.ifCollide( nextCheckPoint ):
                return False;
            nextCheckPoint = ( start[0]+stepLen*i*cosTheta, start[1]+stepLen*i*sinTheta );
            dist2End = math.sqrt( (nextCheckPoint[0]-end[0])**2 + (nextCheckPoint[1]-end[1])**2 );
            i += 1;
        return True;