import pygame;
import math;

from GameWorld import Sphere;

class RobotArm(object):
    """description of class"""
    def __init__( self, position, obstacles ):
        """Create a 1-joint robot arm
         @parm position: the base position.
         @parm obstacles: a list of spheres as obstacles.
         """
        self.mPos = position;
        self.mLen1  = 100;               # Length of the first arm
        self.mLen2  = 100;               # Length of the secondary arm
        self.mAlpha = 0;                # angle of the base
        self.mPhi   = 0;                # angle of the joint
        self.mObsts = obstacles;

    def setParams( self, alpha, phi ):
        """Set angles of the robot arm, return if collide with obstacles."""
        self.mAlpha = alpha;
        self.mPhi = phi;

        base = self.mPos;
        end1 = (base[0]+self.mLen1*math.cos(alpha),    base[1]+self.mLen1*math.sin(alpha));
        end2 = (end1[0]+self.mLen2*math.cos(phi+alpha), end1[1]+self.mLen2*math.sin(phi+alpha));

        for obstacle in self.mObsts:
            dist1 = self.dist( obstacle.mPos, base, end1 );
            dist2 = self.dist( obstacle.mPos, end1, end2 );
            if dist1 < obstacle.mRadius or dist2 < obstacle.mRadius:
                return True;

        return False;

    def dist(self, point, end1, end2):
        """Distance from one point to a line ( end1 --> end2 )"""
        x0 = point[0]; y0 = point[1];
        x1 = end1[0]; y1 = end1[1];
        x2 = end2[0]; y2 = end2[1];

        # line aX + bY + c = 0;
        a = y2 - y1; b = x1 - x2; c = x2*y1-x1*y2;
        distance = (math.fabs(a*x0+b*y0+c)) / math.sqrt(math.pow(a, 2)+math.pow(b,2));
        
        if b == 0:
            b = 0.000000001;
        direction = -a/b;
        intersect = ( point[0] + distance * a/b, point[1] + distance * a/b );
        if( end1[0]<intersect[0] and intersect[0]<end2[0] and end1[1]<intersect[1] and intersect[1]<end2[1] ):
            return distance;
        else:
            distance1 = math.sqrt(math.pow(y0-y1,2) + math.pow(x0-x1,2));
            distance2 = math.sqrt(math.pow(y0-y2,2) + math.pow(x0-x2,2));
            if distance1 < distance2:
                return distance1;
            else:
                return distance2;

    def render(self, imgSurface, ifcollide):
        """Render the robot to the image"""
        alpha = self.mAlpha;
        phi = self.mPhi;

        base = self.mPos;
        end1 = (base[0]+self.mLen1*math.cos(alpha),    base[1]+self.mLen1*math.sin(alpha));
        end2 = (end1[0]+self.mLen2*math.cos(phi+alpha), end1[1]+self.mLen2*math.sin(phi+alpha));

        color = ( 0,0,180 );
        if( ifcollide ):
            color = (180, 0, 0)

        pygame.draw.line( imgSurface, color, base, end1, 3 ); 
        pygame.draw.line( imgSurface, color, end1, end2, 3 );
        return;

    def move(self, start, goal, imgsurf=None):
        """Given two configurations, we want to move from start --> goal"""
        d_alpha = goal[0] - start[0];
        d_phi = goal[1] - start[1];
        dist = math.sqrt( d_alpha**2, d_phi**2 );
        num = int( dist/0.02); 
        for i in range(0,num):
            ifcollide = self.setParams( start[0]+i*(d_alpha/num),start[1]+i*(d_phi/num));
            if( imgsurf is not None ):
                self.render( imgsurf, ifcollide );