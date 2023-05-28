import pygame
from random import randint
from player_class import Player
from obstacle_class import Obstacle
from constants import *

# Initialize pygame
pygame.init()

# Set up the display
pygame.display.set_caption('Show Text')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Variables for obstacle generation
obstacle_interval = FPS * 1
obstacle_interval_counter = 0
obstacles_list = []

# Player setup
player = Player(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 40)
gravity = GRAVITY_CONST
player_acceleration = 0

# Font for collision text
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Colliding', True, (0, 255, 0), (0, 0, 128))

# Calculate time increment per frame
dt = 1 / FPS

# Game loop
while RUNNING:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # Increase obstacle interval counter
    obstacle_interval_counter += 1

    # Clear the screen
    screen.fill((180, 180, 180))

    # Check keyboard input
    key_pressed = pygame.key.get_pressed()

    # Modify player acceleration and velocity based on input
    if key_pressed[pygame.K_SPACE]:
        player_acceleration = - PLAYER_ACCELERATION
    else:
        player_acceleration = PLAYER_ACCELERATION

    player.velocity += player_acceleration * dt
    player.y += player.velocity * dt

    # Apply gravity to the player's velocity
    player.velocity += gravity * dt

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

        # Create a mirror obstacle with a 200-pixel window
        mirror_obstacle = new_obstacle.create_mirror_obstacle()
        obstacles_list.append(mirror_obstacle)

        obstacle_interval_counter = 0  # Reset the interval counter

    # Obstacle movement and collision detection
    for obstacle in obstacles_list:
        obstacle.move_obstacle(2)
        pygame.draw.rect(screen, (255, 0, 0), (obstacle.x,
                         obstacle.y, obstacle.width, obstacle.height))

        if obstacle.is_colliding(player):
            screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        if obstacle.x < 0 - obstacle.width:
            obstacles_list.remove(obstacle)

    # Draw the player
    pygame.draw.rect(screen, (0, 0, 0), (player.x,
                     player.y, player.size, player.size))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
