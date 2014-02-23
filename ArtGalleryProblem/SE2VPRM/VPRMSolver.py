import math
import random

class VPRMSolver(object):
    """description of class"""

    def __init__(self, configuration):
        self.mConf = configuration;
        self.mGuards = [];
        self.mPath = []
        pass

    def dist( theta1, phi1, theta2, phi2 ):
        return sqrt( (theta2-theta1)*(theta2-theta1)+(phi2-phi1)*(phi2-phi1) );

    def checkCollision( self, theta1, phi1, theta2, phi2 ):
        dir = ( theta2-theta1, phi2-phi1 );
        dist = dist( theta1, phi1, theta2, phi1 );
        resolution = ( (theta2-theta1)/dist, (phi2-phi1)/dist );
        curr = (theta1, phi1);
        while dist( theta1, phi1, curr[0], curr[1] )>dist:
            if self.mConf.ifCollide( curr[0], curr[1] ):
                return True;
            else:
                curr = ( curr[0]+resolution[0], curr[1]+resolution[1] );
            pass
        return False;
        pass;

    def solve( self, maxSample ):
        samples = 0;
        while( samples < maxSample ):
            theta = random.random() * math.pi;
            phi = random.random() * math.pi*2;
            isGuard = True;
            for guard in self.mGuards:
                isGuard = self.checkCollision( guard[0], gurad[1], theta, phi );
                if not isGuard:
                    break;
                pass
            if isGuard:
                self.mGuards = self.mGuards +[ (theta, phi) ];
        pass