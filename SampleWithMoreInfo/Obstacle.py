
from random import randrange, uniform
import pygame, math


class Obstacle:
    def __init__(self):
        self.Name = "obstacle"
        pass

    def render(self, surface, color, thickness):
        pass;

    def isInside(self, x, y):
        """ Virtual super class of obstacles """
        raise Exception("Not implemented, yet");
        return False;
    
    def rayIntersect( self, ray ):
        """Test if a ray hits the object. This is for spheres and rectangles only"""
        raise Exception("Not implemented, yet");

class Rect(Obstacle):
    def __init__(self, x, y, width, height):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height
        self.Name = "Rectangle"
        pass;

    def render( self, surface, color, thickness ):
        pygame.draw.rect( surface, color, (self.X, self.Y, self.Width, self.Height), thickness );
        pass

    def isInside(self, x, y):
        """Determine if 2D point (x, y) is in the rectangle"""
        if x > self.X and x < (self.X+self.Width) and y > self.Y and y < (self.Y+self.Height):
            return True;
        else:
            return False;

class Circle(Obstacle):
    def __init__( self, x, y, radius ):
        self.X = x
        self.Y = y
        self.Radius = radius
        self.Name = "Circle"
        pass

    def render( self, surface, color, thickness ):
        pygame.draw.circle( surface, color, (self.X, self.Y), self.Radius, thickness );
        pass

    def isInside( self, x, y ):
        dist2 = (self.X-x)*(self.X-x) + (self.Y-y)*(self.Y-y);
        if dist2<= self.Radius*self.Radius:
            return True;
        else:
            return False;

class ObstaclesManager:
    def __init__(self, scrWidth, scrHeight):
        self.mObstacles = []
        self.mScreenWidth = scrWidth;
        self.mScreenHeight = scrHeight;

    def generateObstacles( self, rectNum, cirNum, minWidth, maxWidth, minHeight, maxHeight ):
        obs = []
        for i in range( 0, rectNum ):
            w = randrange( 50, 150 );
            h = randrange( 50, 150 );
            x = randrange( minWidth, maxWidth-w );
            y = randrange( minHeight, maxHeight-h );
            obs = obs + [Rect(x,y,w,h)];
            pass;

        for i in range( 0, cirNum ):
            r = randrange( 30, 100 );
            x = randrange( r, maxWidth-r );
            y = randrange( r, maxHeight-r );
            obs = obs + [Circle(x, y, r)];
            pass;

        self.mObstacles = obs;

        return obs; 

    def getObstacles(self):
        return self.mObstacles;

    def addObstacle(self, obst):
        self.mObstacles += [obst];

    def isPathFree( self, start, end ):
        """Check if the path between start --> end is free.
        Note: This is for 2D only!
        @param start:    start position of the path
        @param end:        end position of the path
        """
        if len(start)>2 or len(end) > 2:
            raise Exception( "This method is for 2D only now." );

        dx = end[0]-start[0];
        dy = end[1]-start[1];
        length = math.sqrt( dx**2 + dy**2 );
        if math.fabs(length) < 0.001:
            return True;
        cosTheta = dx / length;
        sinTheta = dy / length;
        stepLen = 1.0;

        isInitInside = False;
        nextCheckPoint = ( start[0]+stepLen*cosTheta, start[1]+stepLen*sinTheta );
        dist2End = length-1.0;
        i = 0;                 # Steps
        while( dist2End >= 1.0 ):
            if( self.isConfigInObstacle( nextCheckPoint ) ):
                return False;
            nextCheckPoint = ( start[0]+stepLen*i*cosTheta, start[1]+stepLen*i*sinTheta );
            dist2End = math.sqrt( (nextCheckPoint[0]-end[0])**2 + (nextCheckPoint[1]-end[1])**2 );
            i += 1;
        return True;

    def ifCollide( self, sample ):
        return self.isConfigInObstacle(sample);

    def isConfigInObstacle(self, sample):
        space = Rect( 0,0, self.mScreenWidth, self.mScreenHeight );

        if not space.isInside( sample[0], sample[1] ):
            return True;

        for obst in self.mObstacles:
            if( obst.isInside(sample[0], sample[1]) ):
                return True;
        return False;

    def isOutOfWorld(self, sample):
        space = Rect( 0,0, self.mScreenWidth, self.mScreenHeight );
        if not space.isInside( sample[0], sample[1] ):
            return True;