import pygame;

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



