import pygame
import classes
import random
from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from map import wall_grid

def event_handling(tank1, tank2, screen, shells, targets):
    keys = pygame.key.get_pressed()

    tank1_x_delta = 0
    tank1_y_delta = 0
    tank2_x_delta = 0
    tank2_y_delta = 0

    # --- TANK 1 INPUTS ---
    if keys[pygame.K_w]:
        if tank1.direction != "up" and tank1.can_rotate("up", targets):
            tank1.direction = "up"
            tank1.update()
        tank1_y_delta = -2
    elif keys[pygame.K_s]:
        if tank1.direction != "down" and tank1.can_rotate("down", targets):
            tank1.direction = "down"
            tank1.update()
        tank1_y_delta = 2
    elif keys[pygame.K_a]:
        if tank1.direction != "left" and tank1.can_rotate("left", targets):
            tank1.direction = "left"
            tank1.update()
        tank1_x_delta = -2
    elif keys[pygame.K_d]:
        if tank1.direction != "right" and tank1.can_rotate("right", targets):
            tank1.direction = "right"
            tank1.update()
        tank1_x_delta = 2
    elif keys[pygame.K_e]:
        tank1.rotate(2, targets)
    elif keys[pygame.K_q]:
        tank1.rotate(-2, targets)

    # --- TANK 2 INPUTS ---
    if keys[pygame.K_i]:
        if tank2.direction != "up" and tank2.can_rotate("up", targets):
            tank2.direction = "up"
            tank2.update()
        tank2_y_delta = -2
    elif keys[pygame.K_k]:
        if tank2.direction != "down" and tank2.can_rotate("down", targets):
            tank2.direction = "down"
            tank2.update()
        tank2_y_delta = 2
    elif keys[pygame.K_j]:
        if tank2.direction != "left" and tank2.can_rotate("left", targets):
            tank2.direction = "left"
            tank2.update()
        tank2_x_delta = -2
    elif keys[pygame.K_l]:
        if tank2.direction != "right" and tank2.can_rotate("right", targets):
            tank2.direction = "right"
            tank2.update()
        tank2_x_delta = 2
    elif keys[pygame.K_o]:
        tank2.rotate(2, targets)
    elif keys[pygame.K_u]:
        tank2.rotate(-2, targets)

    # --- MOVEMENT BOUNDS + COLLISION ---
    moveBounds1 = (tank1.x + tank1_x_delta + tank1.frame_width/2 < SCREEN_WIDTH and 
                   tank1.x + tank1_x_delta - tank1.frame_width/2 > 0 and 
                   tank1.y + tank1_y_delta + tank1.frame_height/2 < SCREEN_HEIGHT and 
                   tank1.y + tank1_y_delta - tank1.frame_height/2 > 0)

    if moveBounds1 and not tank_hits_wall(tank1, tank1_x_delta, tank1_y_delta, targets):
        tank1.move(tank1_x_delta, tank1_y_delta, targets)

    moveBounds2 = (tank2.x + tank2_x_delta + tank2.frame_width/2 < SCREEN_WIDTH and 
                   tank2.x + tank2_x_delta - tank2.frame_width/2 > 0 and 
                   tank2.y + tank2_y_delta + tank2.frame_height/2 < SCREEN_HEIGHT and 
                   tank2.y + tank2_y_delta - tank2.frame_height/2 > 0)

    if moveBounds2 and not tank_hits_wall(tank2, tank2_x_delta, tank2_y_delta, targets):
        tank2.move(tank2_x_delta, tank2_y_delta, targets)

def setup(screen, targets):
    for targetX in range (750):
        for targetY in range (750):
            if(wall_grid[targetX][targetY] == 1):
                x = targetX
                y = targetY
                target = classes.Target(x,y,screen)
                targets.append(target)

def drawMenu(screen, running):

    #writing
    font = pygame.font.SysFont(None, 40)  # None uses default font, 40 is font size
    font_colour = (144, 238, 144)
    single_player_button = font.render("Single Player", True, font_colour)  # White text
    multiplayer_button = font.render("Multi Player", True, font_colour)  # White text
    controls_button = font.render("Controls", True, font_colour)  # White text

    #clickable rects for the words
    singlePlayerRect = single_player_button.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + single_player_button.get_height()/2))
    multiPlayerRect = multiplayer_button.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2+single_player_button.get_height() + 10 + multiplayer_button.get_height()/2))
    controlRect = controls_button.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + single_player_button.get_height() + 10 + multiplayer_button.get_height() + 10 + controls_button.get_height()/2))

    #handle clicks
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

    #draw everything onto screen
    logo = pygame.image.load("resources/logo.png")
    logo = pygame.transform.scale(logo, (logo.get_width()/2,logo.get_height()/2))
    screen.blit(logo,(SCREEN_WIDTH/2 - logo.get_width()/2, SCREEN_HEIGHT/10 - 100))
    screen.blit(single_player_button, (SCREEN_WIDTH/2 - single_player_button.get_width()/2,SCREEN_HEIGHT/2))  # Draw text at position (100, 100)
    screen.blit(multiplayer_button, (SCREEN_WIDTH/2 - multiplayer_button.get_width()/2,SCREEN_HEIGHT/2+single_player_button.get_height() + 10))  # Draw text at position (100, 100)
    screen.blit(controls_button, (SCREEN_WIDTH/2 - controls_button.get_width()/2,SCREEN_HEIGHT/2 + single_player_button.get_height() + 10 + multiplayer_button.get_height() + 10))  # Draw text at position (100, 100)

    #event handling
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
    
    #default case
    return "nothing"

