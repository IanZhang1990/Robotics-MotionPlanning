
import math
import pygame
import sys, os
import copy
import utility


class Sphere:
    def __init__( self, x, y, r ):
        self.mPos = (x, y);
        self.mRadius = r;

    def render(self, imgsurface, color):
        """Render the sphere"""
        pygame.draw.circle( imgsurface, color, self.mPos, self.mRadius );


class RobotCar(object):
    """description of class"""

    def __init__( self, obstacles, x, y, phi ):
        self.mObstacles = obstacles;
        self.mX = x;                # X position of the center of the car
        self.mY = y;                # Y position of the center of the car
        self.mPhi = phi;             # angle with the horizontal level
        self.mWidth = 70;
        self.mHeight = 40;
        self.mIfCollide = False;

        self.mCarImg = pygame.image.load('car.png')
        self.mCarImg = pygame.transform.scale( self.mCarImg, ( self.mWidth, self.mHeight) );


    def ifCollide( self, imgSurf = None):
        """Test if the car is colliding with anything."""
        #midTop =    ( self.mX + self.mWidth/2.0*math.cos(self.mPhi), self.mY + self.mWidth/2.0*math.sin(self.mPhi) );
        #midButtom = ( self.mX + self.mWidth/2.0*math.cos(self.mPhi+math.pi), self.mY + self.mWidth/2.0*math.sin(self.mPhi+math.pi) );
        midLeft =   [ self.mX + self.mHeight/2.0*math.cos( math.pi/2.0+self.mPhi ), self.mY - self.mHeight/2.0*math.sin( math.pi/2.0+self.mPhi ) ];
        midRight =  [ self.mX + self.mHeight/2.0*math.cos( math.pi/2.0-self.mPhi ), self.mY + self.mHeight/2.0*math.sin( math.pi/2.0-self.mPhi ) ];

        topleft = [ midLeft[0] + self.mWidth/2.0*math.cos(self.mPhi), midLeft[1] - self.mWidth/2.0*math.sin(self.mPhi) ];
        topright = [ midRight[0] + self.mWidth/2.0*math.cos(self.mPhi), midRight[1] - self.mWidth/2.0*math.sin(self.mPhi) ];
        buttleft = [ midLeft[0] - self.mWidth/2.0*math.cos(self.mPhi), midLeft[1] + self.mWidth/2.0*math.sin(self.mPhi) ];
        buttright = [ midRight[0] - self.mWidth/2.0*math.cos(self.mPhi), midRight[1] + self.mWidth/2.0*math.sin(self.mPhi) ];


        color = ( 0, 250, 0 );
        if self.mIfCollide:
            color = ( 255, 0, 0 );
        if( imgSurf is not None ):
            pygame.draw.line( imgSurf, color, topleft, topright );
            pygame.draw.line( imgSurf, color, topleft, buttleft );
            pygame.draw.line( imgSurf, color, buttleft, buttright );
            pygame.draw.line( imgSurf, color, topright, buttright );

        self.mIfCollide = False;

        for obst in self.mObstacles:
            # assume each obstacle is sphere
            if utility.sphereLineCollision( obst.mPos, obst.mRadius, topleft, topright ):
                self.mIfCollide = True;
                return True;
            if utility.sphereLineCollision( obst.mPos, obst.mRadius, topleft, buttleft ):
                self.mIfCollide = True;
                return True;
            if utility.sphereLineCollision( obst.mPos, obst.mRadius, buttleft, buttright ):
                self.mIfCollide = True;
                return True;
            if utility.sphereLineCollision( obst.mPos, obst.mRadius, topright, buttright ):
                self.mIfCollide = True;
                return True;

        return False;


    def move( self, mode, time, imgSurf = None ):
        """@param mode: forward | backward | right_forward | left_forward | right_backward | left_backward
         @param time: time of action"""
        omega = 0.02;
        r = 100;
         
        if mode == "forward":
            speed = 2;
            self.mX = self.mX + speed * math.cos( self.mPhi );
            self.mY = self.mY - speed * math.sin( self.mPhi );
            pass;
        elif mode == "backward":
            speed = -2;
            self.mX = self.mX + speed * math.cos( self.mPhi );
            self.mY = self.mY + speed * math.sin( self.mPhi );
            pass;
        elif mode == "right_forward":
            theta_old = self.mPhi + math.pi / 2.0;
            center = ( self.mX - r*math.cos(theta_old), self.mY + r*math.sin( theta_old ) );
            dltTheta = - omega * time;
            theta_new = theta_old + dltTheta;
            self.mX = center[0] + r*math.cos( theta_new );
            self.mY = center[1] - r*math.sin( theta_new );
            self.mPhi = theta_new - math.pi/2.0;
            pass;
        elif mode == "left_forward":
            theta_old = self.mPhi - math.pi / 2.0;
            center = ( self.mX - r*math.cos(theta_old), self.mY + r*math.sin( theta_old ) );
            dltTheta = omega * time;
            theta_new = theta_old + dltTheta;
            self.mX = center[0] + r*math.cos( theta_new );
            self.mY = center[1] - r*math.sin( theta_new );
            self.mPhi = theta_new + math.pi/2.0;
            pass;
        elif mode == "right_backward":
            theta_old = self.mPhi + math.pi / 2.0;
            center = ( self.mX - r*math.cos(theta_old), self.mY + r*math.sin( theta_old ) );
            dltTheta =  omega * time;
            theta_new = theta_old + dltTheta;
            self.mX = center[0] + r*math.cos( theta_new );
            self.mY = center[1] - r*math.sin( theta_new );
            self.mPhi = theta_new - math.pi/2.0;
            pass;
        elif mode == "left_backward":
            theta_old = self.mPhi - math.pi / 2.0;
            center = ( self.mX - r*math.cos(theta_old), self.mY + r*math.sin( theta_old ) );
            dltTheta = - omega * time;
            theta_new = theta_old + dltTheta;
            self.mX = center[0] + r*math.cos( theta_new );
            self.mY = center[1] - r*math.sin( theta_new );
            self.mPhi = theta_new + math.pi/2.0;
            pass;

        return self.ifCollide(imgSurf);



    def rotate(self, image, angle):
        """rotate a Surface, maintaining position."""
        pos = (self.mX-self.mWidth/2.0, self.mY-self.mHeight/2.0)

        #draw surf to screen and catch the rect that blit returns
        #blittedRect = imgSurf.blit(self.mCarImg, pos)
        blittedRect = image.get_rect();
        blittedRect.x = pos[0]; blittedRect.y = pos[1];

        ##ROTATED
        #get center of surf for later
        oldCenter = blittedRect.center

        #rotate surf by DEGREE amount degrees
        rotatedSurf =  pygame.transform.rotate(image, math.degrees(angle))

        #get the rect of the rotated surf and set it's center to the oldCenter
        rotRect = rotatedSurf.get_rect()
        rotRect.center = oldCenter
        return rotatedSurf, rotRect 

    def render( self, imgSurf ):
        rotatedSurf, rotRect = self.rotate( self.mCarImg, self.mPhi )
        imgSurf.blit(rotatedSurf, rotRect)

        #pygame.draw.circle( imgSurf, ( 255,0,0 ), (int(self.mX), int(self.mY)), 4 );
        #color = ( 0, 255, 0 )
        #if self.mIfCollide:
        #    color = ( 255, 0, 0 )
        #pygame.draw.rect( imgSurf, color, rotRect, 2 );
        pygame.display.update()