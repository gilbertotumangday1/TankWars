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
tank = classes.Tank(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,screen)


#game loop
while running:
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    functions.event_handling(tank)

    #update
    screen.fill((0, 0, 0))

    #game rendering here
    
    #draw
    pygame.draw.rect(screen,(211,211,211),background)
    tank.draw(screen)
    pygame.display.flip() #screen buffering
    clock.tick(60) #fps

pygame.quit()
sys.exit()  