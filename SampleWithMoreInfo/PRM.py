
import math
import copy
import Queue;
from Obstacle import *
from PriorityQueue import *


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

	def getRoot(self):
		return self.mRoot;

	def search( self, targetVal ):
		"""Search a node in the tree with the specific value"""
		return None;

	def searchNearest2d(self, val):
		"""search the node nearest to the given point in 2D space.
		@param val: the position of the sample in 2d space
		TODO: find an algorithm that runs faster. Currently, I'm using bread first search
		"""
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
			if( !pq.isEmpty() ):
				result += [pq.pop()];
			else:
				break;

		return result;



class PRM:
	"""Probability roadmap in a 2D world"""
	def __init__(self):
		pass;

	def buildPRM(self, Xinit, obstMgr):
