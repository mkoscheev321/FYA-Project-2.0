import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
screen_width, screen_height = 1000, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer Game")

# Define colors
background_color = (0, 0, 0)  # Black
platform_color = (0,255,0) # green

# Frame rate control
clock = pygame.time.Clock()


# Player setup
player_width, player_height = 30, 30  # Rectangle dimensions
player_speed = 10  # Speed of movement
player_color = (255, 0, 0)  # Red
gravity = 1

#Game setup
level = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("player.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (player_width, player_height))  # resize if needed
        #self.rect = self.image.get_rect()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(player_color)  
        self.rect = self.image.get_rect()
        self.rect.x = (screen_width - player_width) // 2
        self.rect.y = screen_height - 50
        self.movex = 0
        self.movey = 0
        self.on_ground = False

    def setCoord(self, xloc, yloc):
        self.rect.x = xloc
        self.rect.y = yloc

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

    def collide_platforms(self, platforms):
      hits = pygame.sprite.spritecollide(self, platforms, False)
      if hits:
          if self.movey > 0:  # falling down, land on top
              self.rect.bottom = hits[0].rect.top
              self.movey = 0
              self.on_ground = True
          elif self.movey < 0:  # jumping up, hit the bottom
              self.rect.top = hits[0].rect.bottom
              self.movey = 0
      else:
          if self.rect.bottom < screen_height:  # not on floor either
            self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.movex = -player_speed
        elif keys[pygame.K_RIGHT]:
            self.movex = player_speed
        else:
            self.movex = 0

        self.apply_gravity()

        self.collide_platforms(platforms)
        
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump()

        self.rect.x += self.movex
        self.rect.y += self.movey

        # Clamp to screen edges
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(screen_width, self.rect.right)



class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, width=100, height=20):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(platform_color) 
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
    def setCoord(self, xloc, yloc):
        self.rect.x = xloc
        self.rect.y = yloc

class Key(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, width=40, height=40):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 238, 140)) #yellow
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
    def setCoord(self, xloc, yloc):
        self.rect.x = xloc
        self.rect.y = yloc
player = Player()
key = Key(920, 240)
platform1 = Platform(-200,0)
platform2 = Platform(-200,0)
platform3 = Platform(-200,0)
platform4 = Platform(-200,0)
platform5 = Platform(-200,0)
platform6 = Platform(-200,0)
all_sprites = pygame.sprite.Group(player)
keyList = pygame.sprite.Group(key)
platforms = pygame.sprite.Group(platform1, platform2, platform3,platform4,platform5,platform6)
all_sprites.add(platform1, platform2, platform3,platform4,platform5,platform6)



levelUpdated = False
# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with the background color
    screen.fill(background_color)

    #setup level
    if level == 1:
      platform1.setCoord(200,500)
      platform2.setCoord(400,400)
      platform3.setCoord(600,300)
      platform4.setCoord(900,300)
      levelUpdated = True
    elif level == 2:
      platform1.setCoord(200,500)
      platform2.setCoord(400,400)
      platform3.setCoord(600,300)
      platform4.setCoord(900,100)
      levelUpdated = True

    ###
    player.update(platforms)

    #CHECK level
    hits = pygame.sprite.spritecollide(player, keyList, False)
    if hits:
      level+=1
      levelUpdated = False;

    all_sprites.draw(screen)


    # Update the display
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)
pygame.quit()
