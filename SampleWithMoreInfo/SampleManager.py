
from random import randrange, uniform

import sys, os, datetime
import math
from Obstacle import *
from Ray import *
from World import *
import pygame

from multiprocessing  import Process, Manager, Value, Array
import signal

def signal_handler(signum, frame):
	raise Exception( "Timed Out!!!" );

class DistSample:
	"""Sample with distance to obstacles"""
	def __init__(self, x, y, radius):
		self.mSample = (x,y)
		self.mRadius = radius;

	def withInArea(self, x, y):
		dx = x - self.mSample[0];
		dy = y - self.mSample[1];
		dist = math.sqrt( dx**2 + dy**2 );

		if dist < math.fabs( self.mRadius ):
			return True;
		else:
			return False;		

	#def collideWithPath(self, x1, y1, x2, y2):
    #    pass;

class SampleManager:
	def __init__( self, world ):
		self.mWorld = world;
		self.mObstMgr = world.mObstMgr;
		self.mDistSamples = Manager().list();
		self.mFreeSamples = [];
		self.mObstSamples = [];
		self.g_failTimes = Value( 'i', 0 );
		

	def simpleSample(self, num):
		"""randomly sample the world. save all samples"""
		samp = [];
		sampCount = 0;
		for i in range( 0, num ):
			irand_1 = randrange(0, self.mWorld.mWidth);
			irang_2 = randrange(0, self.mWorld.mHeight);
			if not self.mObstMgr.isConfigInObstacle( (irand_1, irang_2) ):
				self.mFreeSamples += [(irand_1, irang_2)];
			else:
				self.mObstSamples += [(irand_1, irang_2)];
		pass;

	def sampleFree(self, num):
		"""Sample free space only, return num samples"""
		freeSamp = [];
		freeSampCount = 0;
		while( freeSampCount < num ):
			irand_1 = randrange(0, self.mWorld.mWidth);
			irang_2 = randrange(0, self.mWorld.mHeight);
			if not self.mObstMgr.isConfigInObstacle( (irand_1, irang_2) ):
				freeSamp += [(irand_1, irang_2)];
				freeSampCount += 1;
		self.mFreeSamples = freeSamp;
		print "Finished sampling free space, got {0} samples!".format( len(freeSamp) );
		return freeSamp;

	def sampleNonVisArea( self, num ):
		"""After sampling many configurations with distance info. 
		There is still space not covered by those (hyper-)spheres.
		This method samples in the non-visiable area, and get num samples"""
		if len(self.mDistSamples) == 0:
			raise Exception( "Please sample (hyper)spheres in configuration space first." );
		
		samples = [];
		sampCount = 0;
		while( sampCount < num ):
			irand_1 = randrange(0, self.mWorld.mWidth);
			irang_2 = randrange(0, self.mWorld.mHeight);
			newSamp = ( irand_1, irang_2 );
			newSampValid = True;
			for distSamp in self.mDistSamples:
				if distSamp.withInArea( newSamp[0], newSamp[1] ):
					newSampValid = False;
					break;
			if newSampValid:
				samples += [newSamp];
				sampCount += 1;

		return samples;


	def sampleObst(self, num):
		"""Sample obstacle space only, return num samples"""
		obstSamp = [];
		obstSampCount = 0;
		while( obstSampCount < num ):
			irand_1 = randrange(0, self.mWorld.mWidth);
			irang_2 = randrange(0, self.mWorld.mHeight);
			if self.mObstMgr.isConfigInObstacle( (irand_1, irang_2) ):
				obstSamp += [(irand_1, irang_2)];
				obstSampCount += 1;

		self.mObstSamples = obstSamp;
		return obstSamp;

	def timeSafeSampleWithDistance( self, num, timeout ):
		"""Randomly sample configurations in the c-space
		@param num: termination conditon. num times failed to find a new point, then terminate.
		@param timeout: maximun sampling time
		"""
		signal.signal( signal.SIGALRM, signal_handler );
		signal.alarm( timeout );
		try:
			self.sampleWithMoreInfo( num );
		except Exception, msg:
			print msg;
			print "Get {0} samples with distances\n".format( len(self.mDistSamples) );

	def sampleWithDistInfo_multiThread(self, num):
		"""Randomly sample configurations in the c-space with multi-threading
		@param num: termination conditon. num times failed to find a new point, then terminate.
		"""
		try:
			self.g_failTimes.value = 0;
			threads = [];
			threadsCount = 4;
			for i in range(0,threadsCount):
				newThread = Process( target=self.__mltithreadDistSample__, args=[ i,num ] );
				threads += [newThread];
			for i in range( 0,threadsCount ):
				threads[i].start();
			for i in range( 0,threadsCount ):
				threads[i].join();

			print "Get {0} samples".format( len(self.mDistSamples) );

		except Exception, msg:
			print "Failed to start a thread, MSG:\n\t" + msg;
			self.g_failTimes.value = 0;

	def __mltithreadDistSample__(self, threadname, num):
		while( self.g_failTimes.value < num ):
			#print "Thread:\t{0} failedTimes:\t{1}\n".format( threadname, self.g_failTimes );
			rnd1 = randrange(0,self.mWorld.mWidth);
			rnd2 = randrange(0,self.mWorld.mHeight);

			newSamp = True;
			for sample in self.mDistSamples:
				if sample.withInArea( rnd1, rnd2 ):
					newSamp = False;
					self.g_failTimes.value += 1
					break;

			if newSamp:
				# randomly shoot rays to get the nearest distance to obstacles
				rayShooter = RayShooter( rnd1, rnd2, self.mObstMgr );
				dist = rayShooter.randShoot(72);
				if math.fabs(dist) >= 1.0:
					newDistSamp = DistSample(rnd1, rnd2, dist)
					for samp in self.mDistSamples:
						# Check if old sample is with the area of the new sample;
						if newDistSamp.withInArea( samp.mSample[0], samp.mSample[1] ):
							try:
								self.mDistSamples.remove( samp );
							except:
								continue;
					(self.mDistSamples) += [ newDistSamp ];
					self.g_failTimes.value=0;

		#print "Get {0} samples in thread {1}".format( len(self.mDistSamples), threadname );


	def sampleWithMoreInfo(self, num):
		"""Randomly sample configurations in the c-space
		@param num: termination conditon. num times failed to find a new point, then terminate.
		"""
		failTimes = 0;
		self.mDistSamples = []
		while( failTimes < num ):
			rnd1 = randrange(0,self.mWorld.mWidth);
			rnd2 = randrange(0,self.mWorld.mHeight);

			newSamp = True;
			for sample in self.mDistSamples:
				if sample.withInArea( rnd1, rnd2 ):
					newSamp = False;
					failTimes += 1
					break;

			if newSamp:
				# randomly shoot rays to get the nearest distance to obstacles
				rayShooter = RayShooter( rnd1, rnd2, self.mObstMgr );
				dist = rayShooter.randShoot(72);
				if math.fabs(dist) >= 1.0:
					self.mDistSamples += [ DistSample(rnd1, rnd2, dist) ];
					failTimes=0;

		print "Get {0} samples".format( len(self.mDistSamples) );


	def renderDistSample(self, ImgSurface):
		"""Render distance sample to image"""
		freeColor = ( 0, 0, 250 );
		obstColor = ( 200, 0, 100 );
		for samp in self.mDistSamples:
			if samp.mRadius > 0: # Free sample
				pygame.draw.circle( ImgSurface, freeColor, (samp.mSample[0], samp.mSample[1]), int(math.fabs(samp.mRadius)), 1 );
			else:
				pygame.draw.circle( ImgSurface, obstColor, (samp.mSample[0], samp.mSample[1]), int(math.fabs(samp.mRadius)), 1 );

	def writeSamplesToFile( self, filename ):
		file2write = open( filename, 'w' );
		formattedData = ""
		for vector in self.mDistSamples:
			formattedData += "{0}\t{1}\t{2}\n".format( vector.mSample[0], vector.mSample[1], vector.mRadius )
			pass

		file2write.write( formattedData );
		file2write.close();