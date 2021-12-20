import pygame
from drawer.draw_floor import draw_floor
from drawer.legend_drawer import LegendDrawer
from drawer.rectangle import Rectangle
from drawer.room_drawer import RoomDrawer
from model.jsonHelper import fromFile

floor0 = fromFile("floor0.json")

rect_size = 25
pygame.init()
screen = pygame.display.set_mode((1500, 800))
running = True
color_red = (255, 0, 0)
color_green = (0, 255, 0)
rooms = floor0.get_all_rooms()
room_drawer = RoomDrawer(
    screen,
    Rectangle(0, 0, 1500, 600),
    border_width=2,
    blocks_x=floor0.get_blocks_x(),
    blocks_y=floor0.get_blocks_y()
)
draw_floor(floor0, room_drawer)
legend_drawer = LegendDrawer(screen, Rectangle(0, 600, 1500, 200))
legend_drawer.draw()
font = pygame.font.SysFont('Arial', 12)
BLACK = (0, 0, 0)
step = 0

while running:
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
