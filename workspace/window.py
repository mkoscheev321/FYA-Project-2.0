import pygame
import random
import os


# Initializing
pygame.init()
<<<<<<< HEAD
font = pygame.font.Font(None, 36)
GOLD = (255, 215, 0)

try:
    pygame.mixer.init()
    pygame.mixer.music.load("cutemusic.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.5)
except pygame.error:
    pass  # No audio device, just skip music
=======
pygame.mixer.init()

font = pygame.font.Font(None, 36)
GOLD = (255, 215, 0)


#loading music file 
pygame.mixer.music.load("cutemusic.mp3")

pygame.mixer.music.play(-1)

#set music volume 
pygame.mixer.music.set_volume(.5)
>>>>>>> 08e8d2c46462b23579f5112116e8860d9763df1f

# Frame rate
clock = pygame.time.Clock()
FPS = 70

# Window size, color/background and name variables
screen_width = 800
screen_height = 210
window_name = "cool"

gameIsRunning = True
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(window_name)

pygame.display.flip()

# Parallax setup
scroll = 0

#ground_image = pygame.image.load("ground.png").convert_alpha()
ground_image = pygame.image.load("skyground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []
for i in range(1, 3):
    bg_image = pygame.image.load(f"skylyr-{i}.png").convert_alpha()
    bg_images.append(bg_image)

# Find width
bg_width = bg_images[0].get_width()


def draw_bg():
    for x in range(3):
        speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.2


def draw_ground():
    for x in range(15):
        screen.blit(ground_image, ((x * ground_width) - scroll * 2.2, screen_height - ground_height))


# Define colors
background_color = (255, 192, 203)  # Pink
platform_color = (94, 181, 36)      # Green
block_color = platform_color        # Dark green

# Frame rate control
clock = pygame.time.Clock()

# Player setup
player_width, player_height = 20, 40
player_speed = 5
player_color = (0, 255, 0)  # Red
gravity = 1.3

platform_width, platform_height = 50, 10
harm_width, harm_height = 60, 20

# Game setup
level = 0
startx = 20
starty = screen_height - 20


class Player(pygame.sprite.Sprite):
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load("flower1.png").convert_alpha()
       self.image = pygame.transform.scale(self.image, (player_width, player_height))  # resize if needed
       #self.image = pygame.Surface((player_width, player_height))
       #self.image.fill(player_color) 
       self.rect = self.image.get_rect()
       self.rect.x = startx
       self.rect.y = starty
       self.movex = 0
       self.movey = 0
       self.on_ground = False

    def changeImage(self):
      global level
      self.image = pygame.image.load(f"flower{level}.png").convert_alpha()
      self.image = pygame.transform.scale(self.image, (player_width, player_height))  # resize if needed
      self.rect = self.image.get_rect()

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
        """Control player movement."""
        self.movex += x
        self.movey += y

    def jump(self):
        if self.on_ground:
            self.movey = -14
            self.on_ground = False

    def collide_platforms(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.movey > 0:  # Falling down, land on top
                self.rect.bottom = hits[0].rect.top
                self.movey = 0
                self.on_ground = True
            elif self.movey < 0:  # Jumping up, hit the bottom
                self.rect.top = hits[0].rect.bottom
                self.movey = 0
        else:
            if self.rect.bottom < screen_height:
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
        global scroll
        hits = pygame.sprite.spritecollide(self, harmList, False)
        if hits:
            self.rect.x = startx
            self.rect.y = starty
            scroll = 0
    def playerReset(self):
      global scroll
      self.rect.x = startx
      self.rect.y = starty
      scroll = 0

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
        self.collide_blocks(blocks, 'y')
        self.apply_gravity()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump()

        self.rect.x += self.movex
        self.collide_blocks(blocks, 'x')

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
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc

    def setCoord(self, xloc, yloc):
        self.rect.x = xloc
        self.rect.y = yloc
    def setTwo(self):
      self.image = pygame.image.load("2Triangles.png").convert_alpha()
      self.image = pygame.transform.scale(self.image, (harm_width/3*2, harm_height))
      self.rect = self.image.get_rect()
    def setFlipped(self):
      self.image = pygame.image.load("FlippedTriangles.png").convert_alpha()
      self.image = pygame.transform.scale(self.image, (harm_width, harm_height))
      self.rect = self.image.get_rect()


class Key(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, width=20, height=20):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("key1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        #self.image = pygame.Surface((width, height))
        #self.image.fill((255, 238, 140))  # Yellow
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc

    def setCoord(self, xloc, yloc):
        self.rect.x = xloc
        self.rect.y = yloc

    def changeImage(self):
      global level
      self.image = pygame.image.load(f"key{level}.png").convert_alpha()
      self.image = pygame.transform.scale(self.image, (20, 20))  # resize if needed
      self.rect = self.image.get_rect()

class startImage(pygame.sprite.Sprite):
    def __init__(self, xloc = 0, yloc = -500, width=800, height=210):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("startImage.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        #self.image = pygame.Surface((width, height))
        #self.image.fill((255, 238, 140))  # Yellow
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
    def setCoord(self, xloc, yloc):
        self.rect.x = xloc
        self.rect.y = yloc

class endGame(pygame.sprite.Sprite):
    def __init__(self, xloc = 0, yloc = -500, width=800, height=210):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("endGame.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        #self.image = pygame.Surface((width, height))
        #self.image.fill((255, 238, 140))  # Yellow
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc
    def setCoord(self, xloc, yloc):
        self.rect.x = xloc
        self.rect.y = yloc




# Sprite instantiation
startImage = startImage()
endImage = endGame()
player = Player()
key = Key(920, 240)
platform1 = Platform(-200, 0)
platform2 = Platform(-200, 0)
platform3 = Platform(-200, 0)
platform4 = Platform(-200, 0)
platform5 = Platform(-200, 0)
platform6 = Platform(-200, 0)
harm1 = HarmObject(-200, 0)
harm2 = HarmObject(-200, 0)
harm3 = HarmObject(-200, 0)
harm4 = HarmObject(-200, 0)
harm5 = HarmObject(-200, 0)
harm6 = HarmObject(-200, 0)
harm7 = HarmObject(-200, 0)
harm8 = HarmObject(-200, 0)
harm9 = HarmObject(-200, 0)
block1 = Block(-200, 0)
block2 = Block(-200, 0)
block3 = Block(-200, 0)

keyList = pygame.sprite.Group(key)
harmList = pygame.sprite.Group(harm1, harm2, harm3, harm4, harm5, harm6, harm7, harm8, harm9)
platforms = pygame.sprite.Group(platform1, platform2, platform3, platform4, platform5, platform6)
blocks = pygame.sprite.Group(block1, block2, block3)

all_sprites = pygame.sprite.Group(player)
all_sprites.add(platform1, platform2, platform3, platform4, platform5, platform6)
all_sprites.add(harm1, harm2, harm3, harm4, harm5, harm6, harm7, harm8, harm9)
all_sprites.add(block1, block2, block3)
all_sprites.add(key)
all_sprites.add(startImage)
all_sprites.add(endImage)

levelUpdated = False

# Main game loop
running = True
clock.tick(FPS)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keypress and define scroll variables
    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_LEFT] and scroll > 0:
        scroll -= 5

    if key_pressed[pygame.K_RIGHT] and scroll < 1000:
        scroll += 5

    # Draw the world
    draw_bg()
    draw_ground()

    #score tracking 

   

    # Setup level
    if level == 0:
      startImage.setCoord(0,0)
      if key_pressed[pygame.K_SPACE]:
        level+=1
      
    if level == 1:
        if levelUpdated == False :
          player.playerReset()
          player.changeImage()
          key.changeImage()
        startImage.setCoord(0,-500)
        platform1.setCoord(200, 140)
        platform2.setCoord(570, 110)
        platform3.setCoord(710, 80, 60, 10)
        platform4.setCoord(-200, 0)
        platform5.setCoord(-200, 0)
        platform6.setCoord(-200, 0)
        harm1.setCoord(340, 150)
        harm2.setCoord(510, 190)
        harm3.setCoord(570, 190)
        harm4.setCoord(630, 190)
        harm5.setCoord(690, 190)
        harm6.setCoord(750, 190)
        harm7.setCoord(-200, 0)
        harm9.setCoord(-200, 0)
        block1.setCoord(290, 120, 50, 90)
        block2.setCoord(340, 170, 60, 40)
        block3.setCoord(400, 130, 110, 80)
        key.setCoord(730, 60)
        levelUpdated = True
    elif level == 2:
        if levelUpdated == False :
          player.playerReset()
          player.changeImage()
          key.changeImage()
        platform1.setCoord(120, 170)
        platform2.setCoord(30, 130)
        platform3.setCoord(140, 70)
        platform4.setCoord(540, 70)
        platform5.setCoord(660, 100)
        block1.setCoord(260, 110, 40, 100)
        block2.setCoord(300, 110, 180, 60)
        block3.setCoord(480, 150, 240, 20)
        harm1.setCoord(340, 90)
        harm2.setCoord(480, 130)
        harm3.setCoord(540, 130)
        harm4.setCoord(600, 130)
        harm5.setCoord(660, 130)
        harm6.setCoord(-200, 0)
        key.setCoord(310, 190)
        levelUpdated = True
    elif level == 3:
      if levelUpdated == False :
          player.playerReset()
          player.changeImage()
          key.changeImage()
      platform1.setCoord(100, 60)
      platform2.setCoord(190, 60)
      platform3.setCoord(310, 60)
      platform4.setCoord(440, 80)
      platform5.setCoord(570, 60, 80, 20)
      platform6.setCoord(700, 140)
      block1.setCoord(20, 100, 370, 20)
      block2.setCoord(460, 160, 120, 50)
      block3.setCoord(390, 180, 50, 10)
      harm1.setCoord(20, 80)
      harm2.setCoord(80, 80)
      harm3.setCoord(140, 80)
      harm4.setCoord(200, 80)
      harm5.setCoord(260, 80)
      harm6.setCoord(320, 80)
      harm7.setFlipped()
      harm7.setCoord(140, 120)
      
      harm9.setCoord(520, 140)
      key.setCoord(120, 40)
      levelUpdated = True
    elif level == 4:
      endImage.setCoord(0, 0)
      if key_pressed[pygame.K_r]:
          endImage.setCoord(0, -500)
          startImage.setCoord(0, -500)
          key.setCoord(-200, -500)
          level = 1
          levelUpdated = False   # ← ADD THIS
      elif key_pressed[pygame.K_q]:
          running = False

    player.update(platforms, harmList, blocks)

    # Check level
    hits = pygame.sprite.spritecollide(player, keyList, False)
    if hits and 1 <= level <= 3: 
        level += 1
        levelUpdated = False

    all_sprites.draw(screen)
    if 1 <= level <= 3:
      level_text = font.render(f"Level: {level}", True, GOLD)
    else:
      level_text = font.render(f" ", True, GOLD)
    screen.blit(level_text, (10,10))


    level_text = font.render(f"Level: {level}", True, GOLD)
    screen.blit(level_text, (10,10))


    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)
