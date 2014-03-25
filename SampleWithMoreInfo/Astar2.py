
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
                if( math.sqrt( dx**2+dy**2 ) <= (sphere.mRadius+other.mRadius) ):
                    # Overlap! Record it in the dictionary
                    self.mOverlapDict[sphere] += [ other ];

    def findOwnerSphere( self, x, y ):
        """Given sample with (x,y) coordinate, find the sphere the sample is in."""
        minCenterDist = 1000000000;
        chosenSphere = None;
        for sphere in self.mSpheres:
            if sphere.withInArea( x, y ):
                dx = x - sphere.mSample[0];
                dy = y - sphere.mSample[1];
                dist = math.sqrt( dx**2+dy**2 );
                if minCenterDist >= dist:
                    minCenterDist = dist;
                    chosenSphere = sphere;
        return chosenSphere;


    def astarSearch( self, start, goal, imgsurface=None ):
        """Given a start and goal point, search for an optimal path connecting them"""
