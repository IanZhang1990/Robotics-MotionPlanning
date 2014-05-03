
from random import randrange, uniform

import sys, os, datetime
import math
from Ray import *
from World import *
from SpacePartition import *;
from ObstSurfSearcher import *
#import pygame
from Queue import Queue
from collections import defaultdict
import multiprocessing
from multiprocessing  import Process, Manager, Value, Array
import signal

def signal_handler(signum, frame):
	raise Exception( "Timed Out!!!" );


class DistSample:
    """Sample with distance to obstacles.
	A dist sample can be viewed as a sphere in Rn space"""
    def __init__(self, pos, radius):
        self.mSample = pos
        self.mRadius = radius;
        self.mBoundaries = None;

    def getBoundaryConfigs(self, maxDimLens, num=0):
        """ Get configs in the boundary of the sphere.
         @param maxDimLens: max length of each dimension
         @param num: the number of boundary configs you need.
         When num = 0, automatically get boundary configs."""

        #return [];

        if self.mBoundaries is not None:
            return self.mBoundaries;

        bndRadius = self.mRadius*1.212;
        if( self.mRadius ) < 5:
            return [];

        self.mBoundaries = []
        if( num == 0 ):
            num = bndRadius*3;
        if num < 20:
            num = 20;

        dlt_ang = (2*math.pi) / float(num); # increment of angle;
        for i in range(1, int(num)+1):
            ang = dlt_ang * i;
            newX = self.mSample[0]+(bndRadius)*math.cos( ang );
            newY = self.mSample[1]+(bndRadius)*math.sin( ang );
            self.mBoundaries.append((newX, newY));
        return self.mBoundaries;
    
    def isInside(self, position, maxDimLens):
        """Determine if a position is inside the sphere"""
        dim = len(position);
        deltas = [0] * dim;
        distSqr = 0;
        for i in range(0, dim):
            deltas[i] = math.fabs(position[i] - self.mSample[i]);
            if math.fabs(maxDimLens[i] - deltas[i]) < deltas[i]:
                deltas[i] = math.fabs(maxDimLens[i] - deltas[i]);
            distSqr += deltas[i]**2;

        if distSqr < ( self.mRadius**2 ):
            return True;
        else:
            return False;

    def isInsideEpsBall( self, position, maxDimLens ):
        dim = len(position);
        deltas = [0] * dim;
        distSqr = 0;
        for i in range(0, dim):
            deltas[i] = math.fabs(position[i] - self.mSample[i]);
            if math.fabs(maxDimLens[i] - deltas[i]) < deltas[i]:
                deltas[i] = math.fabs(maxDimLens[i] - deltas[i]);
            distSqr += deltas[i]**2;

        if distSqr < ( self.epsRadius()**2 ):
            return True;
        else:
            return False;

    def epsRadius( self ):
        return self.mRadius/5.0;

