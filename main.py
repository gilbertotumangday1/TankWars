#import modules
import pygame
import sys

#globals
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
TEXT_SIZE = 30
#setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update
    screen.fill((0, 0, 0))

    #game rendering here
    font = pygame.font.SysFont('Arial', TEXT_SIZE)
    text = font.render("Hello!", True, (255,255,255))
    
    #draw
    screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
    pygame.display.flip() #screen buffering
    clock.tick(60) #fps

pygame.quit()
sys.exit()