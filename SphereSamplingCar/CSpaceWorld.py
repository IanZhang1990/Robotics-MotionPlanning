
import sys, os
import math
import random
import copy
from CollisionManager import *
#import pygame;

class CSpaceWorld:
    #g_obcColor = [ 150, 150, 150 ]
    #g_obcThickness = 0;
    #g_spaceColor = [ 0, 150, 0 ]
    #g_spaceThickness = 3;

    def __init__( self, robot, dimensionLengths, cdimensionLengths ):
        self.mRobot = robot;
        self.mOriginDimLens = dimensionLengths;
        self.mMaxDimLens = cdimensionLengths;
        self.mCollisionMgr = CollisionManager( robot );
            
    def map2UnscaledSpace( self, config ):
        """The given parameters are scaled, we want to map them to unscaled with phi  (-PI ~ PI)"""
        unscaled = [0, 0, 0];

        for i in range(0, len(unscaled)-1):
            unscaled[i] = ( config[i] / float(self.mMaxDimLens[i])) * self.mOriginDimLens[i];

        unscaled[2] = ( config[2]%self.mMaxDimLens[2] - self.mMaxDimLens[2]/2 ) / float( self.mMaxDimLens[2] ) * math.pi * 2;
        return tuple(unscaled);

    def map2ScaledSpace( self, unscaled ):
        """Given angles in the unscaled real world, map them to scaled space."""
        scaled = [0] * len(unscaled);
        for i in range(0, len(angles)-1):
            scaled[i] = (unscaled[i] / float(self.mOriginDimLens[i])) * self.mMaxDimLens[i] ;

        scaled[2] = (unscaled[2] / (2*math.pi))*self.mMaxDimLens[2] + self.mMaxDimLens[2]/2.0;
        return tuple(scaled);

    def mapPath2UnscaledSpace(self, start, goal):
        """Map a path between two configurations in scaled space to unscaled space"""
        deltas = [0] * len(start);
        for i in range(0, len(start)):
            deltas[i] = goal[i] - start[i];
            if( deltas[i] > 0 and self.mMaxDimLens[i] - deltas[i] < deltas[i] ):
                deltas[i] = -(self.mMaxDimLens[i] - deltas[i]);
            elif( deltas[i] < 0 and self.mMaxDimLens[i] + deltas[i] < (-deltas[i]) ):
                deltas[i] = self.mMaxDimLens[i] + deltas[i];

        newgoal = [0] * len(start);
        for i in range(0, len(newgoal)):
            newgoal[i] = start[i] + deltas[i];

        start_ = self.map2UnscaledSpace( start );
        goal_ = self.map2UnscaledSpace( newgoal );

        return tuple(start_), tuple(goal_);