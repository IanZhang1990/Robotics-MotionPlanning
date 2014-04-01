
import sys, os, datetime
import math
from collections import defaultdict
from time import sleep
import pygame

from SampleManager import DistSample
from PriorityQueue import PriorityQueue;



class AstarNode:
	def __init__(self, pos, parent, sphere = None):
		self.mPosition = pos;
		self.mParentNode = parent;
		self.mSphere = sphere;		# The sphere the sample is in
		self.mG = 0;
		self.mH = 0;
		self.mF = 0; 				# F = cost + heuristic

class AstarSearcher:
    def __init__( self, spheres, maxDimLens ):
        """Constructor of AstarSearcher. The constructor will iterate each given spheres,
        and record their overlapping relationship. 
        @param spheres: distance samples got by SampleManager. Those samples should have 
        covered the whole free space.
        @param maxDimLens: max length of each dimension
        """
        self.mSpheres = spheres;
        self.mOverlapDict = defaultdict( list );

        for sphere in self.mSpheres:
            for other in self.mSpheres:
                if( sphere == other ):
                    continue;
                deltas = [0] * len(sphere.mSample);
                for i in range(0, len(sphere.mSample)):
                    deltas[i] = math.fabs( sphere.mSample[i] - other.mSample[0] );
                    if( maxDimLens[i] - deltas[i] < deltas[i] ):
                        deltas[i] = maxDimLens[i] - deltas[i];
                
                dist = 0;
                for i in range(0, len(sphere.mSample)):
                    dist += deltas[i]**2;
                dist = math.sqrt(length);

                if( length <= (sphere.mRadius+other.mRadius) ):
                    # Overlap! Record it in the dictionary
                    self.mOverlapDict[sphere] += [ other ];

    def findOwnerSphere( self, point, maxDimLens ):
        """Given sample, find the sphere the sample is in."""
        minCenterDist = 1000000000;
        chosenSphere = None;
        dim = len(point);
        for sphere in self.mSpheres:
            if sphere.isInside( point, maxDimLens ):
                deltas = [0] * dim;
                dist = 0;
                for j in range( 0, dim ):
                    deltas[j] = math.fabs(point[j] - sphere.mSample[j])
                    if( maxDimLens[j] - deltas[j] < deltas[j]):
                        deltas[j] = maxDimLens[j] - deltas[j];
                    dist += deltas[j]**2;
                dist = math.sqrt( dist );
                if minCenterDist > dist:
                    minCenterDist = dist;
                    chosenSphere = sphere;
        return chosenSphere;
    
    def getSphereBoundaries( self, sphere, goal, maxDimLens ):
        """Given a sphere, return the points in the boundary of the sphere.
         These boundary points should lie in shared areas btw the sphere and its overlaping spheres.
         Data structure of each element in returned list: (point, sphere)
         """
        if sphere.isInside( goal, maxDimLens ):
            return [(goal, sphere)];

        points = sphere.getBoundaryConfigs( maxDimLens );

        neighborSpheres = self.mOverlapDict[sphere];

        legalPoints = [];
        for point in points:
            for neighborSphere in neighborSpheres:
                if neighborSphere is not sphere and neighborSphere.isInside( point, maxDimLens ):
                    legalPoints += [(point, neighborSphere)]
                    break;

        return legalPoints;

    def distance( self, one, two, maxDimLens ):
        """Given two points, return their distance in the cspace"""
        dlts = [0] * len(one);
        dist = 0;
        for i in range(0,dim):
            dlts[i] = math.fabs( one[i] - two[i] );
            if( maxDimLens[i] - dlts[i] < dlts[i] ):
                dlts[i] = maxDimLens[i] - dlts[i];
            dist += dlts[i]**2;
        return math.sqrt(dist);


    def astarSearch_Q( self, start, goal, cSpace, imgsurface=None ):
        def backtrace( node, pardict ):
            path = []
            path.append( node )
            while( pardict.has_key(str(node))):
                path.append( pardict[str(node)] );
                node = pardict[str(node)];
            path.reverse();
            return path;

        openList = PriorityQueue();
        closedList = PriorityQueue();

        parentDict = defaultdict();
        sphereDict = defaultdict();
        GDict = defaultdict();

        ownerShpere = self.findOwnerSphere( start[0],start[1], cSpace.mScaledWidth, cSpace.mScaledHeight);
        startNode = AstarNode( start[0], start[1], None, ownerShpere );
        start_mF =  self.distance( start, goal, cSpace.mScaledWidth, cSpace.mScaledHeight );
        openList.push( startNode.mPosition,  start_mF );
        sphereDict[str(startNode.mPosition)] = ownerShpere;
        GDict[str(startNode.mPosition)] = 0;

        while( not openList.isEmpty() ):
            current, curr_mF = openList.pop();
            if current == goal:
                return backtrace( current, parentDict );
            if( imgsurface is not None ):
                for event in pygame.event.get():
                    pass;
                pygame.draw.circle( imgsurface, (0,255,0), (int(current[0]), int(current[1])), 2 );
                pygame.display.update();

            #openList.remove_task( current );
            currOwnerSphere = sphereDict[str(current)];
            successors = self.getSphereBoundaries(currOwnerSphere, goal, cSpace.mScaledWidth, cSpace.mScaledHeight);
            closedList.push( current, curr_mF );

            for suc in successors:
                sucSamp = suc[0];
                if( closedList.find( sucSamp ) ):
                    continue;
                sucOwnerSphere = suc[1];
                sucNode = AstarNode( sucSamp[0], sucSamp[1], current, sucOwnerSphere )
                sphereDict[str(sucNode.mPosition)] = sucOwnerSphere;

                #if sucSamp == goal:
                #    parentDict[str(sucNode.mPosition)] = current;
                #    return backtrace( sucSamp, parentDict );
                sucNode.mG = GDict[str(current)] + self.distance( sucSamp, current, cSpace.mScaledWidth, cSpace.mScaledHeight );

                sameOpen = openList.find( sucNode.mPosition );
                if( sameOpen is None or GDict[str(sucNode.mPosition)] > sucNode.mG):
                    parentDict[str(sucNode.mPosition)] = sucNode.mParentNode;
                    GDict[str(sucNode.mPosition)] = sucNode.mG;
                    sucNode_mH = self.distance( sucSamp, goal, cSpace.mScaledWidth, cSpace.mScaledHeight );
                    sucNode_mF = sucNode.mG + sucNode_mH;
                    openList.push( sucNode.mPosition, sucNode_mF );
                pass
            pass
        return None;

    def savePath( self, path ):
        """Given a path in the scaled CSpace, save it to disk"""
        pathfile = open( "path.txt", 'w' );
        if path is not None:
            for i in range( 0, len(path) ):
                config = path[i];
                toWrite = ""
                for j in range( 0, len(config) ):
                    toWrite += str( config[i] ) + "\t";
                toWrite += "\n";
                pathfile.write( toWrite );


    def loadPath( self, pathfile ):
        """Given a path file in the disk,  read the path to memory"""
        pathfile = open( pathfile );
        path = []
        for line in pathfile:
            info = line.split('\t');
            dim = len(info);
            pos = [0] * (dim);
            for i in range(0,dim):
                pos[i] = float( info[i] );
            path.append( pos );
            pass;
        return path;



