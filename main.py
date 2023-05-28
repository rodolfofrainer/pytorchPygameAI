from player_class import Player
from obstacle_class import Obstacle
import pygame

from random import randint

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RUNNING = True
FPS = 144

GRAVITY_CONST = 1500
PLAYER_SPEED = 1800
obstacle_interval = 0

obstacles_list = []

pygame.display.set_caption('Show Text')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

gravity = GRAVITY_CONST
player_size = 50
dt = 1 / FPS

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Colliding', True, (0, 255, 0), (0, 0, 128))

player = Player(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 40)

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    obstacle_interval += 1

    screen.fill((180, 180, 180))

    key_pressed = pygame.key.get_pressed()

    # draws player
    pygame.draw.rect(screen, (0, 0, 0), (player.x,
                     player.y, player.size, player.size))

    # modifies gravity and player position based on input
    if key_pressed[pygame.K_SPACE]:
        gravity = 0
        if player.y > 0:
            player.y -= PLAYER_SPEED * dt
        else:
            player.y = 0
    else:
        gravity = GRAVITY_CONST
        player.y += gravity * dt

    # stops player from going off screen
    player.y = max(0 - player.size, min(player.y, SCREEN_HEIGHT - player.size))

    # closes game if Q key is pressed
    if key_pressed[pygame.K_q]:
        RUNNING = False

    if obstacle_interval == FPS/2:
        new_obstacle = Obstacle(
            x=SCREEN_WIDTH + 5,
            y=randint(0, SCREEN_HEIGHT),
            height=SCREEN_HEIGHT
        )
        obstacles_list.append(new_obstacle)
        # print whenever a new obstacle is created
        print("obstacle created")
        obstacle_interval = 0

    for obstacle in obstacles_list:
        # draws obstacle
        obstacle.move_obstacle(5)
        pygame.draw.rect(screen, (255, 0, 0), (obstacle.x,
                                               obstacle.y, obstacle.width, obstacle.height))
        if obstacle.is_colliding(player):
            screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        if obstacle.x < 0-obstacle.width:
            obstacles_list.pop(0)

    # [DEBUG]
    # print player position
    # print(player.x, player.y)
    # print gravity applied to player
    # print(gravity)
    # print obstacle_interval
    # print(obstacle_interval)

    pygame.display.flip()
    dt = clock.tick(FPS) / 1000

    # FPS
    clock.tick(FPS)

pygame.quit()
