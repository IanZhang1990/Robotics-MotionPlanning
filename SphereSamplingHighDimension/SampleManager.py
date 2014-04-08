
from random import randrange, uniform

import sys, os, datetime
import math
from Ray import *
from CSpaceWorld import *
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
        
        if self.mBoundaries is not None:
            return self.mBoundaries;

        def prod(n):
            """Product of elements"""
            result = 1;
            for i in range(1, n+1):
                result = result * i;
            return result;

        def surf( radius, n ):
            """Surface of """
            if n != 3:
                raise Exception( "Please use 3-Dimension first" );
            return 2* (math.pi**2) * (radius**3);
         
        
        dlt = 25;
        dim = len(self.mSample);
        if num == 0:
            num = int( (surf( self.mRadius, dim ) / ( dlt**2 * 1.73205 / 4.0 )  + 1));
            if num ==0: num = 10;
        if num > 500:
            num = 500;

        bnds = list();
        for i in range(0, num):
            temp = [0] * dim;
            length = 0;
            for j in range(0, dim):
                temp[j] = randint( -100, 100 );
                length += temp[j]**2;
            length = math.sqrt( length );
            if length == 0:
                continue;
            for j in range(0, dim):
                temp[j] = (float(temp[j]) / float(length)) * (self.mRadius + 2) + self.mSample[j];
                if temp[j] < 0: temp[j] = maxDimLens[j] + temp[j];
                else: temp[j] = temp[j] % maxDimLens[j]; 

            bnds.append( temp );
        
        return bnds;

        #if( num == 0 ):
        #    num = self.mRadius / 5 + 5;
            
        #dlt_ang = (2*math.pi) / float(num); # increment of angle;
        #dlt_dist = self.mRadius / 10;
        #if dlt_dist > 1.0:
        #    dlt_dist = 1.0;
        #for i in range(1, int(num)+1):
        #    ang = dlt_ang * i;
        #    newX = self.mSample[0]+(self.mRadius+dlt_dist)*math.cos( ang );
        #    if newX < 0:                                            # Warp the space
        #        newX = maxWidth + newX;
        #    else:
        #        newX = newX % maxWidth;                              # Warp the space
        #    newY = self.mSample[1]+(self.mRadius+dlt_dist)*math.sin( ang );
        #    if newY < 0:                                            # Warp the space
        #        newY = maxHeight + newY;
        #    else:
        #        newY = newY % maxHeight;                             # Warp the space

        #    retSet += [ (newX, newY) ]
        #return retSet;
    
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

