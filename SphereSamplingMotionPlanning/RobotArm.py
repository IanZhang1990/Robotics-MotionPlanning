import pygame;
import math;
from time import sleep

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
        # Ref: http://blog.csdn.net/freezhanacmore/article/details/9568873
        ab = ( end2[0] - end1[0], end2[1] - end1[1]);
        ac = ( point[0]- end1[0], point[1]-end1[1] );
        bc = ( point[0]- end2[0], point[1]-end2[1] )
        
        if( ab[0]*ac[0]+ab[1]*ac[1] < 0 ):
            return math.sqrt( ac[0]**2 + ac[1]**2 );
        elif( ab[0]*bc[0]+ab[1]*bc[1] > 0 ):
            return math.sqrt( bc[0]**2 + bc[1]**2 );
        else:
            return math.fabs( ab[0]*ac[1]-ab[1]*ac[0] ) / math.sqrt( ab[0]**2 + ab[1]**2 );

    def render(self, imgSurface, ifcollide, color=(0,0,180)):
        """Render the robot to the image"""
        alpha = self.mAlpha;
        phi = self.mPhi;

        base = self.mPos;
        end1 = (base[0]+self.mLen1*math.cos(alpha),    base[1]+self.mLen1*math.sin(alpha));
        end2 = (end1[0]+self.mLen2*math.cos(phi+alpha), end1[1]+self.mLen2*math.sin(phi+alpha));

        if( ifcollide ):
            color = (250, 0, 0)

        for event in pygame.event.get():
            pass;
        pygame.draw.line( imgSurface, color, base, end1, 2 ); 
        pygame.draw.line( imgSurface, color, end1, end2, 2 );
        pygame.display.update();
        return;

    def move(self, start, goal, beginColor=(0,0,180), endColor=(0,0,180), imgsurf=None):
        """Given two configurations, we want to move from start --> goal"""
        d_alpha = goal[0] - start[0];
        d_phi = goal[1] - start[1];
        dist = math.sqrt( d_alpha**2 + d_phi**2 );
        num = int( dist/0.1);
        if num == 0:
            num = 1;
        delta_blue = (endColor[2] - beginColor[2])/num;
        for i in range(0,num):
            ifcollide = self.setParams( start[0]+i*(d_alpha/num),start[1]+i*(d_phi/num));
            color = (math.fabs(100-(beginColor[0]+delta_blue*i)), (beginColor[1]+delta_blue*i)/1, math.fabs( 180-(beginColor[2]+delta_blue*i)/1));
            if( imgsurf is not None ):
                self.render( imgsurf, ifcollide, color );
            sleep(0.2);