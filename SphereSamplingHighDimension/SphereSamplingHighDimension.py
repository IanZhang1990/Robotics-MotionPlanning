import sys, os, datetime
import pygame;
from pygame.locals import *


from CSpaceWorld import *
from RobotArm import *
from SampleManager import *
from AstarSearcher import *

pygame.init()
WIDTH = 1366
HEIGHT = 768
DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))

# segment obstacles
g_obstacles = []#[Rect( 40,40, 100, 150 ), Circle( 300, 200, 50 ), Circle( 520, 200, 50 )]


def drawLine( start, end, imgsurf, color, maxWidth, maxHeight ):
    dx = ( end[0]-start[0] );
    dy = ( end[1]-start[1] );
    if( dx > 0 and maxWidth - dx < dx ):
        dx = -(maxWidth - dx);
    elif( dx < 0 and maxWidth - (-dx) < (-dx)):
        dx = maxWidth - (-dx);
    if( dy > 0 and maxHeight - dy < dy ):
        dy = -(maxHeight - dy);
    elif( dy < 0 and maxHeight-(-dy)<(-dy) ):
        dy = maxHeight-(-dy);

    newgoal = (start[0] + dx, start[1] + dy);
    pygame.draw.line( imgsurf, color, start, newgoal );

def main():

    ######## Set up the robot stuff
    #obstacles = [ Sphere( 550, 300, 50 ), Sphere( 550, 500, 30 ),Sphere( 850, 500, 50 ), Sphere( 900, 300, 30 ), Sphere( 790, 450, 20 ) ];
    obstacles = [ Sphere( 550, 300, 50 ), Sphere( 550, 500, 60 ), Sphere( 850, 450, 70 ), Sphere( 720, 340, 40 ) ];
    lens = [ 100,100,100 ];
    robot = RobotArm( (WIDTH/2, HEIGHT/2), obstacles, lens );
    maxDimLens = [ 1000, 1000, 1000 ];

    cSpaceWorld = CSpaceWorld( robot, maxDimLens );

    ######## Now, let's begin to sample spheres in the scaled-CSpace.
    sampleManager = SampleManager( cSpaceWorld );
    #sampleManager.distSampleUsingObstSurfSamps(20, maxDimLens);
    #sampleManager.writeSamplesToFile("CSpaceDistSamples.txt");
    sampleManager.loadDistSamplesFromFile("CSpaceDistSamples.txt");


    ######## Plan a motion task ########################
    astarSearcher = AstarSearcher( sampleManager.mDistSamples, maxDimLens );
    startScaled = ( 900, 200, 50 ); goalScaled = (600, 754, 189);
    start = cSpaceWorld.map2UnscaledSpace( startScaled );
    goal = cSpaceWorld.map2UnscaledSpace( goalScaled );
    before = datetime.datetime.now();
    #path = astarSearcher.astarSearch_Q( startScaled, goalScaled, cSpaceWorld );
    now = datetime.datetime.now();
    print now - before;
    #astarSearcher.savePath(path);
    path = astarSearcher.loadPath("path.txt");

    ######## Set up the pygame stuff
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
    DISPLAYSURF.fill((255,255,255));
    for sphere in obstacles:
        sphere.render( DISPLAYSURF, ( 50, 50, 50 ) );


    ifCollide = robot.setParams( start );
    robot.render( DISPLAYSURF, ifCollide );

    if path is not None:
        pathLen = len(path);
        perPathColorChange = 250 / pathLen;
        pathCount = 0;
        for i in range(1, len(path)):
            chanel = 255 - perPathColorChange * pathCount;
            beginColor = ( chanel,chanel, chanel );
            chanel = 255 - perPathColorChange * (pathCount+1);
            endColor = (chanel/5, chanel/5, chanel);
            pathCount += 1;
            #print "{0}\t{1}".format( path[i-1], path[i] );
            start_, goal_ = cSpaceWorld.mapPath2UnscaledSpace( path[i-1], path[i] );
            robot.move( start_, goal_, beginColor, endColor, DISPLAYSURF );

    ifCollide = robot.setParams( start );
    robot.render( DISPLAYSURF, ifCollide );
    ifCollide = robot.setParams( goal );
    robot.render( DISPLAYSURF, True );

    pygame.image.save( DISPLAYSURF, "PhysicSpace.PNG" );
    """
    ####### Randomly sample the world, show it in the image
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));

    ######## For testing only
    angles = [0,0,0];

    while True:
        DISPLAYSURF.fill((255,255,255))
        for i in range( 0, len(angles) ):
            angles[i] += 0.02

        for sphere in obstacles:
            sphere.render( DISPLAYSURF, ( 50, 50, 50 ) );

        ifcollide = robot.setParams( angles );
        robot.render( DISPLAYSURF, ifcollide );

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update();

        sleep( 0.01 );
        pass
    """
    return;

if __name__ == "__main__":
	#freeze_support();
	main();
	#pygame.quit();
