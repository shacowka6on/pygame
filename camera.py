from settings import WIDTH, HEIGHT

class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0

    def update(self, player):
        self.offset_x = player.rect.centerx - WIDTH // 4
        self.offset_y = player.rect.centery - HEIGHT // 2

    def apply(self, rect):
        # Call this when drawing anything
        return rect.move(-self.offset_x, -self.offset_y)