import pygame
from pygame.locals import *
import Box2D
from Box2D.b2 import *

from RobotArm import *

# --- constants ---
# Box2D deals with meters, but we want to display pixels, 
# so define a conversion factor:
PPM=5.0 # pixels per meter
TARGET_FPS=60
TIME_STEP=1.0/TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT=800,600
b2_pi=3.14159265359

# --- pygame setup ---
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Simple pygame example')
clock=pygame.time.Clock()

# --- pybox2d world setup ---
# Create the world
world=world(gravity=(0,-10),doSleep=True)


robotArm = TriJointArm( world, (80, 30) )

colors = {
    staticBody  : (127,127,127,255),
    dynamicBody : (127,127,127,255),
}

# --- main game loop ---
running=True
while running:
    # Check the event queue
    for event in pygame.event.get():
        if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
            # The user closed the window or pressed escape
            running=False

    screen.fill((0,0,0,0))
    
    robotArm.updateJoints(0.5*b2_pi, 0.25*b2_pi, 0.5*b2_pi);
    #robotArm.render(screen, PPM);
    # Draw the world
    for body in world.bodies: # or: 
        # The body gives us the position and angle of its shapes
        for fixture in body.fixtures:
            # The fixture holds information like density and friction,
            # and also the shape.
            shape=fixture.shape
            
            # Naively assume that this is a polygon shape. (not good normally!)
            # We take the body's transform and multiply it with each 
            # vertex, and then convert from meters to pixels with the scale
            # factor. 
            vertices=[(body.transform*v)*PPM for v in shape.vertices]

            # But wait! It's upside-down! Pygame and Box2D orient their
            # axes in different ways. Box2D is just like how you learned
            # in high school, with positive x and y directions going
            # right and up. Pygame, on the other hand, increases in the
            # right and downward directions. This means we must flip
            # the y components.
            vertices=[(v[0], SCREEN_HEIGHT-v[1]) for v in vertices]

            pygame.draw.polygon(screen, colors[body.type], vertices)

    # Make Box2D simulate the physics of our world for one step.
    # Instruct the world to perform a single step of simulation. It is
    # generally best to keep the time step and iterations fixed.
    # See the manual (Section "Simulating the World") for further discussion
    # on these parameters and their implications.
    world.Step(TIME_STEP, 10, 10)

    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)
    
pygame.quit()
print('Done!')