class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height

    def is_colliding(self, player):
        if player.x + player.size > self.x and player.x < self.x + self.width:
            if player.y + player.size > self.y and player.y < self.y + self.height:
                return True
        return False
