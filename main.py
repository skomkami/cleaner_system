import pygame
from drawer.draw_floor import draw_floor
from drawer.legend_drawer import LegendDrawer
from model.test_data import floor0
from drawer.room_drawer import RoomDrawer
from drawer.rectangle import Rectangle


rect_size = 25
pygame.init()
img_height = 800
img_width = 1500
screen = pygame.display.set_mode((img_width, img_height))
running = True
color_red = (255, 0, 0)
color_green = (0, 255, 0)
rooms = floor0.get_all_rooms()
room_drawer = RoomDrawer(
    screen,
    Rectangle(0, 0, img_width, img_height - 200),
    border_width=2,
    blocks_x=floor0.get_blocks_x(),
    blocks_y=floor0.get_blocks_y()
)
legend_drawer = LegendDrawer(screen, Rectangle(0, 600, img_width, 200))
font = pygame.font.SysFont('Arial', 12)
BLACK = (0, 0, 0)
step = 0

while running:
    draw_floor(floor0, room_drawer)
    legend_drawer.draw()
    # if step == 1:
    #     move_cleaner(floor0.get_room('r5'), floor0.get_room('cs2'))
    # if step == 2:
    #     move_cleaner(floor0.get_room('cs2'), floor0.get_room('r6'))
    for room in rooms:
        if room.cleaners > 0:
            rect = pygame.Rect(room.pos_x - 15, img_height - room.pos_y, rect_size, rect_size)
            rect.center = (room.room_center_x + 15, room.room_center_y)
            pygame.draw.rect(screen, color_red, rect)
            text = font.render(str(room.cleaners), True, BLACK)
            textRect = text.get_rect()
            textRect.center = rect.center
            screen.blit(text, textRect)
        if room.people > 0:
            rect2 = pygame.Rect(room.pos_x, img_height - room.pos_y, rect_size, rect_size)
            rect2.center = (room.room_center_x - 15, room.room_center_y)
            pygame.draw.rect(screen, color_green, rect2)
            text2 = font.render(str(room.people), True, BLACK)
            textRect2 = text2.get_rect()
            textRect2.center = rect2.center
            screen.blit(text2, textRect2)
    step_text = font.render(str(step), True, BLACK)
    stepRectD = step_text.get_rect()
    stepRectD.topleft = (5, 500)
    screen.blit(step_text, stepRectD)
    pygame.display.update()
    step += 1
    pygame.time.delay(1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