class SampleManager:
    def __init__( self, CSpace ):
        self.mCSpace = CSpace;
        self.mCollisionMgr = CSpace.mObstMgr;
        self.mDistSamples = [];
        self.mFreeSamples = [];
        self.mObstSamples = [];
        self.mDelta = 5.0;
        self.g_failTimes = Value( 'i', 0 );
        unitLens = [136.6, 76.8];
        self.mSpacePartition = SpacePartition( self.mCSpace.mMaxDimLens, unitLens );

    def getFreeSamples( self, num, dim, maxDimLens ):
        """get num number of free samples in C-Space"""
        size = 0; 
        while size < num:
            rnd = [0] * dim;
            for i in range( 0, dim ):
                rnd[i] = randrange( 0, maxDimLens[i] );
                pass
            if( self.mCollisionMgr.ifCollide( rnd ) ):
                self.mFreeSamples.append( rnd );
                size += 1;

    def getCSpaceBoundaryPoints(self):
        for i in range( 3, int(1366/5.0) ):
            self.mFreeSamples.append( (i, 3 ) );
        for i in range( 3, int(765/3) ):
            self.mObstSamples.append( ( 3, i ) );

    def randomSample( self, num, dim, maxDimLens ):
        #self.getCSpaceBoundaryPoints();

        for i in range( 0, num ):
            rnd = [0] * dim;
            for i in range( 0, dim ):
                rnd[i] = randrange( 0, maxDimLens[i] );
                pass
            if( self.mCollisionMgr.ifCollide( rnd ) ):
                self.mFreeSamples.append( rnd );
            else:
                self.mObstSamples.append( rnd );
     
    def getARandomFreeSample(self, num, surfSearcher, maxDimLens, dim):
        """Randomly sample the space and return a free sample (with distance info).
         The sample is not inside of any other sphere. Also, this method will not automatically 
         add the new sample to self.mDistSamples list.
         @param num: fail time. If failed to find such a sample num times, return null"""
        failTime=0;
        while( failTime < num ):
            rnd = [0] * dim;
            for i in range( 0, dim ):
                rnd[i] = randrange( 0, maxDimLens[i] );
                pass
            if( self.mCollisionMgr.ifCollide( rnd ) ):
                continue;

            newSamp = True;

            grid = self.mSpacePartition.getContainingGrid( rnd );
            for sphere in grid.mContainer:
                if sphere.isInside( rnd, maxDimLens ):
                    newSamp = False;
                    failTime += 1
                    break;

            if newSamp:
                # randomly shoot rays to get the nearest distance to obstacles
                #rayShooter = RayShooter( rnd, self.mCollisionMgr, self.mCSpace );
                dist, neighbor = surfSearcher.getNearest( rnd ); # Get the distance to obstacles
                if math.fabs(dist) >= self.mDelta:
                    newDistSamp = DistSample( rnd, dist );
                    #print "failed times: {0}".format( failTime );
                    failTime=0;
                    return newDistSamp;
                else:
                    failTime += 1;
                    print "failed times: {0}".format( failTime );
        
        print "failed times: {0}".format( failTime );
        return None;
           

    def randDistSampleUsingObstSurf( self, num ):
        maxDimLens = self.mCSpace.mMaxDimLens;
        self.randomSample( 1000, len(maxDimLens), maxDimLens );
        searcher = ObstSurfSearcher(self.mCollisionMgr, self.mCSpace);
        searcher.searchObstSurfConfigs( self.mFreeSamples, self.mObstSamples, 1 );

        self.mDistSamples = [];
        boundaryQueue = [];
        bndSphDict = defaultdict();
        randFreeSamp = 1234;

        while( True ):
            pass;


    def distSampleUsingObstSurfSamps( self, num ):
        """@param num: failure time to sample a new configuration randomly"""
        maxDimLens = self.mCSpace.mMaxDimLens;
        self.randomSample(  1000, len(maxDimLens), maxDimLens );
        searcher = ObstSurfSearcher(self.mCollisionMgr, self.mCSpace);
        searcher.searchObstSurfConfigs( self.mFreeSamples, self.mObstSamples, 2);

        self.mDistSamples = [];
        boundaryQueue = [];
        bndSphDict = defaultdict();
        randFreeSamp = 1234;

        while( randFreeSamp != None ):
            randFreeSamp = self.getARandomFreeSample( num, searcher, maxDimLens, len(maxDimLens) );
            if( randFreeSamp == None ):
                return;
            self.mDistSamples.append( randFreeSamp );
            self.mSpacePartition.addSphere( randFreeSamp );
            bounds = randFreeSamp.getBoundaryConfigs( maxDimLens );

            if( len(self.mDistSamples)%100 == 0 ):
                print "Dist samples: {0}".format( len(self.mDistSamples) );

            for bndConfig in bounds:
                #if not bndConfig in bndSphDict:			# put the boundconfig-sphere relation to the dictionary
                bndSphDict[str(bndConfig)] = randFreeSamp;
                boundaryQueue.append( bndConfig );				# put the boundary config to the queue.

            while( len( boundaryQueue) != 0 ):
                bnd = boundaryQueue[0];							# get a new boundary
                del boundaryQueue[0]
                newSamp = True;
                if self.mCollisionMgr.ifCollide( bnd ):
                    continue;

                if(self.mCollisionMgr.isOutOfWorld( bnd ) ):
                    continue;

                grid = self.mSpacePartition.getContainingGrid( bnd );
                for sphere in grid.mContainer:
                    if sphere.isInside( bnd, maxDimLens ):
                        newSamp = False;
                        break;

                if newSamp:
                    # get the nearest distance to obstacles
                    dist, neighbor = searcher.getNearest( bnd );              # Get the distance to obstacles
                    if (dist) >= self.mDelta:	    					 # if not too close to obstacles
                        newDistSamp = DistSample(bnd, dist)	# construct a new dist sample
                        print "{0}  R: {1}".format( bnd, dist );
                        self.mDistSamples.append( newDistSamp );				# add to our dist sample set
                        self.mSpacePartition.addSphere( newDistSamp );         ############# Add new sphere to space partition
                        #if( len(self.mDistSamples) >= 800 ):
                        #    return;
                        bounds = newDistSamp.getBoundaryConfigs(maxDimLens);		# get the boundary configs
                        if len(bounds) == 0:
                            continue;
                        for bndConfig in bounds:
                            #if not bndConfig in bndSphDict:				# put the boundconfig-sphere relation to the dictionary
                            bndSphDict[str(bndConfig)] = newDistSamp;
                            boundaryQueue.append( bndConfig );				# put the boundary config to the queue.
                        
                        ###########################=========================================================
                        """
                        if len(self.mDistSamples)%30 == 0:
                            print "------------ FRESH -------------"
                            idx = 0;
                            for bnd in boundaryQueue:
                                grid = self.mSpacePartition.getContainingGrid( bnd );
                                for sphere in grid.mContainer:
                                    if sphere.isInside( bnd, maxDimLens ):
                                        try:
                                            del boundaryQueue[idx];
                                            idx -= 1;
                                        except:
                                            pass;
                                idx += 1;
                        """

                        #    for sphere in self.mDistSamples:
                        #        boundaryQueue = [x for x in boundaryQueue if( not sphere.isInside(x, maxDimLens)) ]
                        ###########################=========================================================

                        print "\t\t\t\t\t\t\t\t\t\t{0}\n".format(len(boundaryQueue));
                        

    def renderDistSample(self, ImgSurface):
        """Render distance sample to image"""
        print "render {0} dist samples to the image".format( len(self.mDistSamples) );
        freeColor = ( 0, 220, 0 );
        obstColor = ( 200, 0, 100 );
        for samp in self.mDistSamples:
            if samp.mRadius > 0: # Free sample
                pygame.draw.circle( ImgSurface, freeColor, (int(samp.mSample[0]), int(samp.mSample[1])), int(math.fabs(samp.mRadius)), 0);
            else:
                pygame.draw.circle( ImgSurface, obstColor, (int(samp.mSample[0]), int(samp.mSample[1])), int(math.fabs(samp.mRadius)), 1 );
            #if(samp.mRadius/5.0 >= 4):
            #    pygame.draw.circle( ImgSurface, ( 0, 200, 0 ), (int(samp.mSample[0]), int(samp.mSample[1])), int(math.fabs(samp.epsRadius())) );


    def writeSamplesToFile( self, filename ):
        file2write = open( filename, 'w' );
        formattedData = ""
        for vector in self.mDistSamples:
            for i in range( 0, len(vector.mSample) ):
                formattedData += str( vector.mSample[i] ) + "\t";
            formattedData += str(vector.mRadius);
            formattedData += "\n";
            pass
        
        file2write.write( formattedData );
        file2write.close();

    def loadDistSamplesFromFile( self, filename ):
        file2read = open( filename, 'r' );
        self.mDistSamples = [];
        lineNum = 0;
        for line in file2read:
            if( lineNum % 300 == 0 ):
                print "Reading line: {0}".format( lineNum );
            lineNum += 1;
            strDistSamp = line;
            info = strDistSamp.split( '\t' );
            dim = len(info);
            pos = [0] * (dim-1);
            for i in range(0,dim-1):
                pos[i] = float( info[i] );
            radius = float(info[dim-1]);
            distSamp = DistSample(tuple(pos), radius);
            if( distSamp.mRadius >= 3 ):
                self.mDistSamples += [ distSamp ];
                self.mSpacePartition.addSphere( distSamp );