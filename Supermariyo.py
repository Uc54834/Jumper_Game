import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 1
JUMP_STRENGTH = -20
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mariyo")
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 150
        self.velocity_y = 0
        self.on_ground = False
        
    def update(self, platforms):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # If falling down
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.velocity_y = 0
                # If jumping up
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
        
        # Prevent player from going off the bottom of the screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True
            self.velocity_y = 0
    
    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprites
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

platforms = pygame.sprite.Group()

# Ground
ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
platforms.add(ground)
all_sprites.add(ground)

# Some platforms
platform1 = Platform(100, SCREEN_HEIGHT - 150, 200, 20)
platform2 = Platform(400, SCREEN_HEIGHT - 250, 200, 20)
platform3 = Platform(200, SCREEN_HEIGHT - 350, 200, 20)
platforms.add(platform1, platform2, platform3)
all_sprites.add(platform1, platform2, platform3)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
    
    # Get pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.rect.x += PLAYER_SPEED
    
    # Update
    player.update(platforms)
    
    # Keep player on screen
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH
    
    # Draw
    screen.fill(BLUE)
    all_sprites.draw(screen)
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()