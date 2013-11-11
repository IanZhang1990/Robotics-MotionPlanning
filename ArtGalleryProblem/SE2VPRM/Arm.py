import pygame
import math

class Arm(object):
    """Robotics Arm whose motion is defined by two angles: theta, phi.
                        /
                      /phi______
                    / 
                  /
    ______/ theta _________
    """

    def __init__(self):
        self.mLen1 = 100;
        self.mLen2 = 100;
        self.mTheta = 0;
        self.mPhi = 0;
        self.mOrigin = ( 600, 600 );
        pass;

    def midPoint(self):
        return ( self.mOrigin[0] + int( self.mLen1*math.cos( self.mTheta ) ), self.mOrigin[1] - int(self.mLen1*math.sin( self.mTheta )) );

    def endPoint( self ):
        return ( self.midPoint()[0] + int(self.mLen2*math.cos( self.mPhi )), self.midPoint()[1] - int(self.mLen2*math.sin( self.mPhi )) );

    def render( self, screen ):
        pygame.draw.line( screen, (40, 40, 40), ( 0, 600 ), (1366, 600), 2  )
        pygame.draw.circle(screen, ( 0, 230, 0 ), self.mOrigin, 5, 3);
        pygame.draw.line(screen, (0, 0, 230), self.mOrigin, self.midPoint(), 2 );
        pygame.draw.circle(screen, ( 0, 0, 230 ), self.midPoint(), 5, 3);
        pygame.draw.line(screen, (0, 0, 230), self.midPoint(), self.endPoint(), 2 );
        pygame.draw.circle(screen, ( 0, 0, 230 ), self.endPoint(), 5, 3);
        pass;

    def move( self, theta, phi ):
        self.mTheta = theta % ( math.pi );     # first joint:  0~180
        self.mPhi = phi % ( math.pi * 2 );           # secont joint: 0~360
        pass;