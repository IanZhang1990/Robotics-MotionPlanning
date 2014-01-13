import pygame, sys, os
from pygame.locals import *
from random import randrange, uniform
import numpy
from SVMClassification import *
from scipy.spatial import Delaunay
import numpy as np

class Triangle:
	def __init__(self, x1, y1, x2, y2, x3, y3):
		self.points = [[x1, y1], [x2,y2], [x3,y3]];

	def render(self, surface, color):
		pygame.draw.line( surface, color, self.points[0], self.points[1], 1 );
		pygame.draw.line( surface, color, self.points[1], self.points[2], 1 );
		pygame.draw.line( surface, color, self.points[0], self.points[2], 1 );

class Triangulator:
	def __init__(self):
		self.triangles = []

	def triangulate(self, points):
		triangles = Delaunay(points)
		triIndces = triangles.vertices
		for tri in triIndces:
			x1 = points[tri[0]][0];
			y1 = points[tri[0]][1];
			x2 = points[tri[1]][0];
			y2 = points[tri[1]][1];
			x3 = points[tri[2]][0];
			y3 = points[tri[2]][1];
			newTri = Triangle(x1,y1,x2,y2,x3,y3);
			self.triangles = self.triangles + [newTri];