import pygame


class Tank:
    def __init__(self, tank_x, tank_y, background):
        self.direction = "up"
        self.intact = True
        self.x = tank_x
        self.y = tank_y
        self.frame_width = 40
        self.frame_height = 80
        self.frame_colour = (53,94,59)
        self.frame_surface = background
        self.frame = pygame.Rect(self.x - self.frame_width/2, self.y - self.frame_height/2, self.frame_width, self.frame_height)
        self.lid_radius = 15
        self.lid_colour = (144, 238, 144)
        self.lid_center = (self.x, self.y + 10)
        self.lid_surface = background
        self.barrel_width = 10
        self.barrel_height = 60
        self.barrel_x = self.x - self.barrel_width/2
        self.barrel_y = self.y + 10 - self.barrel_width/2
        self.barrel_original = pygame.Surface((self.barrel_width, self.barrel_height), pygame.SRCALPHA)
        self.barrel_original.fill((120, 134, 107))
        self.barrel_angle = 0  # in degrees
        self.barrel = self.barrel_original
        self.barrel_rect = self.barrel.get_rect(center=self.lid_center)
    
    def move(self, tank_offset_x, tank_offset_y):
        self.x += tank_offset_x
        self.y += tank_offset_y

    def rotate(self, tank_offset_angle):
        self.barrel_angle += tank_offset_angle
        self.barrel = pygame.transform.rotate(self.barrel_original, -self.barrel_angle)  # negative for clockwise
        self.barrel_rect = self.barrel.get_rect(center=self.lid_center)

    def update(self):
        if self.direction == "up":
            self.frame_width = 40
            self.frame_height = 80
            self.lid_center = (self.x, self.y + 10)
            self.barrel_x = self.x - self.barrel_width/2
            self.barrel_y = self.y + 10 - self.barrel_width/2
        elif self.direction == "down":
            self.frame_width = 40
            self.frame_height = 80
            self.lid_center = (self.x, self.y - 10)
            self.barrel_x = self.x - self.barrel_width/2
            self.barrel_y = self.y - 10 - self.barrel_width/2
        elif self.direction == "left":
            self.frame_width = 80
            self.frame_height = 40
            self.lid_center = (self.x + 10, self.y)
            self.barrel_x = self.x - self.barrel_width/2 + 10
            self.barrel_y = self.y - self.barrel_width/2
        elif self.direction == "right":
            self.frame_width = 80
            self.frame_height = 40
            self.lid_center = (self.x - 10, self.y)
            self.barrel_x = self.x - self.barrel_width/2 - 10
            self.barrel_y = self.y - self.barrel_width/2

        self.frame = pygame.Rect(self.x - self.frame_width/2, self.y - self.frame_height/2, self.frame_width, self.frame_height)
        self.barrel_rect = self.barrel.get_rect(center=self.lid_center)

    def draw(self, screen):
        pygame.draw.rect(self.frame_surface,self.frame_colour,self.frame)
        pygame.draw.circle(self.lid_surface,self.lid_colour,self.lid_center,self.lid_radius)
        screen.blit(self.barrel, self.barrel_rect.topleft)


