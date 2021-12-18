import pygame
from graph.draw_graph import draw_floor
from model.test_data import floor0
from pygame.color import Color


filename = "floor.png"

draw_floor(floor0, filename)
pygame.init()
image = pygame.image.load(filename)
img_size = image.get_size()
(img_width, img_height) = img_size
screen = pygame.display.set_mode(img_size)
running = True
room = floor0.getRoom('r6')
color = (255, 0, 0)
while running:
    screen.blit(image, (0, 0))
    pygame.draw.rect(screen, color, pygame.Rect(room.pos_x, img_height - room.pos_y, 20, 20))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
