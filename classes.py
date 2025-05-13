import pygame
import math
from globals import SCREEN_HEIGHT,SCREEN_WIDTH


class Tank:
    def __init__(self, tank_x, tank_y, background):
        #general info
        self.direction = "up"
        self.intact = True
        self.x = tank_x
        self.y = tank_y
        
        #frame
        self.frame_width = 40
        self.frame_height = 80
        self.frame_colour = (53, 94, 59)
        self.frame_surface = background
        self.frame = pygame.Rect(self.x - self.frame_width / 2, self.y - self.frame_height / 2, self.frame_width, self.frame_height)

        #roof
        self.roof_width = 30
        self.roof_height = 50
        self.roof_colour = (131,105,83)
        self.roof_surface = background
        self.roof = pygame.Rect(self.x - self.roof_width/2, self.y - self.roof_height/2 + 10 , self.roof_width , self.roof_height)

        #lid
        self.lid_radius = 15
        self.lid_colour = (144, 238, 144)
        self.lid_center = (self.x, self.y + 10)
        self.lid_surface = background

        #barrel
        self.barrel_width = 10
        self.barrel_height = 60
        self.barrel_angle = 0  # degrees
        self.barrel_original = pygame.Surface((self.barrel_width, self.barrel_height), pygame.SRCALPHA)
        self.barrel_original.fill((120, 134, 107))
        self.barrel_pivot_offset = pygame.math.Vector2(0, self.barrel_height/2)  # Pivot at bottom center
        self.barrel = self.barrel_original
        self.barrel_rect = self.barrel.get_rect()
    
    def move(self, tank_offset_x, tank_offset_y):
        self.x += tank_offset_x
        self.y += tank_offset_y

    def rotate(self, tank_offset_angle):
        self.barrel_angle += tank_offset_angle

        # Rotate the image
        self.barrel = pygame.transform.rotate(self.barrel_original, -self.barrel_angle)

        # Rotate offset vector
        offset_rotated = self.barrel_pivot_offset.rotate(self.barrel_angle)

        # Set new rect to keep pivot at lid center
        self.barrel_rect = self.barrel.get_rect(center=(self.lid_center[0] - offset_rotated.x,
                                                        self.lid_center[1] - offset_rotated.y))

    def update(self):
        if self.direction == "up":
            self.frame_width = 40
            self.frame_height = 80
            self.roof_width = 30
            self.roof_height = 50
            self.lid_center = (self.x, self.y + 10)
            self.roof = pygame.Rect(self.x - self.roof_width/2, self.y - self.roof_height/2 + 10, self.roof_width , self.roof_height)
        elif self.direction == "down":
            self.frame_width = 40
            self.frame_height = 80
            self.roof_width = 30
            self.roof_height = 50
            self.lid_center = (self.x, self.y - 10)
            self.roof = pygame.Rect(self.x - self.roof_width/2, self.y - self.roof_height/2 -10, self.roof_width , self.roof_height)
        elif self.direction == "left":
            self.frame_width = 80
            self.frame_height = 40
            self.roof_width = 50
            self.roof_height = 30
            self.lid_center = (self.x + 10, self.y)
            self.roof = pygame.Rect(self.x - self.roof_width/2 + 10, self.y - self.roof_height/2 , self.roof_width , self.roof_height)
        elif self.direction == "right":
            self.frame_width = 80
            self.frame_height = 40
            self.roof_width = 50
            self.roof_height = 30
            self.lid_center = (self.x - 10, self.y)
            self.roof = pygame.Rect(self.x - self.roof_width/2 - 10, self.y - self.roof_height/2 , self.roof_width , self.roof_height)

        self.frame = pygame.Rect(self.x - self.frame_width / 2, self.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.rotate(0)  # Refresh barrel position

    def draw(self, screen):
        if(self.intact):
            pygame.draw.rect(self.frame_surface, self.frame_colour, self.frame)
            pygame.draw.rect(self.roof_surface, self.roof_colour, self.roof)
            pygame.draw.circle(self.lid_surface, self.lid_colour, self.lid_center, self.lid_radius)
            screen.blit(self.barrel, self.barrel_rect.topleft)

class Shell:
    def __init__(self, source_tank, background):
        #general info
        self.fired = False
        self.collided = False
        self.velocity = 5

        #get starting x and y position
        angle_rad = math.radians(source_tank.barrel_angle)
        self.x = source_tank.lid_center[0] + math.sin(angle_rad) * source_tank.barrel_height
        self.y = source_tank.lid_center[1] + math.cos(angle_rad) * -source_tank.barrel_height

        #get travel direction slope
        self.dir_x = math.sin(angle_rad)
        self.dir_y = -math.cos(angle_rad)

        #shell dimensions
        self.shell_width = 5
        self.shell_height = 10
        
        #more shell info
        self.shell_surface = background
        self.shell_colour = (0,0,0)
        self.shell_original = pygame.Surface((self.shell_height, self.shell_width), pygame.SRCALPHA)
        self.shell_original.fill(self.shell_colour)
        self.angle_deg = math.degrees(math.atan2(self.dir_y, self.dir_x))
        self.shell = pygame.transform.rotate(self.shell_original, -self.angle_deg)
        self.shell_rect = self.shell.get_rect(center=(self.x, self.y))
        

    def move(self):
        deltax = self.dir_x * self.velocity
        deltay = self.dir_y * self.velocity

        if (0 < self.x + deltax < SCREEN_WIDTH) and (0 < self.y + deltay < SCREEN_HEIGHT):
            self.x += deltax
            self.y += deltay
        else:
            self.fired = False

        # Recalculate rect to match new center
        self.shell_rect = self.shell.get_rect(center=(self.x, self.y))

    
    def draw(self):
        self.shell_surface.blit(self.shell, self.shell_rect)

class Target:
    def __init__(self, target_x, target_y, background):
        self.hit = False
        self.x = target_x
        self.y = target_y
        self.target_width = 10
        self.target_height = 10
        self.target_colour = (100,100,100)
        self.target = pygame.Rect(target_x, target_y, self.target_width, self.target_height)
        self.target_surface = background
    
    def draw(self):
        pygame.draw.rect(self.target_surface, self.target_colour, self.target)

    


