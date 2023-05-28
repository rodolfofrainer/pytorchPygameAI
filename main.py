from player_class import Player
from obstacle_class import Obstacle

import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RUNNING = True
FPS = 144

pygame.display.set_caption('Show Text')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

gravity = 1000
player_size = 50
dt = 0

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Colliding', True, (0, 255, 0), (0, 0, 128))

player = Player(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 40)

obstacle = Obstacle(x=player.x+(player.size/2), y=player.y,
                    width=player.size, height=SCREEN_HEIGHT)

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    screen.fill((255, 255, 255))

    if obstacle.is_colliding(player):
        screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    key_pressed = pygame.key.get_pressed()

    # draws obstacle
    pygame.draw.rect(screen, (255, 0, 0), (obstacle.x,
                     obstacle.y, obstacle.width, obstacle.height))

    # draws player
    pygame.draw.rect(screen, (0, 0, 0), (player.x,
                     player.y, player.size, player.size))

    # applies gravity to player
    player.y += gravity * dt

    # stops player from going off screen
    if (player.y - (3000 * dt)) < 0:
        player.y = 0 - player.size
    if player.y > SCREEN_HEIGHT - player.size:
        player.y = SCREEN_HEIGHT - player.size
    if player.y < 0:
        player.y = 0 + player.size/2

    # list of commands
    if key_pressed[pygame.K_SPACE]:
        gravity = 0
        player.y -= 3000 * dt
    if key_pressed[pygame.K_q]:
        RUNNING = False

    # print player position [DEBUG]
    print(player.x, player.y)

    pygame.display.flip()
    dt = clock.tick(FPS) / 1000
    clock.tick(60)

pygame.quit()
