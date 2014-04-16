import pygame, sys
from pygame.locals import *
from RobotCar import *;
from CSpaceWorld import *;
from SampleManager import *;
import math # math library


pygame.init()
mainClock = pygame.time.Clock()
degree = 0
WHITE = 250,250,250
rect2 = pygame.rect = (100,100,50,50)
WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Car Test')


def main():
    obstacles = [ Sphere( 150, 300, 80 ), Sphere( 550, 800, 80 ),Sphere( 750, 200, 90 ), Sphere( 500, 500, 130 ), Sphere( 790, 650, 100 )]
    robot = RobotCar( obstacles, 600, 400, math.pi/6.0 );
    originDimLens = [ WINDOWWIDTH, WINDOWHEIGHT ]
    maxDimLens = [ 1000, 1000, 1000 ];
    cSpaceWorld = CSpaceWorld( robot, originDimLens, maxDimLens );

    ######## Now, let's begin to sample spheres in the scaled-CSpace.
    sampleManager = SampleManager( cSpaceWorld );
    sampleManager.distSampleUsingObstSurfSamps(20, maxDimLens);
    sampleManager.writeSamplesToFile("CSpaceDistSamples.txt");
    #sampleManager.loadDistSamplesFromFile("CSpaceDistSamples.txt");
    return;

"""
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((250, 250, 250));

    for obst in obstacles:
        obst.render( screen, ( 40,40,40 ) )


    time = 1;
    
    move = "right_backward";
    robot.move( move, time );
    #robot.ifCollide(screen)
    robot.render( screen );


    pygame.display.update()
    mainClock.tick(60)
"""



if __name__ == "__main__":
	#freeze_support();
	main();
	#pygame.quit();