def drawGame(screen, background, tank1, tank2, shells, targets, gamestate):
    font = pygame.font.SysFont(None, 40)  # None uses default font, 40 is font size
    font_colour = (255, 0, 0)
    goalText = font.render("Eliminate the opposing tank.", True, font_colour)

    #draw the background
    pygame.draw.rect(screen,(211,211,211),background)

    #draw the tanks
    tank1.draw(screen)
    tank2.draw(screen)

    #draw shells
    for shell in shells:
        if(shell.fired):
            #targets (single player mode)
            for target in targets:
                if shell.shell_rect.colliderect(target.target):
                    shell.fired = False
                    shell.collided = True
                    target.hit = True
            #shell tank collisions
            if shell.shell_rect.colliderect(tank1.frame):
                tank1.intact = False
                shell.fired = False
                shell.collided = True
                gamestate = "tank 2 won"
            if shell.shell_rect.colliderect(tank2.frame):
                tank2.intact = False
                shell.fired = False
                shell.collided = False
                gamestate = "tank 1 won"
            
            #update and draw shells
            shell.move()
            shell.draw()
        else:
            shells.remove(shell)
    
    #targets (single player mode)
    for target in targets:
        if(not target.hit):
            target.draw()
        else:
            targets.remove(target)
    
    #draw text
    screen.blit(goalText, (SCREEN_WIDTH/2 - goalText.get_width()/2, 20))

    return gamestate

def drawEndGame(screen, running, winner):
    #writing
    font = pygame.font.SysFont(None, 40)  # None uses default font, 40 is font size
    font_colour = (144, 238, 144)

    restart_game_button = font.render("Restart", True, font_colour)  # White text
    menu_button = font.render("Menu", True, font_colour)  # White text
    winFont = pygame.font.SysFont(None, 100)
    if(winner == 1):
        winText = winFont.render("Tank 1 wins!", True, (255,0,0))
    elif(winner == 2):
        winText = winFont.render("Tank 2 wins!", True, (255,0,0))

    #clickable rects for the words
    restartRect = restart_game_button.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + restart_game_button.get_height()/2 + 50))
    menuRect = menu_button.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2+restart_game_button.get_height() + 10 + menu_button.get_height()/2 + 50))

    #handle clicks
    mousePos = pygame.mouse.get_pos()
    restartHover = restartRect.collidepoint(mousePos)
    menuHover = menuRect.collidepoint(mousePos)
    if(restartHover):
        restart_game_button = font.render("Restart", True, (255,255,255))
    if(menuHover):
        menu_button = font.render("Menu", True, (255,255,255))

    #draw everything onto screen
    over = pygame.image.load("resources/gameover.png")
    over = pygame.transform.scale(over, (over.get_width()/2,over.get_height()/2))
    screen.blit(over,(SCREEN_WIDTH/2 - over.get_width()/2, SCREEN_HEIGHT/10 - 100))
    screen.blit(restart_game_button, (SCREEN_WIDTH/2 - restart_game_button.get_width()/2,SCREEN_HEIGHT/2 + 50))  # Draw text at position (100, 100)
    screen.blit(menu_button, (SCREEN_WIDTH/2 - menu_button.get_width()/2,SCREEN_HEIGHT/2+restart_game_button.get_height() + 10 + 50))  # Draw text at position (100, 100)
    screen.blit(winText, (SCREEN_WIDTH/2 - winText.get_width()/2, SCREEN_HEIGHT - 100 - winText.get_height()))

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "off"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if restartHover:
                return "restart"
            elif menuHover:
                return "menu"
    
    #default case
    return "nothing"

def tank_hits_wall(tank, dx, dy, targets):
    future_frame = tank.frame.move(dx, dy)
    for target in targets:
        if future_frame.colliderect(target.target):
            return True
    return False
