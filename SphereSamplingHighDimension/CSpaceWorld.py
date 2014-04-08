
import sys, os
import math
import random
import copy
from CollisionManager import *
#import pygame;

class CSpaceWorld:
    g_obcColor = [ 150, 150, 150 ]
    g_obcThickness = 0;
    g_spaceColor = [ 0, 150, 0 ]
    g_spaceThickness = 3;

    def __init__( self, robot, dimensionLengths ):
        self.mRobot = robot;
        self.mRatio = 100;
        self.mMaxDimLens = dimensionLengths;
        self.mCollisionMgr = CollisionManager( robot );
            
    def map2UnscaledSpace( self, position ):
        """The given parameters are scaled, we want to map them to -1.0~1.0PI"""
        angles = [0] * len(position);
        for i in range(0, len(position)):
            angles[i] = ( position[i] - self.mMaxDimLens[i]/2 ) / float( self.mMaxDimLens[i] ) * math.pi * 2;
        return tuple(angles);

    def map2ScaledSpace( self, angles ):
        """Given angles in the unscaled real world, map them to scaled space."""
        retXcoord = alpha * self.mScaledWidth / (2.0*math.pi) + self.mScaledWidth/2.0;
        retYcoord = phi  * self.mScaledHeight / (2.0*math.pi) + self.mScaledHeight/2.0;
        position = [0] * len(angles);
        for i in range(0, len(angles)):
            position[i] = angles[i] * self.mMaxDimLens[i] / (2.0*math.pi) + self.mMaxDimLens[i]/2.0;

        return position;

    def mapPath2UnscaledSpace(self, start, goal):
        """Map a path between two configurations in scaled space to unscaled space"""
        deltas = [0] * len(start);
        for i in range(0, len(start)):
            deltas[i] = goal[i] - start[i];
            if( deltas[i] > 0 and self.mMaxDimLens[i] - deltas[i] < deltas[i] ):
                deltas[i] = -(self.mMaxDimLens[i] - deltas[i]);
            elif( deltas[i] < 0 and self.mMaxDimLens[i] + deltas[i] < (-deltas[i]) ):
                deltas[i] = self.mMaxDimLens[i] + deltas[i];

        #if( dx > 0 and self.mScaledWidth - dx < dx ):
        #    dx = -(self.mScaledWidth - dx);
        #elif( dx < 0 and self.mScaledWidth - (-dx) < (-dx)):
        #    dx = self.mScaledWidth - (-dx);
        #if( dy > 0 and self.mScaledHeight - dy < dy ):
        #    dy = -(self.mScaledHeight - dy);
        #elif( dy < 0 and self.mScaledHeight-(-dy)<(-dy) ):
        #    dy = self.mScaledHeight-(-dy);

        newgoal = [0] * len(start);
        for i in range(0, len(newgoal)):
            newgoal[i] = start[i] + deltas[i];

        start_ = self.map2UnscaledSpace( start );
        goal_ = self.map2UnscaledSpace( newgoal );

        return tuple(start_), tuple(goal_);