import pygame
import math
from globals import SCREEN_HEIGHT, SCREEN_WIDTH

class Tank:
    def __init__(self, tank_x, tank_y, background):
        self.direction = "up"
        self.intact = True
        self.x = tank_x
        self.y = tank_y

        self.frame_surface = background
        self.roof_surface = background
        self.lid_surface = background

        self.frame_colour = (53, 94, 59)
        self.roof_colour = (131, 105, 83)
        self.lid_colour = (144, 238, 144)
        self.lid_radius = 15

        self.frame_width = 40
        self.frame_height = 80
        self.roof_width = 30
        self.roof_height = 50

        self.lid_center = (self.x, self.y)
        self.frame = pygame.Rect(0, 0, 0, 0)
        self.roof = pygame.Rect(0, 0, 0, 0)

        self.barrel_width = 10
        self.barrel_height = 60
        self.barrel_angle = 0
        self.barrel_original = pygame.Surface((self.barrel_width, self.barrel_height), pygame.SRCALPHA)
        self.barrel_original.fill((120, 134, 107))
        self.barrel_pivot_offset = pygame.math.Vector2(0, self.barrel_height / 2)
        self.barrel = self.barrel_original
        self.barrel_rect = self.barrel.get_rect()
        self.barrel_tip = pygame.Rect(0, 0, 4, 4)

        self.update()

    def move(self, tank_offset_x, tank_offset_y, walls):
        next_x = self.x + tank_offset_x
        next_y = self.y + tank_offset_y

        temp_frame = pygame.Rect(next_x - self.frame_width / 2, next_y - self.frame_height / 2,
                                 self.frame_width, self.frame_height)

        tip_offset = pygame.math.Vector2(0, self.barrel_height / 2).rotate(self.barrel_angle)
        temp_barrel_center = (next_x - tip_offset.x, next_y - tip_offset.y)
        temp_barrel_rect = self.barrel.get_rect(center=temp_barrel_center)

        if not any(temp_frame.colliderect(wall.target) or temp_barrel_rect.colliderect(wall.target)
                   for wall in walls):
            self.x = next_x
            self.y = next_y
            self.update()

    def can_rotate(self, new_direction, walls):
        old_direction = self.direction
        old_frame = self.frame.copy()
        old_roof = self.roof.copy()
        old_lid_center = self.lid_center

        self.direction = new_direction
        self.update()

        for wall in walls:
            if self.frame.colliderect(wall.target) or self.roof.colliderect(wall.target) or wall.target.collidepoint(self.lid_center):
                self.direction = old_direction
                self.frame = old_frame
                self.roof = old_roof
                self.lid_center = old_lid_center
                self.update()
                return False

        return True

    def rotate(self, tank_offset_angle, walls):
        original_angle = self.barrel_angle
        self.barrel_angle += tank_offset_angle
        self._apply_barrel_transform()

        tip_x = self.lid_center[0] + math.sin(math.radians(self.barrel_angle)) * self.barrel_height
        tip_y = self.lid_center[1] - math.cos(math.radians(self.barrel_angle)) * self.barrel_height
        tip_rect = pygame.Rect(tip_x - 2, tip_y - 2, 4, 4)

        if any(tip_rect.colliderect(wall.target) for wall in walls):
            self.barrel_angle = original_angle
            self._apply_barrel_transform()
            tip_x = self.lid_center[0] + math.sin(math.radians(self.barrel_angle)) * self.barrel_height
            tip_y = self.lid_center[1] - math.cos(math.radians(self.barrel_angle)) * self.barrel_height
            self.barrel_tip = pygame.Rect(tip_x - 2, tip_y - 2, 4, 4)
        else:
            self.barrel_tip = tip_rect

    def _apply_barrel_transform(self):
        self.barrel = pygame.transform.rotate(self.barrel_original, -self.barrel_angle)
        offset_rotated = self.barrel_pivot_offset.rotate(self.barrel_angle)
        self.barrel_rect = self.barrel.get_rect(center=(self.x - offset_rotated.x, self.y - offset_rotated.y))

    def update(self):
        if self.direction == "up":
            self.frame_width, self.frame_height = 40, 80
        elif self.direction == "down":
            self.frame_width, self.frame_height = 40, 80
        elif self.direction == "left":
            self.frame_width, self.frame_height = 80, 40
        elif self.direction == "right":
            self.frame_width, self.frame_height = 80, 40

        self.lid_center = (self.x, self.y)
        self.frame = pygame.Rect(self.x - self.frame_width / 2, self.y - self.frame_height / 2,
                                 self.frame_width, self.frame_height)
        self.roof = pygame.Rect(self.x - self.roof_width / 2, self.y - self.roof_height / 2,
                                self.roof_width, self.roof_height)
        self._apply_barrel_transform()
        tip_x = self.lid_center[0] + math.sin(math.radians(self.barrel_angle)) * self.barrel_height
        tip_y = self.lid_center[1] - math.cos(math.radians(self.barrel_angle)) * self.barrel_height
        self.barrel_tip = pygame.Rect(tip_x - 2, tip_y - 2, 4, 4)

    def draw(self, screen):
        if self.intact:
            pygame.draw.rect(self.frame_surface, self.frame_colour, self.frame)
            pygame.draw.rect(self.roof_surface, self.roof_colour, self.roof)
            pygame.draw.circle(self.lid_surface, self.lid_colour, self.lid_center, self.lid_radius)
            screen.blit(self.barrel, self.barrel_rect.topleft)
            # Optional: draw barrel tip for debug
            # pygame.draw.rect(screen, (255, 0, 0), self.barrel_tip)


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

    


