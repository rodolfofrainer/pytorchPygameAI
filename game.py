import pygame
from random import randint
from player_class import Player
from obstacle_class import Obstacle
from constants import *


class GameStart():
    def __init__(self):
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Flapping cube')
        self.clock = pygame.time.Clock()
        self.reset()
        self.player = Player(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 40)
        # Variables for obstacle generation
        self.obstacle_interval = FPS * 1
        self.obstacle_interval_counter = 0
        self.obstacles_list = []
        # Player setup
        self.gravity = GRAVITY_CONST
        self.player_acceleration = 0
        # Calculate time increment per frame
        self.dt = 1 / FPS
        # Font for collision text
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render(
            'Colliding', True, (0, 255, 0), (0, 0, 128))
        self.reward = 0

    # Game loop
    def reset(self):
        self.player = Player(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 40)
        self.reward = 0

    def run_game(self):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        # Increase obstacle interval counter
        obstacle_interval_counter += 1

        # Clear the screen
        self.display.fill((180, 180, 180))

        # Check keyboard input
        key_pressed = pygame.key.get_pressed()

        if self.player.y == 0:
            self.player.velocity = 0
        elif self.player.y == SCREEN_HEIGHT - self.player.size:
            self.player.velocity = 0

        # Modify player acceleration and velocity based on input
        if key_pressed[pygame.K_SPACE]:
            player_acceleration = -PLAYER_ACCELERATION
        else:
            player_acceleration = PLAYER_ACCELERATION

        # Update player velocity using acceleration
        self.player.velocity += player_acceleration * self.dt

        # Update player position using velocity
        self.player.y += self.player.velocity * self.dt

        # Apply gravity to the player's velocity
        self.player.velocity += self.gravity * self.dt

        # Cap player's y coordinate to prevent it from going negative or outside the screen
        self.player.y = max(
            0, min(self.player.y, SCREEN_HEIGHT - self.player.size))

        # Close game if Q key is pressed
        if key_pressed[pygame.K_q]:
            RUNNING = False

        # Create obstacle at a precise timing
        if obstacle_interval_counter >= self.obstacle_interval:
            new_obstacle = Obstacle(
                x=SCREEN_WIDTH+20 + 5, y=randint(80, SCREEN_HEIGHT), height=SCREEN_HEIGHT)
            self.obstacles_list.append(new_obstacle)

            # Create a mirror obstacle with a 200-pixel window
            mirror_obstacle = new_obstacle.create_mirror_obstacle()
            self.obstacles_list.append(mirror_obstacle)

            obstacle_interval_counter = 0  # Reset the interval counter

        # Obstacle movement and collision detection
        for obstacle in self.obstacles_list:
            obstacle.move_obstacle(2)
            pygame.draw.rect(self.display, (255, 0, 0), (obstacle.x,
                             obstacle.y, obstacle.width, obstacle.height))

            if obstacle.is_colliding(self.player):
                self.display.blit(
                    self.text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            if obstacle.x < 0 - obstacle.width:
                self.obstacles_list.remove(obstacle)

        # Draw the player
        pygame.draw.rect(self.display, (0, 0, 0), (self.player.x,
                         self.layer.y, self.player.size, self.player.size))

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        self.clock.tick(FPS)

    # Quit the game
    pygame.quit()
