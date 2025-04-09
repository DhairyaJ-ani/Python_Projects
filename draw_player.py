import pygame
import os
import random

pygame.init()
PLAYER_HIT = pygame.USEREVENT + 1
OBSTACLE_HIT = pygame.USEREVENT + 2

HEIGHT = 600
WIDTH = 800
fps = 40
player_height, bullet_height = 50, 10
player_width, bullet_width = 50, 5
velocity = 7
obs_vel = 7
Max_Bullets = 4
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("DRAWING, SHOOTING AND MORE!")

CHARACTER_IMAGE= pygame.image.load(os.path.join('SKECHES','character.png'))
CHARACTER = pygame.transform.scale(CHARACTER_IMAGE,(player_width,player_height))

BACKGROUND = pygame.image.load(os.path.join('SKECHES','OPTION.jpg'))
Game_background = pygame.transform.scale(BACKGROUND,(WIDTH,HEIGHT))


def player_handling(keys,player):
    if keys[pygame.K_w] and player.y > 10:
        player.y -= velocity
    if keys[pygame.K_s] and player.y < HEIGHT - player_height - 10:
        player.y += velocity
    if keys[pygame.K_a] and player.x > 10:
        player.x -= velocity
    if keys[pygame.K_d] and player.x < WIDTH - player_width - 10:
        player.x += velocity

def bullet_handling(bullets,obstacles):
    for bullet in bullets:
        bullet.y -= velocity
        if bullet.y < 0:
            bullets.remove(bullet)
        for obstacle in obstacles:
            if bullet.colliderect(obstacle):
                obstacles.remove(obstacle)
                bullets.remove(bullet)

def draw_screen(player,bullets,obstacles):
    screen.blit(Game_background,(0,0))
    screen.blit(CHARACTER,(player.x,player.y))
    for obstacle in obstacles:
        pygame.draw.rect(screen,WHITE,obstacle)
    for bullet in bullets:
        pygame.draw.rect(screen,WHITE,bullet)
    
    pygame.display.update()
        
def game_loop():
    running = True
    clock = pygame.time.Clock()
    player = pygame.Rect(WIDTH // 2 - player_width,HEIGHT - player_height-10,player_width,player_height)
    bullets = []
    obstacles =[]
    while running:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < Max_Bullets:
                    bullet = pygame.Rect(player.x + player_width // 2,player.y - player_height,bullet_width,bullet_height)
                    bullets.append(bullet)
        
        for obstacle in obstacles:
            if random.random() < 0.02:
                obstacle.x = random.randint(0,WIDTH - player_width)
                obstacle.y = -player_height
                obstacles.append(obstacle)
                obstacle = pygame.Rect(obstacle.x,obstacle.y,player_width,player_height)
                obstacle.y += obs_vel
            elif obstacle.y > HEIGHT:
                obstacles.remove(obstacle)
            else: 
                pass

            if (player.x < obstacle[0] + player_width and
                player.x + player_width > obstacle[0] and
                player.y < obstacle[1] + player_height and
                player.y + player_height > obstacle[1]):
                running = False
                
        clock.tick(fps)

        keys = pygame.key.get_pressed()
        player_handling(keys,player)
        bullet_handling(bullets,obstacles)  
        draw_screen(player,bullets,obstacles)
    pygame.quit()            



if __name__ == "__main__":
    game_loop()

