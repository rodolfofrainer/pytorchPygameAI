from player_class import Player
from obstacle_class import Obstacle
import pygame
from random import randint
from constants import *

# Initialize pygame
pygame.init()


# Variables for obstacle generation
obstacle_interval = FPS * 1
obstacle_interval_counter = 0
obstacles_list = []

# Set up the display
pygame.display.set_caption('Show Text')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Player setup
gravity = GRAVITY_CONST
player = Player(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 40)

# Font for collision text
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Colliding', True, (0, 255, 0), (0, 0, 128))

# Calculate time increment per frame
dt = 1 / FPS

# Game loop
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # Increase obstacle interval counter
    obstacle_interval_counter += 1

    # Clear the screen
    screen.fill((180, 180, 180))

    # Check keyboard input
    key_pressed = pygame.key.get_pressed()

    # Draw the player
    pygame.draw.rect(screen, (0, 0, 0), (player.x,
                     player.y, player.size, player.size))

    # Modify gravity and player position based on input
    if key_pressed[pygame.K_SPACE]:
        gravity = 0
        if player.y > 0:
            player.y -= PLAYER_SPEED * dt
        else:
            player.y = 0
    else:
        gravity = GRAVITY_CONST
        player.y += gravity * dt

    # Stop player from going off screen
    player.y = max(0 - player.size, min(player.y, SCREEN_HEIGHT - player.size))

    # Close game if Q key is pressed
    if key_pressed[pygame.K_q]:
        RUNNING = False

    # Create obstacle at a precise timing
    if obstacle_interval_counter >= obstacle_interval:
        new_obstacle = Obstacle(
            x=SCREEN_WIDTH + 5, y=randint(80, SCREEN_HEIGHT), height=SCREEN_HEIGHT)
        obstacles_list.append(new_obstacle)

        # Create a mirror obstacle with a 60-pixel window
        mirror_obstacle = new_obstacle.create_mirror_obstacle()
        obstacles_list.append(mirror_obstacle)

        obstacle_interval_counter = 0  # Reset the interval counter

    for obstacle in obstacles_list:
        # Move and draw the obstacle
        obstacle.move_obstacle(2)
        pygame.draw.rect(screen, (255, 0, 0), (obstacle.x,
                         obstacle.y, obstacle.width, obstacle.height))

        # Check for collision with player
        if obstacle.is_colliding(player):
            screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Remove obstacles that are off-screen
        if obstacle.x < 0 - obstacle.width:
            obstacles_list.remove(obstacle)

    # [DEBUG]
    # Print player position, gravity, and obstacle interval
    # print(player.x, player.y)
    # print(gravity)
    # print(obstacle_interval_counter)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
