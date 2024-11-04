import pygame
class Plane():
    def __init__(self, image, speed, size, pos, max_height, max_width) -> None:
        # super().__init__()
        img = pygame.image.load(image)
        scaled_img = pygame.transform.scale(img, size)
        self.image = scaled_img
        self.pos = scaled_img.get_rect()
        self.pos.x = pos[0]
        self.pos.y = pos[1]
        self.speed = speed
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.max_height = max_height
        self.max_width = max_width

    def set_direction(self, left=False, right=False, up=False, down=False):
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    def move(self):
        if self.up:
            self.pos.y -= self.speed
        elif self.down:
            self.pos.y += self.speed
        if self.right:
            self.pos.x += self.speed
        elif self.left:
            self.pos.x -= self.speed

        if self.pos.top <= 0:
            self.pos.top = 0
        if self.pos.bottom >= self.max_height:
            self.pos.bottom = self.max_height
        if self.pos.left <= 0:
            self.pos.left = 0
        if self.pos.right >= self.max_width:
            self.pos.right = self.max_width