class SampleManager:
    def __init__( self, CSpace ):
        self.mCSpace = CSpace;
        self.mCollisionMgr = CSpace.mCollisionMgr;
        self.mDistSamples = Manager().list();
        self.mFreeSamples = [];
        self.mObstSamples = [];
        self.g_failTimes = Value( 'i', 0 );

    def getFreeSamples( self, num, dim, maxDimLens ):
        """get num number of free samples in C-Space"""
        size = 0; 
        while size < num:
            rnd = [0] * dim;
            for i in range( 0, dim ):
                rnd[i] = randrange( 0, maxDimLens[i] );
                pass
            angles = self.mCSpace.map2UnscaledSpace( rnd );
            if( self.mCollisionMgr.ifCollide( angles ) ):
                self.mFreeSamples.append( rnd );
                size += 1;

    def randomSample( self, num, dim, maxDimLens ):
        for i in range( 0, num ):
            rnd = [0] * dim;
            for i in range( 0, dim ):
                rnd[i] = randrange( 0, maxDimLens[i] );
                pass
            angles = self.mCSpace.map2UnscaledSpace( rnd );
            if( self.mCollisionMgr.ifCollide( angles ) ):
                self.mFreeSamples.append( rnd );
            else:
                self.mObstSamples.append( rnd );
     
    def getARandomFreeSample(self, num, maxDimLens, dim):
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
            angles = self.mCSpace.map2UnscaledSpace( rnd );
            if( self.mCollisionMgr.ifCollide( angles ) ):
                continue;

            newSamp = True;
            for sample in self.mDistSamples:
                if sample.isInside( rnd, maxDimLens ):
                    newSamp = False;
                    failTime += 1
                    break;
            if newSamp:
                # randomly shoot rays to get the nearest distance to obstacles
                rayShooter = RayShooter( rnd, self.mCollisionMgr, self.mCSpace );
                dist = rayShooter.randShoot(50 * (dim-1));
                if math.fabs(dist) >= 1.0:
                    newDistSamp = DistSample( rnd, dist );
                    print "failed times: {0}".format( failTime );
                    failTime=0;
                    return newDistSamp;
                else:
                    failTime += 1;

        return None;
           

    def distSampleUsingObstSurfSamps( self, num, maxDimLens ):
        """@param num: failure time to sample a new configuration randomly"""

        self.randomSample( 800, len(maxDimLens), maxDimLens );
        searcher = ObstSurfSearcher(self.mCollisionMgr, self.mCSpace);
        searcher.searchObstSurfConfigs( self.mFreeSamples, self.mObstSamples, 3 );

        self.mDistSamples = [];
        boundaryQueue = [];
        bndSphDict = defaultdict();
        randFreeSamp = 1234;

        while( randFreeSamp != None ):
            randFreeSamp = self.getARandomFreeSample( num, maxDimLens, len(maxDimLens) );
            if( randFreeSamp == None ):
                return;
            self.mDistSamples.append( randFreeSamp );
            bounds = randFreeSamp.getBoundaryConfigs( maxDimLens );

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
                for sample in self.mDistSamples:
                    if sample.isInside( bnd, maxDimLens ): #####################################################################################================================ Locally Sensetive Hash
                        # check if within any spheres, not including the sphere that the boundary config belongs to.
                        newSamp = False;
                        break;

                if newSamp:
                    # get the nearest distance to obstacles
                    dist, neighbor = searcher.getNearest( bnd );              # Get the distance to obstacles
                    if (dist) >= 30.0:	    					 # if not too close to obstacles
                        newDistSamp = DistSample(bnd, dist)	# construct a new dist sample
                        print "{0}  R: {1}".format( bnd, dist );
                        self.mDistSamples.append( newDistSamp );				# add to our dist sample set
                        if( len(self.mDistSamples) >= 800 ):
                            return;
                        bounds = newDistSamp.getBoundaryConfigs(maxDimLens);		# get the boundary configs
                        for bndConfig in bounds:
                            #if not bndConfig in bndSphDict:				# put the boundconfig-sphere relation to the dictionary
                            bndSphDict[str(bndConfig)] = newDistSamp;
                            boundaryQueue.append( bndConfig );				# put the boundary config to the queue.
                        
                        ###########################=========================================================
                        if len(self.mDistSamples)%30 == 0:
                            print "------------ FRESH -------------"
                            for sphere in self.mDistSamples:
                                boundaryQueue = [x for x in boundaryQueue if( not sphere.isInside(x, maxDimLens)) ]
                        ###########################=========================================================

                        print "\t\t\t\t\t\t\t\t\t\t{0}\n".format(len(boundaryQueue));



    def distSampleOneThread( self, num, maxDimLens ):
        """@param num: failure time to sample a new configuration randomly"""

        self.mDistSamples = [];
        boundaryQueue = [];
        bndSphDict = defaultdict();

        randFreeSamp = 1234;
        while( randFreeSamp != None ):
            randFreeSamp = self.getARandomFreeSample( num, maxDimLens, len(maxDimLens) );
            if( randFreeSamp == None ):
                return;
            self.mDistSamples.append( randFreeSamp );
            bounds = randFreeSamp.getBoundaryConfigs( maxDimLens );

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
                for sample in self.mDistSamples:
                    if sample.isInside( bnd, maxDimLens ): #####################################################################################================================ Locally Sensetive Hash
                        # check if within any spheres, not including the sphere that the boundary config belongs to.
                        newSamp = False;
                        break;

                if newSamp:
                    # randomly shoot rays to get the nearest distance to obstacles
                    rayShooter = RayShooter( bnd, self.mCollisionMgr, self.mCSpace );	# Shot ray
                    dim = len(maxDimLens);
                    dist = rayShooter.randShoot(50*(dim-1));					# Get the distance to obstacles
                    if (dist) >= 40.0:	    					# if not too close to obstacles
                        newDistSamp = DistSample(bnd, dist)	# construct a new dist sample
                        print "{0}  R: {1}".format( bnd, dist );
                        self.mDistSamples.append( newDistSamp );				# add to our dist sample set
                        bounds = newDistSamp.getBoundaryConfigs(maxDimLens);		# get the boundary configs
                        if len(self.mDistSamples) == 100:
                            return;
                        for bndConfig in bounds:
                            #if not bndConfig in bndSphDict:				# put the boundconfig-sphere relation to the dictionary
                            bndSphDict[str(bndConfig)] = newDistSamp;
                            boundaryQueue.append( bndConfig );				# put the boundary config to the queue.
                        
                        ###########################=========================================================
                        if len(self.mDistSamples)%100 == 0:
                            print "------------ FRESH -------------"
                            for sphere in self.mDistSamples:
                                boundaryQueue = [x for x in boundaryQueue if( not sphere.isInside(x, maxDimLens)) ]
                        ###########################=========================================================

                        print "\t\t\t\t\t\t\t\t\t{0}\n".format(len(boundaryQueue));
                        

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
        for line in file2read:
            strDistSamp = line;
            info = strDistSamp.split( '\t' );
            dim = len(info);
            pos = [0] * (dim-1);
            for i in range(0,dim-1):
                pos[i] = float( info[i] );
            radius = float(info[dim-1]);
            distSamp = DistSample(tuple(pos), radius);
            if( distSamp.mRadius >= 2 ):
                self.mDistSamples += [ distSamp ];