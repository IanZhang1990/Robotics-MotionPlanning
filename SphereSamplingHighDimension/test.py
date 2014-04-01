import pygame, sys, os, datetime
from pygame.locals import *
from random import randint;

import math;


pygame.init()
WIDTH = 1000
HEIGHT = 1000
DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))


def boundary( origin, radius, maxDimLens, num ):
    retList = [];
    dim = len( origin );
    for i in range(0, num):
        temp = [0] * dim;
        length = 0;
        for j in range(0, dim):
            temp[j] = randint( -100, 100 );
            length += temp[j]**2;
        length = math.sqrt( length );
        if length == 0:
                continue;
        for j in range(0, dim):
            temp[j] = int( (float(temp[j]) / float(length)) * (radius + 2) + origin[j]);
            if temp[j] < 0: temp[j] = maxDimLens[j] + temp[j];
            else: temp[j] = temp[j] % maxDimLens[j]; 
        retList.append( temp );
    return retList;

def isInside( position, origin, radius, maxDimLens):
    """Determine if a position is inside the sphere"""
    dim = len(position);
    deltas = [0] * dim;
    distSqr = 0;
    for i in range(0, dim):
        deltas[i] = math.fabs(position[i] - origin[i]);
        if math.fabs(maxDimLens[i] - deltas[i]) < deltas[i]:
            deltas[i] = math.fabs(maxDimLens[i] - deltas[i]);
        distSqr += deltas[i]**2;

    if distSqr < ( radius**2 ):
        return True;
    else:
        return False;

origin = (850, 850)
radius = 200;
bnds = boundary( origin, radius, [1000,1000], 300 );

while True:
    DISPLAYSURFACE.fill((255,255,255))
    pygame.draw.circle( DISPLAYSURFACE, (0,200,0), origin, radius, 2);

    for bnd in bnds:
        if (isInside( bnd, origin, radius, [1000, 1000] )):
            pygame.draw.circle( DISPLAYSURFACE, (255,0,0), bnd, 3 )
        else:
            pygame.draw.circle( DISPLAYSURFACE, (0,0,200), bnd, 3 )

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update();
    pass