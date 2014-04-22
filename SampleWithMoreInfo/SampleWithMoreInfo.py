import pygame, sys, os, datetime
from pygame.locals import *
from Obstacle import *

from SampleManager import *
from PRM import *
from GraphSpanner import *
from AstarSearcher import *

pygame.init()
WIDTH = 1366
HEIGHT = 768
#DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))

sampleWorld = World( WIDTH, HEIGHT );
sampleMgr = SampleManager( sampleWorld );

# segment obstacles
g_obstacles = []#[Rect( 40,40, 100, 150 ), Circle( 300, 200, 50 ), Circle( 520, 200, 50 )]

# The space is partitioned into several
# Each part is not connected with others
# g_spaces = [ Rect( 0, 5, 300, 200 ), Rect( 320, 5, 200, 200 ), Circle( 100, 300, 90 ), Circle( 300, 300, 80 ), Circle( 500, 300, 80 ) ]
g_spaces = [ Rect( 1, 1, WIDTH-1, HEIGHT-1 ) ]

g_recordFile = "path.txt"


def writeVectorsToFile( vectors, filename ):
    file2write = open( filename, 'w' );
    plotFile = open( "Plot"+filename, 'w' )
    formattedData = ""
    plotData = ""
    for vector in vectors:
        currentData = ""
        for feature in vector:
            currentData += "{0}\t".format( str(feature) );
        formattedData += currentData + "\n";
        pass

    file2write.write( formattedData );
    file2write.close();

def main():

    global sampleWorld, sampleMgr;

    initSampleImage = pygame.display.set_mode( (WIDTH, HEIGHT) )
    initSampleImage.fill( (255, 255, 255) );


    #sampleWorld.buildWorld();
    #sampleWorld.saveWorld("world.txt");
    sampleWorld.loadWorld("world.txt");
    sampleWorld.renderCSpace( initSampleImage );
    sampleWorld.renderObstacles( initSampleImage );
    pygame.display.update();

    #print sampleWorld.mObstMgr.isPathFree( (1188, 274), (1188, 462) );
    #return;

    #rayShooter = RayShooter( 247, 260, sampleWorld.mObstMgr );
    #dist, ray = rayShooter.randShoot(36);
    #print "Smallest {0}".format(dist);
    #ray.drawRay(initSampleImage);
    #pygame.draw.circle( initSampleImage, ( 0, 250, 0 ), (247, 260), int(dist), 1 );

    """
    print "\nBegin to build PRM* at :{0}".format(datetime.datetime.now());
    prm = PRM( sampleWorld.mObstMgr, sampleMgr );
    prm.buildPRM_star();
    prm.renderRoadMap( initSampleImage);
    """

    print "\nBegin to sample spheres at :{0}".format(datetime.datetime.now());
    #sampleMgr.distSampleUsingObstSurfSamps( 20 );
    #sampleMgr.sampleWithMoreInfo(20);
    #sampleMgr.sampleWithDistInfo_multiThread( 10 )
    #sampleMgr.distSampleOneThread( 200 );
    #sampleMgr.writeSamplesToFile( "distSample.txt" );
    sampleMgr.loadDistSamplesFromFile( "distSample.txt" );
    sampleMgr.renderDistSample( initSampleImage );


    #print "\nBegin to build PRM* at :{0}".format(datetime.datetime.now());
    #prm = PRM( sampleWorld.mObstMgr, sampleMgr );
    #prm.build_nonvisArea_PRM_star(initSampleImage);
    #prm.renderRoadMap( initSampleImage);

    #astarSearcher = AstarSearcher( sampleMgr.mDistSamples );
    #path = astarSearcher.astarSearch( (314,113), (312, 290), initSampleImage );
    #if path is not None:
    #    for i in range( 1, len(path) ):
    #        pygame.draw.line( initSampleImage, (0,255,0), path[i-1], path[i] );


    pygame.image.save( initSampleImage, "SamplingImage.PNG" );

    """
    afterSpanningImg = pygame.display.set_mode( (WIDTH, HEIGHT) );
    afterSpanningImg.fill( (255, 255, 255) );

    sampleWorld.renderObstacles( afterSpanningImg );
    begin = datetime.datetime.now()
    spanner = GraphSpanner(prm.mGraph, sampleMgr.mDistSamples);
    print "Begin to span: {0}".format( begin );
    graph = spanner.span();
    end = datetime.datetime.now();
    timeCost = end-begin;
    print "Finished spanning: {0}".format(end);
    print "Time cost: {0}".format(timeCost);
    graph.render( afterSpanningImg, (0,250,0) );
    sampleMgr.renderDistSample( afterSpanningImg );
    pygame.image.save( afterSpanningImg, "AfterSpanning.PNG" );
    """

    return;

if __name__ == "__main__":
    #freeze_support();
    main();
    pygame.quit();
