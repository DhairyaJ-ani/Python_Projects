import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 600, 200
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Game")

# Load font
font = pygame.font.SysFont("Arial", 24)

# Define the Dino class
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 10
        self.rect.left = 50
        self.y_velocity = 0
        self.is_jumping = False

    def update(self):
        # Apply gravity
        if self.is_jumping:
            self.y_velocity = -15  # Jump force
            self.is_jumping = False
        self.y_velocity += 1  # Gravity effect

        # Update position
        self.rect.y += self.y_velocity

        # Prevent dino from going below the ground
        if self.rect.bottom > HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
            self.y_velocity = 0

    def jump(self):
        if self.rect.bottom == HEIGHT - 10:  # Can only jump if standing
            self.is_jumping = True


# Define the Cactus class
class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - 50
        self.rect.x = WIDTH

    def update(self):
        self.rect.x -= 5
        if self.rect.x < -20:  # Reset cactus position when it goes off screen
            self.rect.x = WIDTH
            self.rect.y = HEIGHT - 50

# Set up sprite groups
dino = Dino()
cactus_group = pygame.sprite.Group()

# Create a cactus every 2-3 seconds
def spawn_cactus():
    cactus = Cactus()
    cactus.rect.x = WIDTH
    cactus_group.add(cactus)

# Create the sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(dino)

# Game Loop
clock = pygame.time.Clock()
score = 0
running = True

# Timer for spawning cacti
pygame.time.set_timer(pygame.USEREVENT, random.randint(1500, 3000))

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino.jump()
        if event.type == pygame.USEREVENT:
            spawn_cactus()
            score += 1

    # Update
    all_sprites.update()
    cactus_group.update()

    # Collision detection
    if pygame.sprite.spritecollide(dino, cactus_group, False):
        running = False
        print("Game Over! Final Score:", score)

    # Draw everything
    all_sprites.draw(screen)
    cactus_group.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    # Refresh screen
    pygame.display.update()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
