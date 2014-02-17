
import sys, os, datetime
import math
from collections import defaultdict

from SampleManager import DistSample
from PriorityQueue import PriorityQueue;

class AstarNode:
	def __init__(self, x, y, parent, sphere = None):
		self.mPosition = (x,y);
		self.mParentNode = parent;
		self.mSphere = sphere;		# The sphere the sample is in
		self.mG = 0;
		self.mH = 0;
		self.mF = 0; 				# F = cost + heuristic

class AstarSearcher:
	def __init__( self, spheres ):
		"""Constructor of AstarSearcher. The constructor will iterate each given spheres,
		and record their overlapping relationship. 
		@param spheres: distance samples got by SampleManager. Those samples should have 
		covered the whole free space.
		"""
		self.mSpheres = spheres;
		self.mOverlapDict = defaultdict( list );

		for sphere in self.mSpheres:
			for other in self.mSpheres:
				if( sphere == other ):
					continue;
				
				dx = sphere.mSample[0] - other.mSample[0];
				dy = sphere.mSample[1] - other.mSample[1];
				if( math.sqrt( dx**2+dy**2 ) <= (sphere.mRadius+other.mRadius) ):
					# Overlap! Record it in the dictionary
					self.mOverlapDict[sphere] += [ other ];

	def findOwnerSphere( self, x, y ):
		"""Given sample with (x,y) coordinate, find the sphere the sample is in."""
		minCenterDist = 1000000000;
		chosenSphere = None;
		for sphere in self.mSpheres:
			if sphere.withInArea( x, y ):
				dx = x - sphere.mSample[0];
				dy = y - sphere.mSample[1];
				dist = math.sqrt( dx**2+dy**2 );
				if minCenterDist >= dist:
					minCenterDist = dist;
					chosenSphere = sphere;
		return chosenSphere;

	def getSphereBoundaries( self, sphere, goal ):
		"""Given a sphere, return the points in the boundary of the sphere.
		These boundary points should lie in shared areas btw the sphere and its overlaping spheres.
		Data structure of each element in returned list: (point, sphere)
		"""
		if sphere.withInArea( goal[0],goal[1] ):
			return [(goal, sphere)];

		delta = 2.0;
		alpha = 2.0 * math.asin( delta / float(sphere.mRadius) );
		num = 2.0 * 3.14159265354 / alpha;
		points = [];
		for i in range( 0, int(num)+1 ):
			angle = alpha * i;
			radius = sphere.mRadius + 1;
			points += [ ( radius * math.cos(angle) + sphere.mSample[0], radius * math.sin(angle) + sphere.mSample[1] ) ];

		neighborSpheres = self.mOverlapDict[sphere];

		illegalPoints = [];
		for point in points:
			for neighborSphere in neighborSpheres:
				if neighborSphere.withInArea( point[0], point[1] ):
					illegalPoints += [(point, neighborSphere)]

		return illegalPoints;

	def distance( self, one, two ):
		dx = one[0] - two[0];
		dy = one[1] - two[1];
		return math.sqrt(dx**2+dy**2);

	def astarSearch( self, start, goal ):
		"""Given a start and goal point, search for an optimal path connecting them"""


		def backtrace( node ):
			path = []
			path.append( node.mPosition )
			while( node.mParentNode is not None ):
				path.append( node.mParentNode.mPosition );
				node = node.mParentNode;
			path.reverse();
			return path;

		openList = set();
		closedList = set();

		ownerShpere = self.findOwnerSphere( start[0],start[1] );
		startNode = AstarNode( start[0], start[1], None, ownerShpere );
		openList.add( startNode );

		while len(openList) is not 0:
			current = min(openList, key=lambda inst:inst.mF);
			owenerSphere = current.mSphere;
			successors = self.getSphereBoundaries(ownerShpere, goal);
			print current.mPosition;
			for suc in successors:
				sucSamp = suc[0];
				sucOwnerSphere = suc[1];
				sucNode = AstarNode( sucSamp[0], sucSamp[1], current, sucOwnerSphere )
				if sucSamp == goal:
					return backtrace( sucNode );
				sucNode.mG = current.mG + self.distance( sucSamp, current.mPosition );
				sucNode.mH = self.distance( sucSamp, goal );
				sucNode.mF = sucNode.mG + sucNode.mH;
				print "sample: {0} has heuristic {1}".format(sucSamp, sucNode.mF);

				samePos = filter( lambda inst: inst.mPosition[0]==sucSamp[0] and inst.mPosition[1]==sucSamp[1], openList)

				if len(samePos) is not 0 and samePos[0].mF <= sucNode.mF:
					continue;

				samePos = filter( lambda inst: inst.mPosition[0]==sucSamp[0] and inst.mPosition[1]==sucSamp[1], closedList)				
				if len(samePos) is not 0 and samePos[0].mF <= sucNode.mF:
					continue;
				openList.add( sucNode );
				pass
			closedList.add( current );
			pass
		return None;





