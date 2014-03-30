
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
        for sphere in self.mSpheres:
            if sphere.isInside( point, maxWidth, maxHeight ):
                dx = math.fabs(x - sphere.mSample[0]);
                dy = math.fabs(y - sphere.mSample[1]);
                if( maxWidth - dx < dx):
                    dx = maxWidth - dx;
                if( maxHeight - dy < dy ):
                    dy = maxHeight - dy;
                dist = math.sqrt( dx**2+dy**2 );
                if minCenterDist >= dist:
                    minCenterDist = dist;
                    chosenSphere = sphere;
        return chosenSphere;
    
    def getSphereBoundaries( self, sphere, goal, maxWidth, maxHeight ):
        """Given a sphere, return the points in the boundary of the sphere.
         These boundary points should lie in shared areas btw the sphere and its overlaping spheres.
         Data structure of each element in returned list: (point, sphere)
         """
        if sphere.isInside( (goal[0],goal[1]), maxWidth, maxHeight ):
            return [(goal, sphere)];

        delta = 2.0;
        alpha = 2.0 * math.asin( delta / float(sphere.mRadius) );
        num = 2.0 * 3.14159265354 / alpha;
        points = [];
        for i in range( 0, int(num)+1 ):
            angle = alpha * i;
            radius = sphere.mRadius + 1;
            x_coord = radius * math.cos(angle) + sphere.mSample[0];
            if( x_coord < 0 ):
                x_coord = maxWidth + x_coord;
            elif( x_coord > maxWidth ):
                x_coord = x_coord % maxWidth;
            y_coord = radius * math.sin(angle) + sphere.mSample[1];
            if( y_coord < 0 ):
                y_coord = maxHeight + y_coord;
            elif( y_coord > maxHeight ):
                y_coord = y_coord % maxHeight;
            points += [ ( x_coord, y_coord ) ];

        neighborSpheres = self.mOverlapDict[sphere];

        legalPoints = [];
        for point in points:
            for neighborSphere in neighborSpheres:
                if neighborSphere is not sphere and neighborSphere.isInside( (point[0], point[1]), maxWidth, maxHeight ):
                    legalPoints += [(point, neighborSphere)]
                    break;

        return legalPoints;

    def distance( self, one, two, maxWidth, maxHeight ):
        """Given two points, return their distance in the cspace"""
        dx = math.fabs(one[0] - two[0]);
        if( maxWidth - dx < dx):
            dx = maxWidth - dx;
        dy = math.fabs(one[1] - two[1]);
        if( maxHeight - dy < dy ):
            dy = maxHeight - dy;
        return math.sqrt(dx**2+dy**2);


    def listContains( self, alist, astartNode ):
        pos = astartNode.mPosition;
        for element in alist:
            if math.fabs(element.mPosition[0] - pos[0]) < 1 and math.fabs(element.mPosition[1]-pos[1]) < 1:
                return element;

        return None;

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

    def astarSearch( self, start, goal, cSpace, imgsurface=None ):
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

        ownerShpere = self.findOwnerSphere( start[0],start[1], cSpace.mScaledWidth, cSpace.mScaledHeight);
        startNode = AstarNode( start[0], start[1], None, ownerShpere );
        openList.add( startNode );

        while len(openList) is not 0:
            current = min(openList, key=lambda inst:inst.mF);
            #if current.mPosition == goal:
            #    return backtrace( sucNode );
            #print "{0} \t {1}".format(len(openList), current.mF);
            if( imgsurface is not None ):
                for event in pygame.event.get():
                    pass;
                pygame.draw.circle( imgsurface, (0,255,0), (int(current.mPosition[0]), int(current.mPosition[1])), 2 );
                pygame.display.update();

            openList.remove( current );
            currOwnerSphere = current.mSphere;
            successors = self.getSphereBoundaries(currOwnerSphere, goal, cSpace.mScaledWidth, cSpace.mScaledHeight);
            #print "current: {0} \towener Sphere: {1}".format(current.mPosition, currOwnerSphere.mSample);
            #print current.mPosition;
            for suc in successors:
                sucSamp = suc[0];
                #if( imgsurface is not None ):
                #    pygame.draw.circle( imgsurface, (255,0,0), (int(sucSamp[0]), int(sucSamp[1])), 2, 1 );
                #    pygame.display.update();
                    #sleep(0.01);

                sucOwnerSphere = suc[1];
                sucNode = AstarNode( sucSamp[0], sucSamp[1], current, sucOwnerSphere )
                if sucSamp == goal:
                    return backtrace( sucNode );
                sucNode.mG = current.mG + self.distance( sucSamp, current.mPosition, cSpace.mScaledWidth, cSpace.mScaledHeight );
                sucNode.mH = self.distance( sucSamp, goal, cSpace.mScaledWidth, cSpace.mScaledHeight );
                sucNode.mF = sucNode.mG + sucNode.mH;
                #print "sample: {0} has heuristic {1}, \towener Sphere: {2}".format(sucSamp, sucNode.mF, sucOwnerSphere.mSample);
                
                #---------------------------------------------------------------------------------------------------------------------------------
                #samePos = filter( lambda inst: inst.mPosition[0]==sucSamp[0] and inst.mPosition[1]==sucSamp[1], openList)

                #if len(samePos) is not 0 and samePos[0].mF <= sucNode.mF:
                #    continue;
                #else:
                #    for node in samePos:
                #        node.mF = sucNode.mF;
                #        node.mParentNode = sucNode.mParentNode;

                #samePos = filter( lambda inst: inst.mPosition[0]==sucSamp[0] and inst.mPosition[1]==sucSamp[1], closedList)
                #if len(samePos) is not 0 and samePos[0].mF <= sucNode.mF:
                #    continue;
                #else:
                #    for node in samePos:
                #        node.mF = sucNode.mF;
                #        node.mParentNode = sucNode.mParentNode;
                #---------------------------------------------------------------------------------------------------------------------------------

                existingNode = self.listContains( openList, sucNode )
                if existingNode is not None:
                    if existingNode.mF > sucNode.mF:
                        existingNode.mF = sucNode.mF;
                        existingNode.mParentNode = sucNode.mParentNode;
                        existingNode.mG = sucNode.mG;
                        existingNode.mH = sucNode.mH;
                else:
                    openList.add( sucNode );
                pass
            closedList.add( current );
            pass
        return None;


    def savePath( self, path ):
        """Given a path in the scaled CSpace, save it to disk"""
        pathfile = open( "path.txt", 'w' );
        if path is not None:
            for i in range( 0, len(path) ):
                config = path[i];
                pathfile.write( "{0}\t{1}\n".format(config[0], config[1]) );


    def loadPath( self, pathfile ):
        """Given a path file in the disk,  read the path to memory"""
        pathfile = open( pathfile );
        path = []
        for line in pathfile:
            info = line.split('\t');
            path.append( (float(info[0]), float(info[1])) );
            pass;
        return path;



