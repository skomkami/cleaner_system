import pygame
from drawer.rectangle import Rectangle
from drawer.drawer import Drawer
from model.model import Room
from drawer.color import *


def overlapping_center(s1: int, e1: int, s2: int, e2: int):
    max_s = max(s1, s2)
    min_e = min(e1, e2)
    # print(f"s1: {s1}, e1: {e1}, s2: {s2}, e2: {e2}, center: {(max_s + min_e) / 2}")
    return (max_s + min_e) / 2


class RoomDrawer(Drawer):
    def __init__(self, pygame_screen: pygame.Surface, drawing_area: Rectangle, border_width: int, blocks_x: int,
                 blocks_y: int):
        super().__init__(pygame_screen, drawing_area)
        self.border = border_width
        self.block_w = self.area.width / blocks_x
        self.block_h = self.area.height / blocks_y
        self.font = pygame.freetype.SysFont("Comic Sans MS", 24)

    def draw_room(self, r: Room):
        room_color = pygame.Color(get_color_for_room(r.room_type))
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
        self.draw_text(self.font, x=x_start + 10, y=y_start + 10, text=r.id)

    def draw_connection(self, r1: Room, r2: Room):
        conn_color = pygame.Color(light_gray)
        conn_wdh = 24  # connection width
        conn_len = 12
        if r1.pos_x < r2.end_x() and r1.end_x() > r2.pos_x:
            conn_x_pos = overlapping_center(r1.pos_x, r1.end_x(), r2.pos_x, r2.end_x()) * self.block_w
            conn_y_pos = r1.end_y() * self.block_h
            if r1.pos_y > r2.pos_y:
                conn_y_pos = r1.pos_y * self.block_h
            self.draw_rect(conn_x_pos - conn_wdh // 2, conn_y_pos - conn_len // 2, conn_wdh, conn_len, conn_color)
        elif r1.pos_y < r2.end_y() and r1.end_y() > r2.pos_y:
            conn_y_pos = overlapping_center(r1.pos_y, r1.end_y(), r2.pos_y, r2.end_y()) * self.block_h
            conn_x_pos = r1.end_x() * self.block_w
            if r1.pos_x > r2.pos_x:
                conn_x_pos = r1.pos_x * self.block_w
            self.draw_rect(conn_x_pos - conn_len // 2, conn_y_pos - conn_wdh // 2, conn_len, conn_wdh, conn_color)
        else:
            print(f'Rooms {r1.id} and {r2.id} are not connected!')
