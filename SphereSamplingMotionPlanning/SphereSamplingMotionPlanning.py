import pygame, sys, os, datetime
from pygame.locals import *

from GameWorld import *
from CSpaceWorld import *
from RobotArm import *
from SampleManager import *

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

    pygame.image.save( DISPLAYSURF, "PhysicSpace.PNG" )

    ####### Randomly sample the world, show it in the image
    DISPLAYSURF.fill((255,255,255));
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
    pygame.image.save(CSpaceSurface, "CSpace.PNG");



    return;

if __name__ == "__main__":
	#freeze_support();
	main();
	pygame.quit();
