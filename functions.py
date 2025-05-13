import pygame
import classes
import random
from globals import SCREEN_WIDTH, SCREEN_HEIGHT

def event_handling(tank1, tank2, screen, shells):
    keys = pygame.key.get_pressed()

    tank1_x_delta = 0
    tank1_y_delta = 0
    tank2_x_delta = 0
    tank2_y_delta = 0
    
    if keys[pygame.K_w]:
        tank1.direction = "up"
        tank1_y_delta = -2
    elif keys[pygame.K_s]:
        tank1.direction = "down"
        tank1_y_delta = 2
    elif keys[pygame.K_a]:
        tank1.direction = "left"
        tank1_x_delta = -2
    elif keys[pygame.K_d]:
        tank1.direction = "right"
        tank1_x_delta = 2
    elif keys[pygame.K_e]:
        tank1.rotate(1)
    elif keys[pygame.K_q]:
        tank1.rotate(-1)
    
    if keys[pygame.K_i]:
        tank2.direction = "up"
        tank2_y_delta = -2
    elif keys[pygame.K_k]:
        tank2.direction = "down"
        tank2_y_delta = 2
    elif keys[pygame.K_j]:
        tank2.direction = "left"
        tank2_x_delta = -2
    elif keys[pygame.K_l]:
        tank2.direction = "right"
        tank2_x_delta = 2
    elif keys[pygame.K_o]:
        tank2.rotate(1)
    elif keys[pygame.K_u]:
        tank2.rotate(-1)

    moveBounds1 = tank1.x + tank1_x_delta + tank1.frame_width/2 < SCREEN_WIDTH and tank1.x + tank1_x_delta - tank1.frame_width/2 > 0 and tank1.y + tank1_y_delta + tank1.frame_height/2 < SCREEN_HEIGHT and tank1.y + tank1_y_delta - tank1.frame_height/2 > 0
    if moveBounds1:
        tank1.move(tank1_x_delta,tank1_y_delta)
        tank1.update()  

    moveBounds2 = tank2.x + tank2_x_delta + tank2.frame_width/2 < SCREEN_WIDTH and tank2.x + tank2_x_delta - tank2.frame_width/2 > 0 and tank2.y + tank2_y_delta + tank2.frame_height/2 < SCREEN_HEIGHT and tank2.y + tank2_y_delta - tank2.frame_height/2 > 0
    if moveBounds2:
        tank2.move(tank2_x_delta,tank2_y_delta)
        tank2.update()  

def setup(screen, targets):
    for targetIndex in range (50):
        x = random.randint(0,SCREEN_WIDTH)
        y = random.randint(0,SCREEN_HEIGHT)
        target = classes.Target(x,y,screen)
        targets.append(target)

def drawMenu(screen, running):
    font = pygame.font.SysFont(None, 40)  # None uses default font, 40 is font size
    font_colour = (144, 238, 144)

    single_player_button = font.render("Single Player", True, font_colour)  # White text
    multiplayer_button = font.render("Multi Player", True, font_colour)  # White text
    controls_button = font.render("Controls", True, font_colour)  # White text

    singlePlayerRect = single_player_button.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + single_player_button.get_height()/2))
    multiPlayerRect = multiplayer_button.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2+single_player_button.get_height() + 10 + multiplayer_button.get_height()/2))
    controlRect = controls_button.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + single_player_button.get_height() + 10 + multiplayer_button.get_height() + 10 + controls_button.get_height()/2))


    mousePos = pygame.mouse.get_pos()
    spHover = singlePlayerRect.collidepoint(mousePos)
    mpHover = multiPlayerRect.collidepoint(mousePos)
    coHover = controlRect.collidepoint(mousePos)
    if(spHover):
        single_player_button = font.render("Single Player", True, (255,255,255))
    if(mpHover):
        multiplayer_button = font.render("Multi Player", True, (255,255,255))
    if(coHover):
        controls_button = font.render("Controls", True, (255,255,255))

    logo = pygame.image.load("resources/logo.png")
    logo = pygame.transform.scale(logo, (logo.get_width()/2,logo.get_height()/2))

    screen.blit(logo,(SCREEN_WIDTH/2 - logo.get_width()/2, SCREEN_HEIGHT/10 - 100))
    screen.blit(single_player_button, (SCREEN_WIDTH/2 - single_player_button.get_width()/2,SCREEN_HEIGHT/2))  # Draw text at position (100, 100)
    screen.blit(multiplayer_button, (SCREEN_WIDTH/2 - multiplayer_button.get_width()/2,SCREEN_HEIGHT/2+single_player_button.get_height() + 10))  # Draw text at position (100, 100)
    screen.blit(controls_button, (SCREEN_WIDTH/2 - controls_button.get_width()/2,SCREEN_HEIGHT/2 + single_player_button.get_height() + 10 + multiplayer_button.get_height() + 10))  # Draw text at position (100, 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "off"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if spHover:
                return "single player"
            elif mpHover:
                return "multiplayer"
            elif coHover:
                return "controls"
    
    return "nothing"

def drawGame(screen, background, tank1, tank2, shells, targets):
    pygame.draw.rect(screen,(211,211,211),background) #background

    tank1.draw(screen) #tanks
    tank2.draw(screen)

    for shell in shells: #shells
        if(shell.fired):
            for target in targets:
                #single player mode
                if shell.shell_rect.colliderect(target.target):
                    shell.fired = False
                    shell.collided = True
                    target.hit = True
            
            if shell.shell_rect.colliderect(tank1.frame):
                tank1.intact = False
                shell.fired = False
                shell.collided = True
            if shell.shell_rect.colliderect(tank2.frame):
                tank2.intact = False
                shell.fired = False
                shell.collided = False
            
            shell.move()
            shell.draw()
        else:
            shells.remove(shell)
    
    for target in targets:
        if(not target.hit):
            target.draw()
        else:
            targets.remove(target)
