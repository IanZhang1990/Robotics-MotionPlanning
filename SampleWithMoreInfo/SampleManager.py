
from random import randrange, uniform

import sys, os, datetime, thread
import math
from Obstacle import *
from Ray import *
from World import *
import pygame

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

g_failTimes = 0;

class SampleManager:
	def __init__( self, world ):
		self.mWorld = world;
		self.mObstMgr = world.mObstMgr;
		self.mDistSamples = [];
		self.mFreeSamples = [];
		self.mObstSamples = [];
		

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
		return freeSamp;

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
			print "Get {0} samples".format( len(self.mDistSamples) );

	def sampleWithDistInfo_multiThread(self, num):
		"""Randomly sample configurations in the c-space with multi-threading
		@param num: termination conditon. num times failed to find a new point, then terminate.
		"""
		global g_failTimes;
		try:
			for i in range(0,10):
				thread.start_new( self.__mltithreadSample__, ("Thread-"+str(i), num) )
			g_failTimes = 0;
		except Exception, msg:
			print "Failed to start a thread, MSG:\n\t" + msg;
			g_failTimes = 0;

	def __mltithreadSample__(self, threadname, num):
		print 'start thread '+ threadname + '\n';
		global g_failTimes;
		while( self.g_failTimes < num ):
			rnd1 = randrange(0,self.mWorld.mWidth);
			rnd2 = randrange(0,self.mWorld.mHeight);

			newSamp = True;
			for sample in self.mDistSamples:
				if sample.withInArea( rnd1, rnd2 ):
					newSamp = False;
					g_failTimes += 1
					break;

			if newSamp:
				# randomly shoot rays to get the nearest distance to obstacles
				rayShooter = RayShooter( rnd1, rnd2, self.mObstMgr );
				dist = rayShooter.randShoot(72);
				if math.fabs(dist) >= 1.0:
					self.mDistSamples += [ DistSample(rnd1, rnd2, dist) ];
					g_failTimes=0;


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

	def drawDistSampleToPic(self, ImgSurface):
		freeColor = ( 0, 250, 0 );
		obstColor = ( 200, 0, 0 );
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