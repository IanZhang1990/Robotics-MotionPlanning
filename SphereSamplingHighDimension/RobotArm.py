#import pygame;
import math;
from time import sleep

#from GameWorld import Sphere;


class Sphere:
    def __init__( self, x, y, r ):
        self.mPos = (x, y);
        self.mRadius = r;

    def render(self, imgsurface, color):
        """Render the sphere"""
        pygame.draw.circle( imgsurface, color, self.mPos, self.mRadius );


class RobotArm(object):
    """description of class"""
    def __init__( self, position, obstacles, lengths ):
        """Create a 1-joint robot arm
         @parm position: the base position.
         @parm obstacles: a list of spheres as obstacles.
         @parm lengths: a list of lengths of each joint
         """
        self.mPos = position;
        self.mLengths = lengths;
        self.mAngles = [0] * len(self.mLengths);
        self.mEnds = [(0,0)] * len(self.mLengths);
        self.mObsts = obstacles;

    def setParams( self, angles ):
        """Set angles of the robot arm, return if collide with obstacles."""
        self.mAngles = angles;

        base = self.mPos;
        self.mEnds = [(0,0)] * (len(self.mLengths)+1);
        self.mEnds[0] = base;
        lastAngleSum = 0;
        for i in range( 1, len(self.mLengths)+1 ):
            lastAngleSum += self.mAngles[i-1];
            lastX = self.mEnds[i-1][0];
            lastY = self.mEnds[i-1][1];
            Xpos = lastX + self.mLengths[i-1] * math.cos( lastAngleSum );
            Ypos = lastY + self.mLengths[i-1] * math.sin( lastAngleSum );
            self.mEnds[i] = (Xpos, Ypos);

        for i in range( 1, len(self.mEnds) ):
            for obstacle in self.mObsts:
                dist = self.point2LineDist( obstacle.mPos, self.mEnds[i-1], self.mEnds[i] );
                if dist < obstacle.mRadius:
                    return True;
        return False;

    def point2LineDist(self, point, end1, end2):
        """Distance from one point to a segment of line ( end1 --> end2 )"""
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
        if( ifcollide ):
            color = (250, 0, 0)

        for event in pygame.event.get():
            pass;

        for i in range(1, len(self.mEnds)):
            pygame.draw.line( imgSurface, color, self.mEnds[i-1], self.mEnds[i], 3 ); 
        pygame.display.update();
        return;

    def move(self, start, goal, beginColor=(0,0,180), endColor=(0,0,180), imgsurf=None):
        """Given two configurations, we want to move from start --> goal"""
        d_angles = [0] * len(self.mAngles)
        dist = 0;
        for i in range( 0, len(self.mAngles) ):
            d_angles[i] = start[i] - goal[i];
            dist += d_angles[i]**2;
        dist = math.sqrt( dist );
        num = int( dist/0.1);
        if num == 0:
            num = 1;
        delta_blue = (endColor[2] - beginColor[2])/num;
        for i in range(0,num):
            tempAngles = start;
            for j in range(0,len(self.mAngles)):
                tempAngles[j] = start[j] + i * (d_angles[j]/num);
            ifcollide = self.setParams( tempAngles );
            color = (math.fabs(100-(beginColor[0]+delta_blue*i)), (beginColor[1]+delta_blue*i)/1, math.fabs( 180-(beginColor[2]+delta_blue*i)/1));
            if( imgsurf is not None ):
                self.render( imgsurf, ifcollide, color );
                sleep(0.1);