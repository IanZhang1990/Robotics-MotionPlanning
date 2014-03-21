import pygame, sys, os, datetime
from pygame.locals import *

from GameWorld import *
from CSpaceWorld import *
from RobotArm import *
from SampleManager import *
from AstarSearcher import *

pygame.init()
WIDTH = 1366
HEIGHT = 768
#DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))

# segment obstacles
g_obstacles = []#[Rect( 40,40, 100, 150 ), Circle( 300, 200, 50 ), Circle( 520, 200, 50 )]




def main():

    ######## Set up the robot stuff
    #obstacles = [ Sphere( 550, 300, 50 ), Sphere( 550, 500, 30 ),Sphere( 850, 500, 50 ), Sphere( 900, 300, 30 ), Sphere( 790, 450, 20 ) ];
    obstacles = [ Sphere( 550, 300, 50 ),Sphere( 850, 500, 50 ),  Sphere( 790, 450, 20 ) ];
    robot = RobotArm( (WIDTH/2, HEIGHT/2), obstacles );

    cSpaceWorld = CSpaceWorld( robot );

    ######## Set up the pygame stuff
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
    DISPLAYSURF.fill((255,255,255));
    for sphere in obstacles:
        sphere.render( DISPLAYSURF, ( 50, 50, 50 ) );

    #pygame.image.save( DISPLAYSURF, "PhysicSpace.PNG" )

    ####### Randomly sample the world, show it in the image
    #DISPLAYSURF.fill((255,255,255));
    #CSpaceSurface = cSpaceWorld.renderCSpace();
    CSpaceSurface = cSpaceWorld.loadCSpace( "CSpace.txt" );
    #pygame.image.save(CSpaceSurface, "CSpace.PNG");



    ######## For testing only
    #alpha = 0;
    #phi = 0#math.pi / 2;

    #while True:
    #    DISPLAYSURF.fill((255,255,255))
    #    alpha = alpha + 0.001
    #    #phi = phi + 0.002;

    #    for sphere in obstacles:
    #        sphere.render( DISPLAYSURF, ( 50, 50, 50 ) );

    #    ifcollide = robot.setParams( alpha, phi );
    #    robot.render( DISPLAYSURF, ifcollide );

    #    for event in pygame.event.get():
    #        if event.type == QUIT:
    #            pygame.quit()
    #            sys.exit()
    #    pygame.display.update();
    #    pass


    ######## Now, let's begin to sample spheres in the scaled-CSpace.
    sampleManager = SampleManager( cSpaceWorld );
    #sampleManager.distSampleOneThread(20, CSpaceSurface);
    #sampleManager.writeSamplesToFile("CSpaceDistSamples.txt");
    sampleManager.loadDistSamplesFromFile("CSpaceDistSamples.txt");
    sampleManager.renderAllDistSamples(CSpaceSurface);



    ######## Let us find a path
    astarSearcher = AstarSearcher( sampleManager.mDistSamples, cSpaceWorld.mScaledWidth, cSpaceWorld.mScaledHeight );
    start = ( 0, -math.pi/6 ); goal = (math.pi/3, math.pi/1.5);
    start_x, start_y = cSpaceWorld.map2ScaledSpace( start[0], start[1] );
    goal_x, goal_y = cSpaceWorld.map2ScaledSpace( goal[0], goal[1] );
    pygame.draw.circle(CSpaceSurface, (0,0,0), (int(start_x),int(start_y)), 5);
    pygame.draw.circle(CSpaceSurface, (0,0,0), (int(goal_x), int(goal_y)), 5);
    path = astarSearcher.astarSearch( (start_x,start_y), (goal_x, goal_y), cSpaceWorld, CSpaceSurface );




    if path is not None:
        for i in range( 1, len(path) ):
            pygame.draw.line( CSpaceSurface, (0,255,0), path[i-1], path[i] );
            pygame.display.update();
    pygame.image.save(CSpaceSurface, "CSpace.PNG");

    if path is not None:
        for i in range(1, len(path)):
            start, goal = cSpaceWorld.mapPath2UnscaledSpace( path[i-1], path[i] );
            robot.move( start, goal, DISPLAYSURF );

    pygame.image.save( DISPLAYSURF, "PhysicSpace.PNG" );
    return;

if __name__ == "__main__":
	#freeze_support();
	main();
	pygame.quit();
