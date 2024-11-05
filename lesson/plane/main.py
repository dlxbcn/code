import pygame
import random
from cloud import CloudObject
from plane import Plane

pygame.init()
pygame.display.set_caption("飞机")
screen_height = 768
screen_width = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

cloud1 = pygame.image.load("images/cloud1.png")
scaled_cloud1 = pygame.transform.scale(cloud1, (200, 70))

cloud2 = pygame.image.load("images/cloud2.png")
scaled_cloud2 = pygame.transform.scale(cloud2, (100, 50))

cloud3 = pygame.image.load("images/cloud3.png")
scaled_cloud3 = pygame.transform.scale(cloud3, (120, 60))

cloud4 = pygame.image.load("images/cloud4.png")
scaled_cloud4 = pygame.transform.scale(cloud4, (80, 30))

speed = 100
move = (0, 0)
cloud_list = []
time = 0

plane = Plane("images/plane.png", 3, (80, 40), (100, 100), screen_height, screen_width)
running = True
while running:

    time -=1
    if time <= 0:
        time = 100
        x = 1025
        y = random.randint(1, 600)
        cloud = random.choice([scaled_cloud1,scaled_cloud2,scaled_cloud3,scaled_cloud4])
        cloud_speed = random.choice([2, 3, 4])
        cloud_list.append(CloudObject(cloud, (x, y), cloud_speed))

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                plane.set_direction(right=True)
            if event.key == pygame.K_LEFT:
                plane.set_direction(left=True)
            if event.key == pygame.K_UP:
               plane.set_direction(up=True)
            if event.key == pygame.K_DOWN:
                plane.set_direction(down=True)

    screen.fill((255,255,255))
    
    for cloud in cloud_list:
        cloud.move_to_left()
        if cloud.pos.right <= 0:
            cloud_list.remove(cloud)
        else:
            screen.blit(cloud.image, cloud.pos)

    plane.move()
    screen.blit(plane.image, plane.pos)
    pygame.display.flip()
    clock.tick(60)
