import pygame
from random import randint
from player_class import Player
from obstacle_class import Obstacle
from constants import *


class GameStart():
    def __init__(self):
        pygame.init()
        # init display
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flapping cube')
        self.clock = pygame.time.Clock()

        # Game iteration control
        self.dt = 1 / FPS
        self.frame_iteration = 0

        # Player setup
        self.player = Player(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 40)
        self.gravity = GRAVITY_CONST
        self.player_acceleration = 0

        # Variables for obstacle generation
        self.obstacle_interval = FPS * 1
        self.obstacle_interval_counter = 0
        self.obstacles_list = []

        # Font for collision text
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.score = 0

    def _move(self, action):
        if action:
            self.player.velocity = -PLAYER_MAX_VELOCITY

    def game_reset(self):
        # Resets game when player collides with obstacle
        self.player = Player(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 40)
        self.score = 0
        self.obstacles_list = []
        self.frame_iteration = 0

    def update_score(self):
        if self.frame_iteration % 100 == 0:
            self.score += 1

    def run_game(self, action=None):
        while True:
            self.frame_iteration += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

             # Check keyboard input
            key_pressed = pygame.key.get_pressed()

            # Close game if Q key is pressed
            if key_pressed[pygame.K_q]:
                pygame.quit()
                quit()

            if key_pressed[pygame.K_SPACE]:
                self._move(1)

            # Increase obstacle interval counter
            self.obstacle_interval_counter += 1
            self.update_score()

            # Clear the screen
            self.display.fill((180, 180, 180))

            self._move(action)

            # Player movement
            # Cap player's velocity to prevent it from going negative or exceeding the max velocity
            if self.player.y == 0:
                self.player.velocity = 0
            elif self.player.y == SCREEN_HEIGHT - self.player.size:
                self.player.velocity = 0
            # Update player velocity using acceleration
            self.player.velocity += self.player_acceleration * self.dt
            # Update player position using velocity
            self.player.y += self.player.velocity * self.dt
            # Apply gravity to the player's velocity
            self.player.velocity += self.gravity * self.dt
            # Cap player's y coordinate to prevent it from going negative or outside the screen
            self.player.y = max(
                0, min(self.player.y, SCREEN_HEIGHT - self.player.size))

            # Create obstacle at a precise timing
            if self.obstacle_interval_counter >= self.obstacle_interval:
                new_obstacle = Obstacle(
                    x=SCREEN_WIDTH+20 + 5, y=randint(80, SCREEN_HEIGHT), height=SCREEN_HEIGHT)
                self.obstacles_list.append(new_obstacle)

                # Create a mirror obstacle with a 200-pixel window
                mirror_obstacle = new_obstacle.create_mirror_obstacle()
                self.obstacles_list.append(mirror_obstacle)

                self.obstacle_interval_counter = 0  # Reset the interval counter

            # Obstacle movement and collision detection
            for obstacle in self.obstacles_list:
                if obstacle.x-obstacle.width < self.player.x-self.player.size:
                    self.score += 10
                obstacle.move_obstacle(2)
                pygame.draw.rect(self.display, (255, 0, 0), (obstacle.x,
                                 obstacle.y, obstacle.width, obstacle.height))
                if obstacle.x < 0 - obstacle.width:
                    self.obstacles_list.remove(obstacle)

            # Draw the player
            pygame.draw.rect(self.display, (0, 0, 0), (self.player.x,
                             self.player.y, self.player.size, self.player.size))

            for obstacle in self.obstacles_list:
                if obstacle.is_colliding(self.player):
                    self.game_reset()

            score_text = self.font.render(
                f"Score: {self.score}", True, (0, 0, 0))
            self.display.blit(score_text, (10, 10))

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(FPS)
