
import sys, os, math
from SampleManager import *
from PRM import *

class GraphSpanner:
	
	def __init__(self, graph, distSamples):
		self.mGraph = graph;
		self.mDistSamples = distSamples;
		self.mDict = {};

	def span(self):
		print "\tBefore:\n\t\tVertices: {0}\tEndges:\t{1}".format( len(self.mGraph.mVertices), len(self.mGraph.mEdges) );
		for vert in self.mGraph.mVertices:
			for i in range(0, len(self.mDistSamples)):
				distSamp = self.mDistSamples[i];
				if distSamp.withInArea( vert.mVal[0], vert.mVal[1] ):
					# Check if there is already a vert in the sphere
					if i in self.mDict:
						# remove edges connected to the vertice
						del self.mGraph.mEdges[vert];
						# remove all edges that contains current vertice
						for key in self.mGraph.mEdges.keys():
							if vert in self.mGraph.mEdges[key]:
								self.mGraph.mEdges[key].remove(vert);
						# remove this vertice in the graph
						self.mGraph.mVertices.remove( vert );
					else:
						# add the sphere and the vertice to the dictionary
						self.mDict[i] = vert;
					break;


		print "\tAfter:\n\t\tVertices: {0}\tEndges:\t{1}".format( len(self.mGraph.mVertices), len(self.mGraph.mEdges) );
		return self.mGraph;

