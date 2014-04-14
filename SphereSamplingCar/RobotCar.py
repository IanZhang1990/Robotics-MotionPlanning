
import math
import pygame
import sys, os
import copy

class RobotCar(object):
    """description of class"""

    def __init__( self, obstacles, x, y, phi ):
        self.mObstacles = obstacles;
        self.mX = x;                # X position of the center of the car
        self.mY = y;                # Y position of the center of the car
        self.mPhi = phi;             # angle with the horizontal level
        self.mWidth = 70;
        self.mHeight = 40;

        self.mCarImg = pygame.image.load('car.png')
        self.mCarImg = pygame.transform.scale( self.mCarImg, ( self.mWidth, self.mHeight) );


    def ifCollide( self ):
        """Test if the car is colliding with anything."""

    def move( self, mode, time ):
        """@param mode: forward | backward | right_forward | left_forward | right_backward | left_backward
         @param time: time of action"""
        omega = 0.02;
        r = 100;
         
        if mode == "forward":
            speed = 2;
            self.mX = self.mX + speed * math.cos( self.mPhi );
            self.mY = self.mY + speed * math.sin( self.mPhi );
            pass;
        elif mode == "backward":
            speed = -2;
            self.mX = self.mX + speed * math.cos( self.mPhi );
            self.mY = self.mY + speed * math.sin( self.mPhi );
            pass;
        elif mode == "right_forward":
            theta_old = self.mPhi + math.pi / 2.0;
            center = ( self.mX - r*math.cos(theta_old), self.mY - r*math.sin( theta_old ) );
            dltTheta = - omega * time;
            theta_new = theta_old + dltTheta;
            self.mX = center[0] + r*math.cos( theta_new );
            self.mY = center[1] + r*math.sin( theta_new );
            self.mPhi = theta_new - math.pi/2.0;
            pass;
        elif mode == "left_forward":
            theta_old = self.mPhi - math.pi / 2.0;
            center = ( self.mX - r*math.cos(theta_old), self.mY - r*math.sin( theta_old ) );
            dltTheta = omega * time;
            theta_new = theta_old + dltTheta;
            self.mX = center[0] + r*math.cos( theta_new );
            self.mY = center[1] + r*math.sin( theta_new );
            self.mPhi = theta_new + math.pi/2.0;
            pass;
        elif mode == "right_backward":
            theta_old = self.mPhi + math.pi / 2.0;
            center = ( self.mX - r*math.cos(theta_old), self.mY - r*math.sin( theta_old ) );
            dltTheta =  omega * time;
            theta_new = theta_old + dltTheta;
            self.mX = center[0] + r*math.cos( theta_new );
            self.mY = center[1] + r*math.sin( theta_new );
            self.mPhi = theta_new - math.pi/2.0;
            pass;
        elif mode == "left_backward":
            theta_old = self.mPhi - math.pi / 2.0;
            center = ( self.mX - r*math.cos(theta_old), self.mY - r*math.sin( theta_old ) );
            dltTheta = - omega * time;
            theta_new = theta_old + dltTheta;
            self.mX = center[0] + r*math.cos( theta_new );
            self.mY = center[1] + r*math.sin( theta_new );
            self.mPhi = theta_new + math.pi/2.0;
            pass;

        dx = math.cos(self.mPhi);
        dy = math.sin(self.mPhi);





    def rotate(self, image, angle, screenHeight):
        """rotate a Surface, maintaining position."""
        pos = (self.mX-self.mWidth/2.0, screenHeight - (self.mY+self.mHeight/2.0))

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
        screenHeight = imgSurf.get_height()
        rotatedSurf, rotRect = self.rotate( self.mCarImg, self.mPhi, screenHeight )
        imgSurf.blit(rotatedSurf, rotRect)
        pygame.draw.circle( imgSurf, ( 255,0,0 ), (int(self.mX), int(screenHeight - self.mY)), 4 );
        #pygame.draw.rect( imgSurf,( 0, 255,0 ), rotRect, 2 );
        pygame.display.update()