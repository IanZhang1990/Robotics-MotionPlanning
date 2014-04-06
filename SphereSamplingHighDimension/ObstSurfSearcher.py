
import math;
import utility;

class Segment:
    def __init__(self, collisionMgr):
        """@param collisionMgr: collision manager to detect collision"""
        self.mClsnMgr = collisionMgr;
        pass;


    def search( self, start, end, minDist ):
        """@param start: a point in C-space
         @param end: the end point in C-Space
         @param minDist: the min dist for binary search to consider a point precise enough"""
        startCollide = self.mClsnMgr.ifCollide( start );
        endCollide = self.mClsnMgr.ifCollide(end);
        if ( startCollide == endCollide ):
            return None;
        
        while( startCollide != endCollide ):
            if( utility.euclideanDist( start, end ) <= minDist ):
                if( startCollide == False ):
                    return start;
                else:
                    return end;
            sum = utility.add( start, end );
            mid = utility.devide( sum, 2 );
            midCollide = self.mClsnMgr.ifCollide( mid );
            if( midCollide == startCollide ):
                start = mid;
                startCollide = midCollide;
            else:
                end = mid;
                endCollide = midCollide;

class ObstSurfSearcher(object):
    """to find configurations that are closed to obstacles in C-Space"""
    def __init__( self, collisionMgr ):
        self.mClsnMgr = collisionMgr;
        self.mSurfSamples = [];
    
    def searchObstSurfConfigs( self, freeSamples, obstSamples, minDist ):
        for start in freeSamples:
            for end in obstSamples:
                newSeg = Segment( self.mClsnMgr );
                surfSample = newSeg.search( start, end, minDist );
                if surfSample is not None:
                    self.mSurfSamples.append( surfSample );

"""
import pygame;
import random;

class Sphere:
    def __init__( self, pos, radius ):
        self.mP = pos;
        self.mR = radius;
        pass;

    def isInside( self, point ):
        dist = ( point[0] - self.mP[0] )**2 + ( point[1] - self.mP[1] )**2;
        if dist <= self.mR**2:
            return True;
        else:
            return False;
    def ifCollide( self, point ):
        return self.isInside( point );
    
    def render(self, imgSurf, color):
        pygame.draw.circle( imgSurf, color, self.mP, self.mR );




pygame.init();
WIDTH = 1000;
HEIGHT = 1000;
DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT));

Obst = Sphere( (WIDTH/2, HEIGHT/2), 100 );

Obst.render( DISPLAYSURFACE, (50,50,50) );

freeSamps = [];
obstSamps = [];

for i in range( 1, 20 ):
    randX = random.randint( 1, 1000 );
    randY = random.randint( 1, 1000 );
    if( Obst.isInside(  (randX, randY) ) ):
        obstSamps.append( (randX, randY) );
    else:
        freeSamps.append( (randX, randY) );



searcher = ObstSurfSearcher( Obst );
searcher.searchObstSurfConfigs( freeSamps, obstSamps, 5 );

for samp in searcher.mSurfSamples:
    point = (samp[0], samp[1]);
    pygame.draw.circle( DISPLAYSURFACE, ( 0,150,0 ), point, 1 );

pygame.image.save( DISPLAYSURFACE, "testSurfSampling.PNG" );
pygame.quit();
"""