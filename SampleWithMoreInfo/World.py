
import sys, os
import math
from Obstacle import *
import pygame;

class World:

	g_obcColor = [ 150, 150, 150 ]
	g_obcThickness = 0;
	g_spaceColor = [ 0, 150, 0 ]
	g_spaceThickness = 3;

	def __init__( self, width, height ):
		self.mWidth = width;
		self.mHeight = height;
		self.mSpaces = [ Rect( 1, 1, width-1, height-1 ) ];
		self.mObstMgr = ObstaclesManager( width, height );

	def buildWorld(self):
		self.mObstMgr.generateObstacles( 20, 5, 5, self.mWidth, 5, self.mHeight );

	def loadWorld(self, filename):
		"""load the world from a file"""
		worldFile = open(filename, 'r');

		for line in worldFile:
			info = line.split(' ');
			if(info[0]=="WIDTH"):
				self.mWidth = int(info[1]);
			elif info[0] == "HEIGHT":
				self.mHeight = int(info[1]);
			elif info[0] == "SPACE":
				if info[1] == "rect":
					self.mSpaces += [Rect( int(info[2]), int(info[3]),int(info[4]),int(info[5]) )];
				elif info[1] == "circle":
					self.mSpaces += [Rect( int(info[2]), int(info[3]),int(info[4]) )];
			elif info[0] == "OBSTACLE":
				if info[1] == "rect":
					self.mObstMgr.addObstacle( Rect( int(info[2]), int(info[3]),int(info[4]),int(info[5]) ));
					pass
				elif info[1] == "circle":
					self.mObstMgr.addObstacle( Circle( int(info[2]), int(info[3]),int(info[4]) ));
					pass
		pass

	def saveWorld(self, filename):
		"""Save the world in to a file"""
		worldFile = open( filename, 'w' );
		worldFile.write( "WIDTH {0}\nHEIGHT {1}\n".format( self.mWidth, self.mHeight ) );

		for space in self.mSpaces:
			if isinstance(space, Circle):
				worldFile.write( "SPACE circle {0} {1} {2}\n".format( space.X, space.Y, space.Radius ) );
			elif isinstance(space, Rect):
				worldFile.write( "SPACE rect {0} {1} {2} {3}\n".format( space.X,space.Y,space.Width,space.Height ) );

		for obst in self.mObstMgr.mObstacles:
			if isinstance(obst,Circle):
				worldFile.write( "OBSTACLE circle {0} {1} {2}\n".format( obst.X, obst.Y, obst.Radius ) );
			elif isinstance(obst,Rect):
				worldFile.write( "OBSTACLE rect {0} {1} {2} {3}\n".format( obst.X,obst.Y,obst.Width,obst.Height ) );
		worldFile.close();
		pass;

	def drawSpacesToPic( self, ImgSurface ):
		for space in self.mSpaces:
			space.render( ImgSurface, World.g_spaceColor, World.g_spaceThickness );

	def drawObstaclesToPic(self, ImgSurface):
		for obc in self.mObstMgr.mObstacles:
			obc.render( ImgSurface, World.g_obcColor, World.g_obcThickness );
