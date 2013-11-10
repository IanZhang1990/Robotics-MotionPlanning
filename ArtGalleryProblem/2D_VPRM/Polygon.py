import pygame
from Line import Line
class Polygon(object):
    """Class to describe simple polygons"""

    def __init__(self):
        self.mLines = [];
        self.mPoints = [];

        #self.mPoints = [(100,100), (200,100), (200,200), (100,200)];
        self.mPoints = [(200,200), (350,400), (500,240), (650,400), (800,200)];

        x = []
        y = []
        for point in self.mPoints:
            x = x + [point[0]]
            y = y + [point[1]]
        
        self.mMinX = min( x );
        self.mMinY = min( y );
        self.mMaxX = max( x );
        self.mMaxY = max( y );

        for i in range(1, len(self.mPoints)):
            self.mLines = self.mLines + [Line( self.mPoints[i-1][0], self.mPoints[i-1][1], self.mPoints[i][0], self.mPoints[i][1])]
        self.mLines = self.mLines + [Line( self.mPoints[-1][0], self.mPoints[-1][1], self.mPoints[0][0], self.mPoints[0][1] )]
        pass

    def readFile( self, filename ):
        """Read polygon information from a file"""
        # For test
        self.mPoints = [(0,0), (80,0), (80,80), (0,80)];

        pass;

    def pointInPoly(self, x,y):
        """poly = [(0,0), (80,0), (80,80), (0,80)]"""
        n = len(self.mPoints)
        inside = False

        p1x,p1y = self.mPoints[0]
        for i in range(n+1):
            p2x,p2y = self.mPoints[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    def render(self, screen):
        for line in self.mLines:
            line.render( screen )
        pass