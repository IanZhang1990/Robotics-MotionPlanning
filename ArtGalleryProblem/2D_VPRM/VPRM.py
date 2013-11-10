import pygame
from Line import Line
import random;


class VPRM(object):
    """VPRM Solver"""

    def __init__(self, polygon):
        self.mPolygon = polygon;
        self.mGuards = []
        self.mAllSamples = [];
        self.mUpdate = True;
        self.mMisMatch = 0;
        self.mSolved = False;
        pass

    def solveStep( self, threshold, screen ):
        if self.mMisMatch < threshold:
            # Generate a random sample
            random.seed();
            rndX = random.randint( self.mPolygon.mMinX, self.mPolygon.mMaxX ) 
            rndY = random.randint( self.mPolygon.mMinY, self.mPolygon.mMaxY ) 
            sample = (rndX, rndY);
            self.mAllSamples = self.mAllSamples + [sample];
            #print sample;

            # if the sample is not inside the polygon
            if not self.mPolygon.pointInPoly( rndX, rndY ):
                return;

            if( len(self.mGuards) == 0 ):  # first valid point is always a guard
                self.mGuards = self.mGuards + [ sample ];
                print "Got one guard!\n"
                return;

            # Test each edge of the polygon and the line btw a gurad and the sample
            passTest = False;
            innerPass = 0;
            for guard in self.mGuards:
                line1 = Line( guard[0], guard[1], rndX, rndY );
                guardEdgeIntersectCount = 0;
                for line2 in self.mPolygon.mLines:
                    if line1.intersect( line2 ):
                        guardEdgeIntersectCount += 1;
                        break;
                    pass
                if guardEdgeIntersectCount == 0: # the sample can see the existing guard
                    passTest = False;
                    continue;
                else:
                    innerPass += 1;
            
            if innerPass == len(self.mGuards):
                passTest = True;

            if passTest:
                self.mGuards = self.mGuards + [ sample ];
                self.mUpdate = True;
                self.mMisMatch = 0;
                print "Got one guard!\n"
            else:
                self.mMisMatch = self.mMisMatch + 1;
            pass;
        else:
            print "Solved. Guards number: " + str( len(self.mGuards) );
            self.mSolved = True;
            return;

    def render(self, screen):
        self.mPolygon.render(screen);
        for i in range( 0, len(self.mAllSamples) ):
            pygame.draw.circle(screen, (255,0,0), (self.mAllSamples[i][0],self.mAllSamples[i][1]), 3, 1)
        for i in range( 0, len(self.mGuards) ):
            pygame.draw.circle(screen, (0,0,0), (self.mGuards[i][0],self.mGuards[i][1]), 5, 3)
        pass



