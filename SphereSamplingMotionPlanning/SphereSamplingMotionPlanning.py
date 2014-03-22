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
    obstacles = [ Sphere( 550, 300, 50 ),Sphere( 850, 500, 50 ),  Sphere( 790, 450, 20 ) ];
    robot = RobotArm( (WIDTH/2, HEIGHT/2), obstacles );

    cSpaceWorld = CSpaceWorld( robot );

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
    #path = astarSearcher.astarSearch( (start_x,start_y), (goal_x, goal_y), cSpaceWorld, CSpaceSurface );
    #astarSearcher.savePath(path);
    path = astarSearcher.loadPath("path.txt");
    if path is not None:
        for i in range( 1, len(path) ):
            drawLine( path[i-1], path[i], CSpaceSurface, (0,255,0), cSpaceWorld.mScaledWidth, cSpaceWorld.mScaledHeight )
            #pygame.draw.line( CSpaceSurface, (0,255,0), path[i-1], path[i] );
            pygame.display.update();
    pygame.image.save(CSpaceSurface, "CSpace.PNG");


    ######## Set up the pygame stuff
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
    DISPLAYSURF.fill((255,255,255));
    for sphere in obstacles:
        sphere.render( DISPLAYSURF, ( 50, 50, 50 ) );

    ifCollide = robot.setParams( goal[0], goal[1] );
    robot.render( DISPLAYSURF, True );

    pathLen = len(path);
    perPathColorChange = 180 / pathLen;
    pathCount = 0;

    if path is not None:
        for i in range(1, len(path)):
            chanel = 255 - perPathColorChange * pathCount;
            beginColor = ( chanel,chanel, chanel );
            chanel = 255 - perPathColorChange * (pathCount+1);
            endColor = (chanel, chanel, chanel);
            pathCount += 1;
            print "{0}\t{1}".format( path[i-1], path[i] );
            start_, goal_ = cSpaceWorld.mapPath2UnscaledSpace( path[i-1], path[i] );
            robot.move( start_, goal_, beginColor, endColor, DISPLAYSURF );

    pygame.image.save( DISPLAYSURF, "PhysicSpace.PNG" );
    return;

if __name__ == "__main__":
	#freeze_support();
	main();
	pygame.quit();
