import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ENEMY_SPEED = 2
PLAYER_SIZE = 50
ENEMY_SIZE = 40
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 25
BULLET_SPEED = 7
BULLET_SIZE = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Roguelike Game")

# Font for displaying health
font = pygame.font.SysFont("Arial", 20)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.health = 100
        self.bullets = pygame.sprite.Group()  # Group to store player's bullets

    def update(self, keys):
        # Player movement logic
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED

        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        """Shoot a bullet from the player's position"""
        bullet = Bullet(self.rect.centerx, self.rect.top) 
        # Shoot from player's top center
        self.bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        """Move the bullet upwards"""
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:  # Remove bullet if it goes off-screen
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # Spawn on random edge of screen
        spawn_edge = random.choice(["top", "bottom", "left", "right"])
        if spawn_edge == "top":
            self.rect.center = (random.randint(0, SCREEN_WIDTH), 0)
        elif spawn_edge == "bottom":
            self.rect.center = (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT)
        elif spawn_edge == "left":
            self.rect.center = (0, random.randint(0, SCREEN_HEIGHT))
        elif spawn_edge == "right":
            self.rect.center = (SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT))
    
    def update(self, player_rect):
        # Move enemy towards player
        if self.rect.x < player_rect.x:
            self.rect.x += ENEMY_SPEED
        elif self.rect.x > player_rect.x:
            self.rect.x -= ENEMY_SPEED
        
        if self.rect.y < player_rect.y:
            self.rect.y += ENEMY_SPEED
        elif self.rect.y > player_rect.y:
            self.rect.y -= ENEMY_SPEED

# Create player object and sprite group
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create enemy group
enemies = pygame.sprite.Group()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()  # Shoot a bullet when the spacebar is pressed

    # Update player and enemies
    keys = pygame.key.get_pressed()
    player.update(keys)

    # Spawn new enemies randomly
    if random.randint(1, 100) <= 2:  # Random spawn chance
        new_enemy = Enemy()
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)

    # Update enemy positions
    for enemy in enemies:
        enemy.update(player.rect)
        
        # Check for collision with player
        if player.rect.colliderect(enemy.rect):
            player.health -= 10  # Decrease player health
            enemy.kill()  # Remove enemy from the game after collision

    # Update and draw bullets
    player.bullets.update()
    for bullet in player.bullets:
        player.bullets.draw(screen)
    
    # Check for bullet-enemy collisions
    for bullet in player.bullets:
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                enemy.kill()  # Remove enemy if it is hit by a bullet
                bullet.kill()  # Remove the bullet after hitting an enemy

    # Draw everything
    all_sprites.draw(screen)

    # Draw health bar
    pygame.draw.rect(screen, RED, (10, 10, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(screen, GREEN, (10, 10, (player.health / 100) * HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
    health_text = font.render(f"HP: {player.health}", True, WHITE)
    screen.blit(health_text, (10, 10))

    # Check for game over
    if player.health <= 0:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds before closing
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
