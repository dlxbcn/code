class CloudObject():
    def __init__(self, image, pos, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect()
        self.pos.x = pos[0]
        self.pos.y = pos[1]

    def move_to_left(self):
        self.pos.x -= self.speed
