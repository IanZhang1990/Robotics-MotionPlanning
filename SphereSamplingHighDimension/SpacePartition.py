import math
import sys, os

class Grid:
	def __init__(self, center, dimLens):
		"""@param center: center of the grid;
		@param dimLens: length in each dimension"""
		self.mCenter = center;
		self.mDimLens = dimLens;
		self.mContainer = [];

	def addSphere( self, sphere ):
		self.mContainer.append( sphere );

	def intersect( self, sphere, dim ):
		"""Determine if the grid intersect with a sphere"""
		dlts = [0]  * dim;
		dist = 0;
		for i in range(0, dim):
			dlts[i] = math.fabs(sphere.mSample[i] - self.mCenter[i]) - self.mDimLens[i];
			dist = dlts[i]**2;
		if( dist <= sphere.mRadius**2 ):
			return True;
		else:
			return False;

class SpacePartition:
	def __init__( self, maxDimLens, unitDimLens ):
		dim = len(maxDimLens);
		self.mMaxDimLens = maxDimLens;
		self.mUnitDimLens = unitDimLens;


	def getContainingGrid( self, point ):
		"""Given a point in n-D world, return the grid containing it."""

	def indxHash( self, point ):
		"""Given a point in n-D world, return the index containing the point"""
		dim = len( point );
		dimIdx = [0] * dim;
		for i in range(0, dim):
			dimIdx[i] = int(point[i]) / int( self.mUnitDimLens[i] );

		
