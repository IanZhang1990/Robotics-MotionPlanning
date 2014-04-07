
import math;
import utility;
from sklearn.neighbors import NearestNeighbors
import numpy as np

class Segment:
    def __init__(self, collisionMgr, cspace):
        """@param collisionMgr: collision manager to detect collision"""
        self.mClsnMgr = collisionMgr;
        self.mCSpace = cspace;
        pass;

    def search( self, start, end, minDist ):
        """@param start: a point in C-space
         @param end: the end point in C-Space
         @param minDist: the min dist for binary search to consider a point precise enough"""
        startAngles = self.mCSpace.map2UnscaledSpace( start );
        endAngles = self.mCSpace.map2UnscaledSpace( end )
        startCollide = self.mClsnMgr.ifCollide( startAngles );
        endCollide = self.mClsnMgr.ifCollide(endAngles);
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
            midAngles = self.mCSpace.map2UnscaledSpace( mid )
            midCollide = self.mClsnMgr.ifCollide( midAngles );
            if( midCollide == startCollide ):
                start = mid;
                startCollide = midCollide;
            else:
                end = mid;
                endCollide = midCollide;

class ObstSurfSearcher(object):
    """to find configurations that are closed to obstacles in C-Space"""
    def __init__( self, collisionMgr, cspace ):
        self.mCSpace = cspace;
        self.mClsnMgr = collisionMgr;
        self.mSurfSamples = [];
        self.mSurfSampNumpy = None;
        self.mNeigh = None;
    
    def searchObstSurfConfigs( self, freeSamples, obstSamples, minDist ):
        for start in freeSamples:
            for end in obstSamples:
                newSeg = Segment( self.mClsnMgr, self.mCSpace );
                surfSample = newSeg.search( start, end, minDist );
                if surfSample is not None:
                    self.mSurfSamples.append( surfSample );
                    pass;
                pass;
            pass;
        self.mSurfSampNumpy = np.array( [self.mSurfSamples] );
        self.mNeigh = NearestNeighbors( n_neighbors = 2, algorithm = 'kd_tree', metric = 'euclidean' );
        self.mNeigh.fit( self.mSurfSampNumpy );

    def getNearest( self, config ):
        dist, indx = neigh.kneighbors( config );
        return dist[0][0], self.mSurfSampNumpy[indices[0]][0];



X = np.array([[-1, -1], [-2, -2], [-3, -3], [1.5, 1.5], [2, 2], [3, 3]])
neigh = NearestNeighbors(n_neighbors = 1, algorithm = 'kd_tree', metric = 'euclidean')
neigh.fit( X );

distances, indices = neigh.kneighbors([1,1]);


print X[indices[0]][0];
print distances[0];



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