import math
import sys, os
from collections import defaultdict
from SampleManager import DistSample
import numpy;
import utility;

class Grid:
    def __init__(self, dimLens, center = None):
        """@param center: center of the grid;
         @param dimLens: length in each dimension"""
        self.mCenter = center;
        self.mDimLens = dimLens;
        self.mContainer = [];

    def addSphere( self, sphere ):
        if( self.contains( sphere ) ):
            return;
        self.mContainer.append( sphere );

    def contains( self, sphere):
        for item in self.mContainer:
            if item == sphere:
                return True;
        return False;

    def inside( self, point ):
        """determine if a point is inside the grid"""
        for i in range( 0, len(point) ):
            if math.fabs( self.mCenter[i] - point[i] ) > self.mDimLens[i]/2.0:
                return False;
        return True;

    def __findFarestPoint__( self, outPoint ):
        """from direction center-->outPoint, this method finds a point that is farest from
         the center of the grid, yet still inside the grid."""
        end = outPoint;
        endInside = self.inside( end );
        if endInside: return outPoint;
        start = self.mCenter;
        startInside = self.inside( start );
        
        while( True ):
            if ( utility.euclideanDistSqr( start, end ) <= 2 ):
                return start;
            mid = utility.devide( utility.add( start, end ), 2);
            if self.inside( mid ):
                start = mid;
            else:
                end = mid;

    def intersect( self, sphere, dim ):
        """Determine if the grid intersect with a sphere"""
        nearest = self.__findFarestPoint__( sphere.mSample );
        dist = utility.euclideanDistSqr( nearest, sphere.mSample );
        if( dist < sphere.mRadius**2 ):
            return True;
        else:
            return False;

class SpacePartition:
    def __init__( self, maxDimLens, unitDimLens ):
        dim = len(maxDimLens);
        self.mMaxDimLens = maxDimLens;
        self.mUnitDimLens = unitDimLens;
        num = 1;
        dimNums = [0]*len(maxDimLens);
        for i in range( 0, len(maxDimLens) ):
            dimNums[i] = int(maxDimLens[i] / unitDimLens[i]);
            num *= dimNums[i];

        self.mGrids = [];
        for i in range( 0, num ):
            grid = Grid( unitDimLens );
            self.mGrids.append(grid);
        self.mGrids = numpy.array( self.mGrids );
        self.mGrids.shape = dimNums;

        for index, item in numpy.ndenumerate( self.mGrids ):
            center = [0] * dim;
            for i in range( 0, dim ):
                center[i] = int(index[i]) *unitDimLens[i] + unitDimLens[i]/2.0;
            item.mCenter = center;

    def addSphere( self, sphere ):
        center = sphere.mSample;
        ctrIdx = self.indxHash( center );
        radius = sphere.mRadius;
        dim = len( center );
        #indices, values = numpy.ndenumerate( self.mGrids );
        idx = 0;
        for index, item in numpy.ndenumerate( self.mGrids ):
            if item.intersect( sphere, dim ):
                print index;
                item.addSphere(sphere);
            idx += 1;
        return;

    def getContainingGrid( self, point ):
        """Given a point in n-D world, return the grid containing it."""
        idx = self.indxHash( point );
        return self.mGrids[idx];

    def indxHash( self, point ):
        """Given a point in n-D world, return the index containing the point"""
        dim = len( point );
        dimIdx = [0] * dim;
        for i in range(0, dim):
            dimIdx[i] = int(point[i]) / int( self.mUnitDimLens[i] )
        return tuple(dimIdx);


######### TEST ######################
world = [ 1000, 1000 ];
unitLen = [ 100, 100 ];
sphere = DistSample( ( 100, 300 ), 40 );
sphere2 = DistSample( ( 500, 600 ), 200 );

spacePart = SpacePartition( world, unitLen );
spacePart.addSphere( sphere );
spacePart.addSphere( sphere2 );

