import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer Game")

# Define colors
background_color = (0, 0, 0)  # Black
platform_color = (0,255,0) # green

# Frame rate control
clock = pygame.time.Clock()


# Player setup
player_width, player_height = 20, 20  # Rectangle dimensions
player_x = 50
player_y = 30
player_speed = 10  # Speed of movement
player_color = (0, 255, 0)  # Green
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)  # Create the rectangle
speed = [1, 1]
gravity = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("player.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (player_width, player_height))  # resize if needed
        #self.rect = self.image.get_rect()
        self.image = pygame.Surface((20, 20))
        self.image.fill((139, 69, 19))  # Brown color
        self.rect = self.image.get_rect()
        self.rect.x = (screen_width - player_width) // 2
        self.rect.y = screen_height - 50
        self.movex = 0
        self.movey = 0
        self.on_ground = False


    def apply_gravity(self):
        self.movey += gravity
        self.on_ground = False
        # Stop falling at bottom of screen
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.movey = 0
            self.on_ground = True

    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x
        self.movey += y

    def jump(self):
      if self.on_ground:
          self.movey = -15
          self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.movex = -player_speed
        elif keys[pygame.K_RIGHT]:
            self.movex = player_speed
        else:
            self.movex = 0

        self.apply_gravity()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump()

        self.rect.x += self.movex
        self.rect.y += self.movey

        # Clamp to screen edges
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(screen_width, self.rect.right)


class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, width=100, height=15):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(platform_color) 
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc


player = Player()
all_sprites = pygame.sprite.Group(player)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with the background color
    screen.fill(background_color)

    all_sprites.update()
    all_sprites.draw(screen)


    # Update the display
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

pygame.quit()
