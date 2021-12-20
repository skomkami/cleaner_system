import pygame
from drawer.rectangle import Rectangle
from model.model import Room, RoomType


def get_color_for_room(r: Room):
    color = "#285CBD"
    if r.room_type == RoomType.Administration:
        color = "#00BFB2"
    if r.room_type == RoomType.LaboratoryRoom:
        color = "#FFCB58"
    if r.room_type == RoomType.Entrance:
        color = "#5A9E2F"
    if r.room_type == RoomType.LectureHall:
        color = "#FF9057"
    if r.room_type == RoomType.Hall:
        color = "#F5F0AC"

    return pygame.Color(color)


class RoomDrawer:
    def __init__(self, pygame_screen: pygame.Surface, drawing_area: Rectangle, border_width: int, blocks_x: int,
                 blocks_y: int):
        self.pygame_screen = pygame_screen
        self.area = drawing_area
        self.border = border_width
        self.block_w = pygame_screen.get_width() / blocks_x
        self.block_h = pygame_screen.get_height() / blocks_y
        self.font = pygame.freetype.SysFont("Comic Sans MS", 24)

    def draw_rect(self, x: int, y: int, width: int, height: int, color: pygame.Color = pygame.Color(0, 0, 0)):
        rect = pygame.Rect(x + self.area.start_x, self.area.start_y + y, width, height)
        pygame.draw.rect(self.pygame_screen, color, rect)

    def draw_text(self, x: int, y: int, text: str, color: pygame.Color = pygame.Color(0, 0, 0)):
        self.font.render_to(self.pygame_screen, (x, y), text, color)

    def draw_room(self, r: Room):
        room_color = get_color_for_room(r)
        x_start = int(self.block_w * r.pos_x)
        y_start = int(self.block_h * r.pos_y)
        width = int(self.block_w * r.width)
        height = int(self.block_h * r.height)
        self.draw_rect(x=x_start + self.border, y=y_start + self.border, width=width - self.border,
                       height=height - self.border,
                       color=room_color)
        self.draw_rect(x=x_start, y=y_start, width=width, height=self.border)  # top border
        self.draw_rect(x=x_start, y=y_start + height - self.border, width=width, height=self.border)  # bottom border
        self.draw_rect(x=x_start, y=y_start + self.border, width=self.border,
                       height=y_start + height - self.border)  # left border
        self.draw_text(x=x_start + 5, y=y_start + 5, text=r.id)
