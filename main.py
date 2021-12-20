import pygame
from graph.draw_graph import draw_floor
from model.test_data import floor0
from model.model import move_person, move_cleaner
import time


filename = "floor.png"

rect_size = 25
draw_floor(floor0, filename)
pygame.init()
image = pygame.image.load(filename)
img_size = image.get_size()
(img_width, img_height) = img_size
screen = pygame.display.set_mode(img_size)
running = True
color_red = (255, 0, 0)
color_green = (0, 255, 0)
rooms = floor0.get_all_rooms()

font = pygame.font.SysFont('Arial', 12)
BLACK = (0, 0, 0)
step = 0

while running:
    screen.blit(image, (0, 0))
    if step == 1:
        move_cleaner(floor0.get_room('r5'), floor0.get_room('corridor'))
    if step == 2:
        move_cleaner(floor0.get_room('corridor'), floor0.get_room('r6'))
    for room in rooms:
        if room.cleaners > 0:
            rect = pygame.Rect(room.pos_x, img_height - room.pos_y, rect_size, rect_size)
            rect.center = (room.pos_x - rect_size/2 + 5, img_height - room.pos_y - 3)
            pygame.draw.rect(screen, color_red, rect)
            text = font.render(str(room.cleaners), True, BLACK)
            textRect = text.get_rect()
            textRect.center = rect.center
            screen.blit(text, textRect)
        if room.people > 0:
            rect2 = pygame.Rect(room.pos_x, img_height - room.pos_y, rect_size, rect_size)
            rect2.center = (room.pos_x + rect_size/2 + 5, img_height - room.pos_y - 3)
            pygame.draw.rect(screen, color_green, rect2)
            text2 = font.render(str(room.people), True, BLACK)
            textRect2 = text2.get_rect()
            textRect2.center = rect2.center
            screen.blit(text2, textRect2)
    step_text = font.render(str(step), True, BLACK)
    stepRectD = step_text.get_rect()
    stepRectD.topleft = (5, 5)
    screen.blit(step_text, stepRectD)
    pygame.display.update()
    step += 1
    pygame.time.delay(1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
