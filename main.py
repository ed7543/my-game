import pygame, sys
import random
from pygame.locals import *

# Initialize game
pygame.init()

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pygame Game')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load Assets
player_image = pygame.image.load('cat.png')
enemy_image = pygame.image.load('enemycat.png')
closedDoor_image = pygame.image.load('closeddoor.png')

# Load background
background_image_room1 = pygame.image.load('background.jpeg')

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)
        self.health = 10
        self.time = pygame.time.get_ticks()  # To track attack timings

    def move(self, keys, enemies):
        speed = 3
        prev_rect = self.rect.copy()

        if keys[pygame.K_w]:
            self.rect.y -= speed
        if keys[pygame.K_s]:
            self.rect.y += speed
        if keys[pygame.K_a]:
            self.rect.x -= speed
        if keys[pygame.K_d]:
            self.rect.x += speed

        # Limiting movement inside the borders
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Collision checking with enemies, revert to original position if collision
       # for enemy in enemies:
        #    if self.rect.colliderect(enemy.rect):
         #       self.rect = prev_rect  # Revert position on collision

    def attack(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):  # Player attacks when colliding with enemy
                enemy.take_damage(1)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.health = 2

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def attack(self, player):
        # Define attack box dimensions
        attack_width = 100  # Attack box width
        attack_height = 100  # Attack box height
        attack_offset_x = 50  # Offset from player position
        attack_offset_y = 50  # Offset from player position

        # Create the attack box (centered around player)
        attack_box = pygame.Rect(self.rect.x + attack_offset_x, self.rect.y + attack_offset_y, attack_width, attack_height)

        self.attack_box_colliding = False  # Reset attack box collision

        for enemy in enemies:
            # Update attack box based on the player's position
            self.attack_box = pygame.Rect(self.rect.x + 50, self.rect.y + 50, 50, 50)  # Attack box near the player
            if self.rect.colliderect(player.rect):
                player.take_damage(1)

    def update(self, player):
        # Placeholder: Update logic for enemy behavior (e.g., attacking after a timer)
        current_time = pygame.time.get_ticks()  # Getting current time in ms
        if current_time - player.time > 3000:  # Attack every 3 seconds
            self.attack(player)


# Setup Groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Function for the first room (Loneliness)
def room1():
    global all_sprites
    global enemies
    enemies.empty()  # Clear previous enemies
    all_sprites.empty()

    # Add player
    player = Player()
    all_sprites.add(player)

    # Spawn 5 enemies in random positions
    for _ in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Game loop for room 1
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Get the keys pressed
        keys = pygame.key.get_pressed()

        # Move the player
        player.move(keys, enemies)

        # Handle attack
        if keys[pygame.K_SPACE]:
            player.attack(enemies)

        # Update each enemy manually
        for enemy in enemies:
            enemy.update(player)  # Pass the player to the enemy update method

        # Fill screen with the background in room 1
        screen.blit(background_image_room1, (0, 0))

        # Draw all sprites
        all_sprites.draw(screen)

        # Update the screen
        pygame.display.update()

        # Set the framerate
        pygame.time.Clock().tick(60)

        # Exit room 1 if all enemies are defeated
        if len(enemies) == 0:
            break

# Run the game by calling the room functions
room1()  # Start with room 1
