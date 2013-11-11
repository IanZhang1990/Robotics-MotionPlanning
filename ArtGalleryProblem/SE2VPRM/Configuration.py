import pygame
import math
from Arm import Arm

class Configuration(object):
    """description of class"""

    def __init__(self):
        self.mRobotArm = Arm();
        self.mObstacles = [ ( 600, 500, 10 ) ]; # ( x, y, radius )
        pass;

    def render(self, screen):
        self.mRobotArm.render( screen );
        
        for obs in self.mObstacles:
            pygame.draw.circle(screen, ( 255, 0, 0 ), ( obs[0], obs[1] ), obs[2], 3);

    def dist( point1, point2 ):
        return math.sqrt( (point1[0]-point2[0])*(point1[0]-point2[0])+(point1[1]-point2[1])*(point1[1]-point2[1]) );

    def ifCollide( self, theta, phi ):
        self.mRobotArm.move( theta, phi );
        ori = self.mRobotArm.mOrigin;
        mid = self.mRobotArm.midPoint();
        end = self.mRobotArm.endPoint();

        for obs in self.mObstacles:
            """A line can be written as: Ax + By + C = 0. 
            The distance from a point (xo, yo) to the line is:
            dis = |Axo+Byo+C|/sqrt(A^2+B^2)."""
            k1 = (mid[1]-ori[1])/(mid[0]-ori[0]);
            t1 = mid[1] - k1*mid[0];
            Line1 = ( k1, -1, t1 );
            k2 = (end[1]-mid[1])/(end[0]-mid[0]);
            t2 = end[1] - k2*end[0];
            Line2 = ( k2, -1, t2 );
            
            for obs in self.mObstacles:
                dist1 = math.fabs( Line1[0]*obs[0] + Line1[1]*obs[1] + Line1[2] ) / math.sqrt( Line1[0]*Line1[0] + Line1[1]*Line1[1] );
                dist2 = math.fabs( Line2[0]*obs[0] + Line2[1]*obs[1] + Line2[2] ) / math.sqrt( Line2[0]*Line2[0] + Line2[1]*Line2[1] );
                if dist1 <= obs[3] or dist2 <= obs[3]:
                    return True;
                else:
                    return False;
