import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
screen_width, screen_height = 800, 210
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer Game")

# Define colors
background_color = (255,192,203)  # Pink
platform_color = (34,139,34) # green
block_color = platform_color # dark green


# Frame rate control
clock = pygame.time.Clock()


# Player setup
player_width, player_height = 20, 20  # Rectangle dimensions
player_speed = 5  # Speed of movement
player_color = (255, 0, 0)  # Red
gravity = 1.3

platform_width, platform_height = 50, 10
harm_width, harm_height = 60, 20
#Game setup
level = 1
startx = 20
starty = screen_height - 20

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("player.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (player_width, player_height))  # resize if needed
        #self.rect = self.image.get_rect()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(player_color)  
        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty
        self.movex = 0
        self.movey = 0
        self.on_ground = False

    def setCoord(self, xloc, yloc):
        self.rect.x = xloc
        self.rect.y = yloc

    def apply_gravity(self):
        if not self.on_ground:
          self.movey += gravity
      
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
          self.movey = -14
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
    
    def collide_blocks(self, blocks, axis):
      hits = pygame.sprite.spritecollide(self, blocks, False)
      if hits:
        block = hits[0]
        if axis == 'y':
            if self.movey > 0:
                self.rect.bottom = block.rect.top
                self.movey = 0
                self.on_ground = True
            elif self.movey < 0:
                self.rect.top = block.rect.bottom
                self.movey = 0
        elif axis == 'x':
            if self.movex > 0:
                self.rect.right = block.rect.left
                self.movex = 0
            elif self.movex < 0:
                self.rect.left = block.rect.right
                self.movex = 0

    
    def hitHarm(self, harmList):
      hits = pygame.sprite.spritecollide(self, harmList, False)
      if hits:
        self.rect.x = startx
        self.rect.y = starty

    def update(self, platforms, harmList, blocks):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.movex = -player_speed
        elif keys[pygame.K_RIGHT]:
            self.movex = player_speed
        else:
            self.movex = 0

        self.rect.y += self.movey
        self.collide_platforms(platforms)
        self.collide_blocks(blocks, 'y')  # y axis only        
        self.apply_gravity()
        
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump()

        self.rect.x += self.movex
        self.collide_blocks(blocks, 'x')  # x axis only
        #self.rect.y += self.movey #its above now

        #check if hit harm
        self.hitHarm(harmList)
        # Clamp to screen edges
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(screen_width, self.rect.right)



class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, width=platform_width, height=platform_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(platform_color) 
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
    def setCoord(self, xloc, yloc, width=platform_width, height=platform_height):
        self.rect.x = xloc
        self.rect.y = yloc

class Block(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, width=40, height=40):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(block_color) 
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
    def setCoord(self, xloc, yloc, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc



class HarmObject(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, width=harm_width, height=harm_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("3Triangles.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))  # resize if needed
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
    def setCoord(self, xloc, yloc):
        self.rect.x = xloc
        self.rect.y = yloc

class Key(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, width=10, height=10):
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
harm1 = HarmObject(-200,0)
harm2 = HarmObject(-200,0)
harm3 = HarmObject(-200,0)
harm4 = HarmObject(-200,0)
harm5 = HarmObject(-200,0)
harm6 = HarmObject(-200,0)
block1 = Block(-200,0)
block2 = Block(-200,0)
block3 = Block(-200,0)
keyList = pygame.sprite.Group(key)
harmList = pygame.sprite.Group(harm1, harm2, harm3, harm4, harm5, harm6)
platforms = pygame.sprite.Group(platform1, platform2, platform3,platform4,platform5,platform6)
blocks = pygame.sprite.Group(block1, block2, block3)

all_sprites = pygame.sprite.Group(player)
all_sprites.add(platform1, platform2, platform3,platform4,platform5,platform6)
all_sprites.add(harm1, harm2, harm3, harm4, harm5, harm6)
all_sprites.add(block1, block2, block3)
all_sprites.add(key)



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
      platform1.setCoord(200,140)
      platform2.setCoord(570,110)
      platform3.setCoord(710,80, 60, 10)
      harm1.setCoord(340, 150)
      harm2.setCoord(510, 190)
      harm3.setCoord(570, 190)
      harm4.setCoord(630, 190)
      harm5.setCoord(690, 190)
      harm6.setCoord(750, 190)
      block1.setCoord(290, 120, 50,90)
      block2.setCoord(340, 170, 60, 40)
      block3.setCoord(400, 130, 110, 80)
      key.setCoord(730, 60)
      levelUpdated = True
    elif level == 2:
      platform1.setCoord(200,500)
      platform2.setCoord(400,400)
      platform3.setCoord(600,300)
      platform4.setCoord(900,100)
      levelUpdated = True

    ###
    player.update(platforms, harmList, blocks)

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
