import pygame
class Line(object):
    """description of class"""

    def __init__(self, x1, y1, x2, y2):
        if(x1 < x2):
            self.X1 = float(x1);
            self.Y1 = float(y1);
            self.X2 = float(x2);
            self.Y2 = float(y2);
        else:
            self.X1 = x2;
            self.Y1 = y2;
            self.X2 = x1;
            self.Y2 = y1;
        # y = kx + t
        self.k = 0;
        if self.X1 != self.X2:
            self.k = float(self.Y2-self.Y1)/float(self.X2-self.X1);
        self.t =  self.Y1 - self.k * self.X1;
        pass

    def intersect( self, line ):
        if( self.k == line.k and self.t != line.t  ):
            return False;
            pass
        elif self.k == line.k:
            return True;
        else:
            x = (line.t - self.t) / ( self.k - line.k );
            if x < self.X2 and x > self.X1 and x < line.X2 and x > line.X1:
                return True;
            return False;
            pass

    def render( self, screen, ):
        pygame.draw.line(screen, (255, 0, 255), (self.X1, self.Y1), (self.X2, self.Y2) );
