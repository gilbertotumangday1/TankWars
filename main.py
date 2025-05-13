#import modules
import pygame
import sys
import classes
import functions
from globals import SCREEN_HEIGHT,SCREEN_WIDTH
#setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.Rect((0,0),(SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
tank1 = classes.Tank(SCREEN_WIDTH/3,SCREEN_HEIGHT/2,screen)
tank2 = classes.Tank(SCREEN_WIDTH*2/3,SCREEN_HEIGHT/2,screen)
tank2.frame_colour = (202, 161, 196)
tank2.roof_colour = (124, 150, 172)
tank2.lid_colour = (135, 121, 148)
tank2.barrel_original.fill((111, 17, 111))
gamestate = "menu"
shells = []
targets = []
#functions.setup(screen, targets)


#game loop
while running:
    screen.fill((53, 94, 59))

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                shell = classes.Shell(tank1, screen)
                shell.fired = True
                shells.append(shell)
            if event.key == pygame.K_SEMICOLON:
                shell = classes.Shell(tank2,screen)
                shell.fired = True
                shells.append(shell)
        
    functions.event_handling(tank1, tank2, screen, shells)

    #update

    #game rendering here
    
    #drawing stuff
    if gamestate == "menu":
        nextState = functions.drawMenu(screen, running)
        if(nextState == "single player"):
            gamestate = "play"
        elif(nextState == "multiplayer"):
            gamestate = "play"
        elif(nextState == "controls"):
            gamestate = "play"
        elif nextState == "off":
            running = False
    elif gamestate == "play":
        functions.drawGame(screen, background, tank1, tank2, shells, targets)


    pygame.display.flip() #screen buffering
    clock.tick(60) #fps

pygame.quit()
sys.exit()  