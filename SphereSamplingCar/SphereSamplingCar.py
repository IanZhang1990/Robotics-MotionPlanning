import pygame, sys
from pygame.locals import *
from RobotCar import *;

import math # math library


pygame.init()
mainClock = pygame.time.Clock()
degree = 0
WHITE = 250,250,250
rect2 = pygame.rect = (100,100,50,50)
WINDOWWIDTH = 1200
WINDOWHEIGHT = 750
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Car Test')

car = RobotCar( None, 600, 400, math.pi/3.0 );

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((40, 40, 40));

    time = 1;
    
    move = "right_forward";
    car.move( move, time );
    car.render( screen );


    pygame.display.update()
    mainClock.tick(60)