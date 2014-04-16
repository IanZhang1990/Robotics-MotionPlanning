
import sys, os, datetime
import math
from collections import defaultdict
from time import sleep
#import pygame

from SampleManager import DistSample
from PriorityQueue import PriorityQueue;



class AstarNode:
    def __init__(self, pos, parent, move, time, sphere = None):
        self.mPosition = tuple(pos);
        self.mParentNode = parent;
        self.mSphere = sphere;		# The sphere the sample is in
        self.mG = 0;
        self.mH = 0;
        self.mF = 0; 				# F = cost + heuristic
        self.mMove = "None";
        self.mTime = 0;

class AstarSearcher:
    def __init__( self, spheres, maxDimLens, spacePartition ):
        """Constructor of AstarSearcher. The constructor will iterate each given spheres,
        and record their overlapping relationship. 
        @param spheres: distance samples got by SampleManager. Those samples should have 
        covered the whole free space.
        @param maxDimLens: max length of each dimension
        """
        self.mSpheres = spheres;
        self.mSpacePartition = spacePartition;

    def findOwnerSphere( self, point, maxDimLens ):
        """Given sample, find the sphere the sample is in."""
        radius = 0;
        chosenSphere = None;
        dim = len(point);
        grid = self.mSpacePartition.getContainingGrid( point );
        for sphere in grid.mContainer:
            if sphere.isInside( point, maxDimLens ) and sphere.mRadius > radius :
                chosenSphere = sphere;
                radius = sphere.mRadius;

        return chosenSphere;
    
    def getSphereBoundaries( self, sphere, enterNode, goal, maxDimLens ):
        """Given a sphere, and the point where car enters, return the points in the boundary
         of the sphere. These boundary points should lie in shared areas btw the sphere and its
         overlaping spheres. Data structure of each element in returned list: (point, sphere)
         """
        if sphere.isInside( goal, maxDimLens ):
            return [(goal, sphere)];

    def distance( self, one, two, maxDimLens ):
        """Given two points, return their distance in the cspace"""
        dlts = [0] * len(one);
        dist = 0;
        for i in range(0,len(maxDimLens)):
            dlts[i] = math.fabs( one[i] - two[i] );
            if( i == 2 and maxDimLens[i] - dlts[i] < dlts[i] ):
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

        ownerShpere = self.findOwnerSphere( start, cSpace.mMaxDimLens);
        startNode = AstarNode( start, None, ownerShpere );
        start_mF =  self.distance( start, goal, cSpace.mMaxDimLens );
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
            currOwnerSphere = sphereDict[str(tuple(current))];
            successors = self.getSphereBoundaries(currOwnerSphere, goal, cSpace.mMaxDimLens);
            closedList.push( current, curr_mF );
            if successors is None:
                continue;

            for suc in successors:
                sucSamp = suc[0];
                if( closedList.find( sucSamp ) ):
                    continue;
                sucOwnerSphere = suc[1];
                sucNode = AstarNode( sucSamp, current, sucOwnerSphere )
                sphereDict[str(sucNode.mPosition)] = sucOwnerSphere;

                #if sucSamp == goal:
                #    parentDict[str(sucNode.mPosition)] = current;
                #    return backtrace( sucSamp, parentDict );
                sucNode.mG = GDict[str(current)] + self.distance( sucSamp, current, cSpace.mMaxDimLens );

                sameOpen = openList.find( sucNode.mPosition );
                if( sameOpen is None or GDict[str(sucNode.mPosition)] > sucNode.mG):
                    parentDict[str(sucNode.mPosition)] = sucNode.mParentNode;
                    GDict[str(sucNode.mPosition)] = sucNode.mG;
                    sucNode_mH = self.distance( sucSamp, goal, cSpace.mMaxDimLens );
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
                    toWrite += str( config[j] ) + "\t";
                toWrite += "\n";
                pathfile.write( toWrite );


    def loadPath( self, pathfile ):
        """Given a path file in the disk,  read the path to memory"""
        pathfile = open( pathfile );
        path = []
        for line in pathfile:
            info = line.split('\t');
            dim = len(info);
            pos = [0] * (dim-1);
            for i in range(0,dim-1):
                pos[i] = float( info[i] );
            path.append( pos );
            pass;
        return path;



