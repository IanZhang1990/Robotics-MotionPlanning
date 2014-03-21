import pygame;
from pygame.locals import *

class Sphere:
    def __init__( self, x, y, r ):
        self.mPos = (x, y);
        self.mRadius = r;

    def render(self, imgsurface, color):
        """Render the sphere"""
        pygame.draw.circle( imgsurface, color, self.mPos, self.mRadius );


class GameWorld(object):
    """description of class"""

    def __init__(self, width, height):
        self.mWidth = width;
        self.mHeight = height;





def drawCircle( imgsurf, origin, radius):
    if(imgsurf is not None and radius <= 1000000000 and radius > 0):
            pygame.draw.circle( imgsurf, (0,0,250),(int(origin[0]),int(origin[1])), int(radius), 1 );
            if( origin[0]-radius<0 ):
                pygame.draw.circle( imgsurf, (0,0,250),(int(origin[0])+900,int(origin[1])), int(radius), 1 );
            if( origin[1]-radius<0 ):
                pygame.draw.circle( imgsurf, (0,0,250),(int(origin[0]),int(origin[1])+900), int(radius), 1 );
            if( origin[0]+radius>900 ):
                pygame.draw.circle( imgsurf, (0,0,250),(int(origin[0])-900,int(origin[1])), int(radius), 1 );
            if( origin[1]+radius>900 ):
                pygame.draw.circle( imgsurf, (0,0,250),(int(origin[0]),int(origin[1])-900), int(radius), 1 );


#############################################################################################
#WIDTH = 900;
#HEIGHT = 900;

#DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
#DISPLAYSURF.fill((255,255,255));

#while True:
#    DISPLAYSURF.fill((255,255,255))

#    drawCircle( DISPLAYSURF, (850,850), 100 );

#    for event in pygame.event.get():
#        if event.type == QUIT:
#            pygame.quit()
#            sys.exit()
#    pygame.display.update();
#    pass

#pygame.quit();






