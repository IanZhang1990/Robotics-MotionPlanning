from SampleManager import *
import math;
import pygame;


class Astar2Node:
	def __init__(self, sphere, parent):
		self.mParentNode = parent;
		self.mSphere = sphere;		
		self.mG = 0;
		self.mH = 0;
		self.mF = 0; 				# F = cost + heuristic

class AstarPlus(object):
    """description of class"""
    def __init__( self, spheres ):
        """Constructor of AstarSearcher. The constructor will iterate each given spheres,
		and record their overlapping relationship. 
		@param spheres: distance samples got by SampleManager. Those samples should have 
		covered the whole free space.
		"""
        self.mSpheres = spheres;
        self.mOverlapDict = defaultdict( list );
        
        for sphere in self.mSpheres:
            for other in self.mSpheres:
                if( sphere == other ):
                    continue;

                dx = sphere.mSample[0] - other.mSample[0];
                dy = sphere.mSample[1] - other.mSample[1];
                dist = math.sqrt( dx**2+dy**2 );
                if( dist < (sphere.mRadius+other.mRadius) ):
                    # Overlap! Record it in the dictionary
                    self.mOverlapDict[sphere] += [ other ];

    def findOwnerSphere( self, config, maxWidth, maxHeight ):
        """Given sample with (x,y) coordinate, find the sphere the sample is in."""
        maxRadius = 0;
        chosenSphere = None;
        for sphere in self.mSpheres:
            if sphere.isInside(config, maxWidth, maxHeight):
                if maxRadius <= sphere.mRadius:
                    maxRadius = sphere.mRadius;
                    chosenSphere = sphere;
        return chosenSphere;


    def distance( self, one, two ):
        dx = one[0] - two[0];
        dy = one[1] - two[1];
        return math.sqrt(dx**2+dy**2);

    def astarSearch( self, start, goal, maxWidth, maxHeight, imgsurface=None ):
        """Given a start and goal point, search for an optimal path connecting them"""
        startSphere = self.findOwnerSphere( start, maxWidth, maxHeight );
        goalSphere = self.findOwnerSphere(goal, maxWidth, maxHeight);

        pygame.draw.circle( imgsurface, (255,0,0), (int(startSphere.mSample[0]), int(startSphere.mSample[1])), int(startSphere.mRadius), 2 );
        pygame.draw.circle( imgsurface, (255,0,0), (int(goalSphere.mSample[0]), int(goalSphere.mSample[1])), int(goalSphere.mRadius), 2 );
        pygame.display.update();

        def backtrace( node ):
            path = []
            path.append( node.mSphere )
            while( node.mParentNode is not None ):
                path.append( node.mParentNode.mSphere );
                node = node.mParentNode;
            path.reverse();
            return path;

        openList = set();
        closedList = set();

        starNode = Astar2Node(startSphere, None);
        openList.add(starNode);

        while len(openList) is not 0:
            current = min(openList, key=lambda inst:inst.mF);
            openList.remove( current );
            if current.mSphere == goalSphere:
                return backtrace( current );
            for event in pygame.event.get():
                pass;
            pygame.draw.circle( imgsurface, (250,250,0), (int(current.mSphere.mSample[0]),int(current.mSphere.mSample[1])), int(current.mSphere.mRadius), 2);
            pygame.display.update();
            successors = self.mOverlapDict[current.mSphere];
            #print "current: {0} \towener Sphere: {1}".format(current.mPosition, currOwnerSphere.mSample);
            #print current.mPosition;
            for suc in successors:
                sucNode = Astar2Node( suc, current )
                sucNode.mG = current.mG + self.distance( suc.mSample, current.mSphere.mSample );
                sucNode.mH = self.distance( suc.mSample, goal ) + suc.mRadius;
                sucNode.mF = sucNode.mG + sucNode.mH;
                print "{0}\t{1}\t{2}".format(sucNode.mG,sucNode.mH,sucNode.mF);



                same = filter( lambda inst: inst.mSphere== suc , openList)

                if len(same) is not 0:
                    for sameSphere in same: 
                        if sameSphere.mF > sucNode.mF:
                            sameSphere.mF = sucNode.mF;
                else:
                    openList.add( sucNode );

                same = filter( lambda inst: inst.mSphere == suc, closedList)				
                if len(same) is not 0:
                    for sameSphere in same: 
                        if sameSphere.mF > sucNode.mF:
                            sameSphere.mF = sucNode.mF;
                pass
            closedList.add( current );
            pass
        return None;



def loadDistSamplesFromFile( filename ):
    file2read = open( filename, 'r' );
    distSamples = [];
    for line in file2read:
        strDistSamp = line;
        info = strDistSamp.split( '\t' );
        distSamp = DistSample( float(info[0]), float(info[1]), float(info[2]));
        if( distSamp.mRadius >= 2 ):
            distSamples += [ distSamp ];
    return distSamples;

if __name__ == "__main__":
	
    WIDTH = 1366
    HEIGHT = 768

    spheres = loadDistSamplesFromFile( "F:\Github\Robotics-MotionPlanning\SampleWithMoreInfo\distSample.txt" );
    

    ######## Set up the pygame stuff
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
    DISPLAYSURF.fill((255,255,255));

    pygame.draw.circle( DISPLAYSURF, (0,0,0), (693,393), 2 );
    pygame.draw.circle( DISPLAYSURF, (0,0,0), (1152, 641), 2 );
    for sphere in spheres:
        pygame.draw.circle( DISPLAYSURF, (0,0,200), (int(sphere.mSample[0]), int(sphere.mSample[1])), int(sphere.mRadius), 1 );
    pygame.display.update();


    astarSearcher = AstarPlus( spheres );
    path = astarSearcher.astarSearch((693,393), (1152, 641),WIDTH, HEIGHT, DISPLAYSURF);

    for sphere in path:
        pygame.draw.circle( DISPLAYSURF, (0,250,0), (int(sphere.mSample[0]), int(sphere.mSample[1])), int(sphere.mRadius), 3 );

    pygame.image.save( DISPLAYSURF, "AStar2.PNG" );

    pygame.quit();