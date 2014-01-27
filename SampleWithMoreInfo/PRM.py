
import math
import copy
import Queue;
import pygame;
from Obstacle import *
from PriorityQueue import *
from collections import defaultdict


class Node:
	"""Node of a Tree Structure"""
	def __init__(self, val):
		self.mVal = val;
		self.mChildren = [];

	def addChild(self, node):
		self.mChildren += [node];

	def hasChildren(self):
		return len(self.mChildren) == 0;

	def getChildren(self):
		return (self.mChildren);

	def valDist(self, val):
		"""Computer the distance between 2 values, which is distance in 2D"""
		dx = val[0] - self.mVal[0];
		dy = val[1] - self.mVal[1];
		return math.sqrt( dx**2 + dy**2 );


class Graph:
	"""Graph Structure"""
	def __init__(self, rootNode):
		self.mRoot = rootNode;
		self.mVertices = [rootNode];
		self.mEdges = defaultdict(list);

	def addNode(self, vert):
		self.mVertices += [vert];

	def addEdge(self, vert1, vert2):
		self.mEdges[vert1] += [vert2];
		vert1.addChild( vert2 );

	def getRoot(self):
		return self.mRoot;

	def search( self, targetVal ):
		"""Search a node in the tree with the specific value"""
		raise Exception( "Not Implemented Yet" );

	def findNearVertices( self, vertice, dist ):
		"""Find nearest vertices"""
		neighbors = []
		dist = dist**2
		for vert in self.mVertices:
			deltaSqr = []
			for i in range( 0, len(vertice.mVal)):
				deltaSqr += [(vertice.mVal[i]-vert.mVal[i])**2];
			lenSqr = sum(deltaSqr);
			if lenSqr <= dist:
				neighbors += [vert];
		return neighbors;

	def findKNearVertices( self, vertice, k ):
		"""Find K nearest vertices"""
		neighbors = []
		fringe = PriorityQueue();

		for vert in self.mVertices:
			deltaSqr = 0;
			for i in range( 0, len(vertice.mVal)):
				deltaSqr += (vertice.mVal[i]-vert.mVal[i])**2;
			fringe.push( vert, math.sqrt(deltaSqr) );

		if fringe.isEmpty():
			return neighbors;

		for i in range(0,int(round(k))):
			try:
				neighbors += [fringe.pop()];
			except Exception:
				return neighbors;

		return neighbors;

	def searchNearest2d(self, val):
		"""search the node nearest to the given point in 2D space.
		@param val: the position of the sample in 2d space
		TODO: find an algorithm that runs faster. Currently, I'm using bread first search
		"""
		raise Exception('Please use findNearVertices(vertice, dist) instead. This method has a bug.' )
		currentNode = self.mRoot;
		minDist = 1000000000.0
		chosenNode = None;

		fringe = Queue.Queue();
		fringe.put(currentNode)

		while(fringe.empty()):
			currentNode = fringe.get();
			if currentNode.valDist( val ) < minDist:
				minDist =  currentNode.valDist( val );
				chosenNode = currentNode;
				pass
			if currentNode.hasChildren():
				for node in currentNode.getChildren():
					fringe.put(node);

	def searchNear( self, val, k ):
		"""Search the graph and return k nearest neighbors.
		@param val: sample position in 2D space
		@param k: number of nearest neighbors you want to return."""
		currentNode = self.mRoot;
		pq = PriorityQueue(); 
		fringe = Queue.Queue();
		fringe.put(currentNode)

		while(fringe.empty()):
			currentNode = fringe.get();
			pq.push(currentNode, currentNode.valDist( val ))

			if currentNode.hasChildren():
				for node in currentNode.getChildren():
					fringe.put(node);

		result = []
		for i in range( 0,k ):
			if( not pq.isEmpty() ):
				result += [pq.pop()];
			else:
				break;

		return result;

	def render(self, imgSurf, color):
		for key in self.mEdges.keys():
			if(len(key.mVal)>2):
				raise Exception( 'This method is for 2D only now' );
			adjectList = self.mEdges[key];
			if color == None:
				color = (0,250,0);
			for vert in adjectList:
				pygame.draw.line( imgSurf, color, key.mVal, vert.mVal, 1 );

class PRM:
	"""Probability roadmap in a 2D world"""
	def __init__(self, obstMgr, sampleMgr):
		self.mVertices = []
		self.mObstMgr = obstMgr;
		self.mSampleMgr = sampleMgr;
		self.mGraph = None;
		pass;

	def buildPRM_star(self, imgSurf=None):
		samples = self.mSampleMgr.sampleFree(800);
		firstVert = Node(samples[100]);
		self.mGraph = Graph( firstVert );

		for samp in samples:
			n = len(self.mGraph.mVertices);
			d = 2;
			#r_prm = math.pow(math.log(n)/n, 1.0/d) * math.sqrt( 1366**2+768**2 ) / 1.5;
			#OMPL implementation:
			k = 2 * math.e * math.log(n);
			vert = Node( samp );
			neighbors = self.mGraph.findKNearVertices( vert, k );
			self.mGraph.addNode( vert );
			for neighbor in neighbors:
				if self.mObstMgr.isPathFree( vert.mVal, neighbor.mVal ):
					self.mGraph.addEdge( vert, neighbor );
					#self.mGraph.addEdge( neighbor, vert );
					if imgSurf:
						pygame.draw.line( imgSurf, (0,250,0), vert.mVal, neighbor.mVal, 1 );
						pygame.display.update();
		pass;

	def renderRoadMap(self, imgSurf, color=None):
		self.mGraph.render( imgSurf, color );