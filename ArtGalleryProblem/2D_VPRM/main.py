# import the pygame module, so you can use it
import pygame
from Polygon import Polygon
from VPRM import VPRM
from Line import Line

# define a main function
def main():
    
    configuration = Polygon();
    solver = VPRM( configuration );

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")
    
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((1366,768))
    white = (255,255,255)
    
    # define a variable to control the main loop
    running = True
    screen.fill(white)

    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        
        if( solver.mUpdate ):
            if not solver.mSolved:
                solver.solveStep( 200, screen );
            solver.render(screen);
        pygame.display.flip()
    
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
