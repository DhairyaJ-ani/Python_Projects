import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 1000, 800
FPS = 60
player_width, player_height = 50, 50
obstacle_width, obstacle_height = 50, 50
player_speed = 8
obstacle_speed = 10


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")

# Font for displaying score
font = pygame.font.SysFont(None, 36)

# Clock to control game frame rate
clock = pygame.time.Clock()

# Function to display the score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Main game loop
def game_loop():
    # Initial player position
    player_x = WIDTH // 2
    player_y = HEIGHT - player_height - 10
    player_velocity_x = 0
    player_velocity_y = 0

    # Obstacles setup
    obstacles = []
    score = 0

    running = True
    while running:
        screen.fill(BLACK)  # Fill screen with black to clear previous frame

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_velocity_x = -player_speed
        elif keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_velocity_x = player_speed
        else:
            player_velocity_x = 0
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height -10:
            player_velocity_y = player_speed
        elif keys[pygame.K_UP] and player_y > 0:
            player_velocity_y = -player_speed
        else:
            player_velocity_y = 0

        player_x += player_velocity_x
        player_y += player_velocity_y

        # Update obstacles
        if random.random() < 0.05:  # Chance to generate a new obstacle
            obstacle_x = random.randint(0, WIDTH - obstacle_width)
            obstacle_y = -obstacle_height
            obstacles.append([obstacle_x, obstacle_y])

        for obstacle in obstacles[:]:
            obstacle[1] += obstacle_speed  # Move the obstacle down
            if obstacle[1] > HEIGHT:  # If the obstacle goes off the screen
                obstacles.remove(obstacle)
                score += 1  # Increment score for each obstacle passed

            # Check for collision with player
            if (player_x < obstacle[0] + obstacle_width and
                player_x + player_width > obstacle[0] and
                player_y < obstacle[1] + obstacle_height and
                player_y + player_height > obstacle[1]):
                running = False  # End the game if the player collides with an obstacle

            # Draw the obstacles
            pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))
            
        # Draw the player
        pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

        # Display the score
        display_score(score)
        
        # Update the screen
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()            

# Start the game
if __name__ == "__main__":
    game_loop()
