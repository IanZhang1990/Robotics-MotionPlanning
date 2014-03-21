
from random import randrange, uniform

import sys, os, datetime
import math
from Ray import *
from CSpaceWorld import *
import pygame
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
    def __init__(self, x, y, radius):
        self.mSample = (x,y)
        self.mRadius = radius;

    def getBoundaryConfigs(self, maxWidth, maxHeight, num=0):
        """ Get configs in the boundary of the sphere. For 2D only!!!!
         @param num: the number of boundary configs you need.
         When num = 0, automatically get boundary configs."""
        retSet = []
        if( num == 0 ):
            num = self.mRadius / 5 + 5;
            
        dlt_ang = (2*math.pi) / float(num); # increment of angle;
        dlt_dist = self.mRadius / 10;
        if dlt_dist > 1.0:
            dlt_dist = 1.0;
        for i in range(1, int(num)+1):
            ang = dlt_ang * i;
            newX = self.mSample[0]+(self.mRadius+dlt_dist)*math.cos( ang );
            if newX < 0:                                            # Warp the space
                newX = maxWidth + newX;
            else:
                newX = newX % maxWidth;                              # Warp the space
            newY = self.mSample[1]+(self.mRadius+dlt_dist)*math.sin( ang );
            if newY < 0:                                            # Warp the space
                newY = maxHeight + newY;
            else:
                newY = newY % maxHeight;                             # Warp the space

            retSet += [ (newX, newY) ]
        return retSet;
    
    def isInside(self, position, maxWidth, maxHeight):
        """Determine if a position is inside the sphere"""
        if len(position) > 2:
            raise Exception( "This method is for 2D only now." );
        dx = position[0] - self.mSample[0];
        dy = position[1] - self.mSample[1];
        distSqr = ( dx**2 + dy**2 );

        if distSqr < ( self.mRadius**2 ):
            return True;
        else:
            dx = maxWidth - math.fabs(position[0] - self.mSample[0]);               # These 4 lines wrap the space.
            dy = maxHeight - math.fabs(position[1] - self.mSample[1]);              #       It links the head of the space with the end of if
            distSqr = ( dx**2 + dy**2 );                                         #
            if( distSqr < self.mRadius**2 ):                                      #
                return True;
            return False;

