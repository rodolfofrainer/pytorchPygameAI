from constants import *


class Obstacle:
    def __init__(self, x, y, height, width=20):
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height

    def is_colliding(self, player):
        if player.x + player.size > self.x and player.x < self.x + self.width:
            if player.y + player.size > self.y and player.y < self.y + self.height:
                return True
        return False

    def move_obstacle(self, moving_speed):
        self.x -= moving_speed

    def create_mirror_obstacle(self):
        return Obstacle(self.x, self.y - SCREEN_HEIGHT - 200, self.height, self.width)
