import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RUNNING = True
FPS = 144

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

gravity = 1000
player_size = 50
dt = 0

class Player:
    def __init__(self, x,y, size) -> None:
        self.x = int(x)
        self.y = int(y)
        self.size = size

player = Player(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 40)

obstacles = []

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    screen.fill((0, 0, 0))
    
    
    keys = pygame.key.get_pressed()
    pygame.draw.rect(screen, (255, 255, 255), (player.x, player.y, player.size, player.size))
    
    #applies gravity to player
    player.y += gravity * dt
    
    #stops player from going off screen
    if player.y > SCREEN_HEIGHT - player.size:
        player.y = SCREEN_HEIGHT - player.size
    if player.y < 0:
        player.y = 0 + player.size/2
    
    #list of commands
    if keys[pygame.K_SPACE]:
        player.y -= 3000 * dt
    if keys[pygame.K_q]:
        RUNNING = False
    
    #print player position [DEBUG]
    print(player.x, player.y)
    
    
    pygame.display.flip()
    dt = clock.tick(FPS) / 1000
    clock.tick(60)

pygame.quit()