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
shells = []
targets = []
functions.setup(screen, targets)


#game loop
while running:
    #event handling

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                shell = classes.Shell(tank, screen)
                shell.fired = True
                shells.append(shell)
        
        

    functions.event_handling(tank, screen, shells)

    #update
    screen.fill((0, 0, 0))

    #game rendering here
    
    #drawing stuff
    pygame.draw.rect(screen,(211,211,211),background) #backgrounds

    tank.draw(screen) #tanks

    for shell in shells: #shells
        if(shell.fired):
            for target in targets:
                if shell.shell_rect.colliderect(target.target):
                    shell.fired = False
                    shell.collided = True
                    target.hit = True
            shell.move()
            shell.draw()
        else:
            shells.remove(shell)
    
    for target in targets:
        if(not target.hit):
            target.draw()
        else:
            targets.remove(target)


    pygame.display.flip() #screen buffering
    clock.tick(60) #fps

pygame.quit()
sys.exit()  