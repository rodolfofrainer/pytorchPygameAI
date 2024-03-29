import pygame
import neat
from random import randint
from classes import PlayerClass, ObstacleClass
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
        self.players = []
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
            player_acceleration = -PLAYER_ACCELERATION
            return player_acceleration
        else:
            player_acceleration = PLAYER_ACCELERATION
            return player_acceleration

    def game_reset(self):
        # Resets game when player collides with obstacle
        self.player = PlayerClass(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 40)
        self.score = 0
        self.obstacles_list = []
        self.frame_iteration = 0

    def update_score(self):
        if self.frame_iteration % 100 == 0:
            self.score += 1

    def run_game(self, genomes, config):
        RUNNING = True

        # NEAT
        nets = []
        ge = []
        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            self.players.append(PlayerClass(
                SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 40))
            g.fiteness = 0
            ge.append(g)

        while RUNNING:

            # Control the frame rate
            self.clock.tick(FPS)

            # Check keyboard input
            key_pressed = pygame.key.get_pressed()

            self.frame_iteration += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT or key_pressed[pygame.K_q]:
                    pygame.quit()
                    quit()

            # Increase obstacle interval counter
            self.obstacle_interval_counter += 1
            self.update_score()

            # Clear the screen
            self.display.fill((180, 180, 180))

            # Check keyboard input
            key_pressed = pygame.key.get_pressed()

            for player in self.players:
                if player.y == 0:
                    player.velocity = 0
                elif player.y == SCREEN_HEIGHT - player.size:
                    player.velocity = 0

                # Update player velocity using acceleration
                player.velocity += self._move(
                    key_pressed[pygame.K_SPACE]) * self.dt

                # Update player position using velocity
                player.y += player.velocity * self.dt

                # Apply gravity to the player's velocity
                player.velocity += self.gravity * self.dt

                # Cap player's y coordinate to prevent it from going negative or outside the screen
                player.y = max(
                    0, min(player.y, SCREEN_HEIGHT - player.size))

            # Create obstacle at a precise timing
            if self.obstacle_interval_counter >= self.obstacle_interval:
                new_obstacle = ObstacleClass(
                    x=SCREEN_WIDTH+25, y=randint(80, SCREEN_HEIGHT), height=SCREEN_HEIGHT)
                self.obstacles_list.append(new_obstacle)

                # Create a mirror obstacle with a 200-pixel window
                mirror_obstacle = new_obstacle.create_mirror_obstacle()
                self.obstacles_list.append(mirror_obstacle)

                self.obstacle_interval_counter = 0  # Reset the interval counter

            # Obstacle movement and collision detection
            for obstacle in self.obstacles_list:
                obstacle.move_obstacle(2)
                pygame.draw.rect(self.display, (255, 0, 0), (obstacle.x,
                                 obstacle.y, obstacle.width, obstacle.height))
                if obstacle.x < player.x:
                    self.score += .05
                if obstacle.x < 0 - obstacle.width:
                    self.obstacles_list.remove(obstacle)

            # Draw the player
            for player in self.players:
                pygame.draw.rect(self.display, (0, 0, 255), (player.x,
                                 player.y, player.size, player.size))
            for player in self.players:
                for obstacle in self.obstacles_list:
                    if obstacle.is_colliding(player):
                        RUNNING=False
                        break

            score_text = self.font.render(
                f"Score: {int(self.score)}", True, (0, 0, 0))
            self.display.blit(score_text, (10, 10))

            # [DEBUG]
            # action = key_pressed[pygame.K_SPACE]
            # print(key_pressed[pygame.K_SPACE])

            # Update the display
            pygame.display.flip()
