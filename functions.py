import pygame
import classes
from globals import SCREEN_WIDTH, SCREEN_HEIGHT

def event_handling(tank):
    keys = pygame.key.get_pressed()

    tank_x_delta = 0
    tank_y_delta = 0
    if keys[pygame.K_w]:
        tank.direction = "up"
        tank_y_delta = -1
    elif keys[pygame.K_s]:
        tank.direction = "down"
        tank_y_delta = 1
    elif keys[pygame.K_a]:
        tank.direction = "left"
        tank_x_delta = -1
    elif keys[pygame.K_d]:
        tank.direction = "right"
        tank_x_delta = 1
    elif keys[pygame.K_e]:
        tank.rotate(1)
    elif keys[pygame.K_q]:
        tank.rotate(-1)

    moveBounds = tank.x + tank_x_delta + tank.frame_width/2 < SCREEN_WIDTH and tank.x + tank_x_delta - tank.frame_width/2 > 0 and tank.y + tank_y_delta + tank.frame_height/2 < SCREEN_HEIGHT and tank.y + tank_y_delta - tank.frame_height/2 > 0
    if moveBounds:
        tank.move(tank_x_delta,tank_y_delta)
        tank.update()  