class SampleManager:
    def __init__( self, CSpace ):
        self.mCSpace = CSpace;
        self.mCollisionMgr = CSpace.mCollisionMgr;
        self.mDistSamples = Manager().list();
        self.mFreeSamples = [];
        self.mObstSamples = [];
        self.g_failTimes = Value( 'i', 0 );
        
    def simpleSample(self, num):
        """randomly sample the world. save all samples"""
        samp = [];
        sampCount = 0;
        for i in range( 0, num ):
            irand_1 = randrange(0, self.mCSpace.mScaledWidth);
            irang_2 = randrange(0, self.mCSpace.mScaledHeight);
            alpha, phi = self.mCSpace.map2UnscaledSpace( irand_1, irand_2 );
            if not self.mCollisionMgr.ifCollide( (alpha, phi) ):
                self.mFreeSamples += [(irand_1, irang_2)];
            else:
                self.mObstSamples += [(irand_1, irang_2)];
        pass;
    
    def sampleFree(self, num):
        """Sample free space only, return num samples"""
        freeSamp = [];
        freeSampCount = 0;
        while( freeSampCount < num ):
            irand_1 = randrange(0, self.mCSpace.mScaledWidth);
            irang_2 = randrange(0, self.mCSpace.mScaledHeight);
            alpha, phi = self.mCSpace.map2UnscaledSpace( irand_1, irand_2 );
            if not self.mCollisionMgr.ifCollide( (alpha, phi) ):
                freeSamp += [(irand_1, irang_2)];
                freeSampCount += 1;
        self.mFreeSamples = freeSamp;
        print "Finished sampling free space, got {0} samples!".format( len(freeSamp) );
        return freeSamp;
    
    #def sampleNonVisArea( self, num ):
    #	"""After sampling many configurations with distance info. 
    #	There is still space not covered by those (hyper-)spheres.
    #	This method samples in the non-visiable area, and get num samples"""
    #	if len(self.mDistSamples) == 0:
    #		raise Exception( "Please sample (hyper)spheres in configuration space first." );

    #	samples = [];
    #	sampCount = 0;
    #	while( sampCount < num ):
    #		irand_1 = randrange(0, self.mCSpace.mScaledWidth);
    #		irang_2 = randrange(0, self.mCSpace.mScaledHeight);
    #		newSamp = ( irand_1, irang_2 );
    #		newSampValid = True;
    #		for distSamp in self.mDistSamples:
    #			if distSamp.isInside( (newSamp[0], newSamp[1]), self.mCSpace.mScaledWidth, self.mCSpace.mScaledHeight ):
    #				newSampValid = False;
    #				break;
    #		if newSampValid:
    #			samples += [newSamp];
    #			sampCount += 1;

    #	return samples;

    def getARandomFreeSample(self, num):
        """Randomly sample the space and return a free sample (with distance info).
         The sample is not inside of any other sphere. Also, this method will not automatically 
         add the new sample to self.mDistSamples list.
         @param num: fail time. If failed to find such a sample num times, return null"""
        failTime=0;
        while( failTime < num ):
            rnd1 = randrange(0,self.mCSpace.mScaledWidth);
            rnd2 = randrange(0,self.mCSpace.mScaledHeight);
            alpha, phi = self.mCSpace.map2UnscaledSpace( rnd1, rnd2 );
            if( self.mCollisionMgr.ifCollide( (alpha, phi) ) ):
                continue;

            newSamp = True;
            for sample in self.mDistSamples:
                if sample.isInside( (rnd1, rnd2), self.mCSpace.mScaledWidth, self.mCSpace.mScaledHeight ):
                    newSamp = False;
                    failTime += 1
                    break;
            if newSamp:
                # randomly shoot rays to get the nearest distance to obstacles
                rayShooter = RayShooter( rnd1, rnd2, self.mCollisionMgr, self.mCSpace );
                dist = rayShooter.randShoot(72);
                if math.fabs(dist) >= 1.0:
                    newDistSamp = DistSample(rnd1, rnd2, dist);
                    #(self.mDistSamples).append( newDistSamp );
                    print "failed times: {0}".format( failTime );
                    failTime=0;
                    return newDistSamp;
                else:
                    failTime += 1;

        return None;

    ###=======================================================================================
    ###=== Strategy 2: Randomly sample one sphere, then sample from the boundary
    ###===         Then keep sampling the new boundary of the set of spheres
    def distSampleOneThread( self, num, imgSurface=None ):
        self.mDistSamples = [];
        boundaryQueue = Queue();
        bndSphDict = defaultdict();

        randFreeSamp = 1234;
        while( randFreeSamp != None ):
            randFreeSamp = self.getARandomFreeSample( num );
            if( randFreeSamp == None ):
                return;
            self.mDistSamples.append( randFreeSamp );
            self.drawDistSample(imgSurface, (randFreeSamp.mSample[0],randFreeSamp.mSample[1]), randFreeSamp.mRadius);
            bounds = randFreeSamp.getBoundaryConfigs(self.mCSpace.mScaledWidth, self.mCSpace.mScaledHeight);

            for bndConfig in bounds:
                #if not bndConfig in bndSphDict:				# put the boundconfig-sphere relation to the dictionary
                bndSphDict[bndConfig] = randFreeSamp;
                boundaryQueue.put( bndConfig );				# put the boundary config to the queue.

            while( not boundaryQueue.empty() ):
                print "Size of dist samples {0}".format( len( self.mDistSamples ) );
     #           if( len(self.mDistSamples) % 100 == 0 ):
                    #randFreeSamp = self.getARandomFreeSample( num );
                    #if( randFreeSamp == None ):
                    #	return;
                    #(self.mDistSamples).append( randFreeSamp )
                    #bounds = randFreeSamp.getBoundaryConfigs(self.mCSpace.mScaledWidth, self.mCSpace.mScaledHeight);		# get the boundary configs
                    #for bndConfig in bounds:
                    #	#if not bndConfig in bndSphDict:				# put the boundconfig-sphere relation to the dictionary
                    #	bndSphDict[bndConfig] = newDistSamp;
                    #	boundaryQueue.put( bndConfig );				# put the boundary config to the queue.


                bnd = boundaryQueue.get();							# get a new boundary 
                newSamp = True;
                for sample in self.mDistSamples:
                    if sample.isInside( (bnd[0], bnd[1]), self.mCSpace.mScaledWidth, self.mCSpace.mScaledHeight ): #####################################################################################================================ Locally Sensetive Hash
                        # check if within any spheres, not including the sphere that the boundary config belongs to.
                        newSamp = False;
                        break;

                if newSamp:
                    # randomly shoot rays to get the nearest distance to obstacles
                    rayShooter = RayShooter( bnd[0], bnd[1], self.mCollisionMgr, self.mCSpace );	# Shot ray
                    dist = rayShooter.randShoot(72);					# Get the distance to obstacles
                    if math.fabs(dist) >= 1.0:							# if not too close to obstacles
                        newDistSamp = DistSample(bnd[0], bnd[1], dist)	# construct a new dist sample
                        self.mDistSamples.append( newDistSamp );				# add to our dist sample set
                        self.drawDistSample( imgSurface, (newDistSamp.mSample[0], newDistSamp.mSample[1]), newDistSamp.mRadius );
                        bounds = newDistSamp.getBoundaryConfigs(self.mCSpace.mScaledWidth, self.mCSpace.mScaledHeight);		# get the boundary configs
                        for bndConfig in bounds:
                            #if not bndConfig in bndSphDict:				# put the boundconfig-sphere relation to the dictionary
                            bndSphDict[bndConfig] = newDistSamp;
                            boundaryQueue.put( bndConfig );				# put the boundary config to the queue.

    def renderAllDistSamples(self, ImgSurface):
        """Render distance sample to image"""
        print "render {0} dist samples to the image".format( len(self.mDistSamples) );
        freeColor = ( 0, 0, 250 );
        obstColor = ( 200, 0, 100 );
        for samp in self.mDistSamples:
            if samp.mRadius > 0: # Free sample
                self.drawDistSample( ImgSurface, (int(samp.mSample[0]), int(samp.mSample[1])), int(math.fabs(samp.mRadius)), freeColor );
                #pygame.draw.circle( ImgSurface, freeColor, (int(samp.mSample[0]), int(samp.mSample[1])), int(math.fabs(samp.mRadius)), 1 );
            else:
                self.drawDistSample( ImgSurface, (int(samp.mSample[0]), int(samp.mSample[1])), int(math.fabs(samp.mRadius)), obstColor );
                #pygame.draw.circle( ImgSurface, obstColor, (int(samp.mSample[0]), int(samp.mSample[1])), int(math.fabs(samp.mRadius)), 1 );

    def drawDistSample(self, imgsurf, origin, radius, color=(0,0,250)):
        if(imgsurf is not None and radius <= 1000000000 and radius > 0):
                pygame.draw.circle( imgsurf, color,(int(origin[0]),int(origin[1])), int(radius), 1 );
                if( origin[0]-radius<0 ):
                    pygame.draw.circle( imgsurf, color,(int(origin[0])+900,int(origin[1])), int(radius), 1 );
                if( origin[1]-radius<0 ):
                    pygame.draw.circle( imgsurf, color,(int(origin[0]),int(origin[1])+900), int(radius), 1 );
                if( origin[0]+radius>900 ):
                    pygame.draw.circle( imgsurf, color,(int(origin[0])-900,int(origin[1])), int(radius), 1 );
                if( origin[1]+radius>900 ):
                    pygame.draw.circle( imgsurf, color,(int(origin[0]),int(origin[1])-900), int(radius), 1 );
                pygame.display.update();

    def writeSamplesToFile( self, filename ):
        file2write = open( filename, 'w' );
        formattedData = ""
        for vector in self.mDistSamples:
            formattedData += "{0}\t{1}\t{2}\n".format( vector.mSample[0], vector.mSample[1], vector.mRadius )
            pass
        
        file2write.write( formattedData );
        file2write.close();

    def loadDistSamplesFromFile( self, filename ):
        file2read = open( filename, 'r' );
        self.mDistSamples = [];
        for line in file2read:
            strDistSamp = line;
            info = strDistSamp.split( '\t' );
            distSamp = DistSample( float(info[0]), float(info[1]), float(info[2]));
            if( distSamp.mRadius > 2 ):
                self.mDistSamples += [ distSamp ];