from drawer.drawer import Drawer
import pygame
import pygame.freetype as ft

from drawer.rectangle import Rectangle
from drawer.color import *


class LegendDrawer(Drawer):
    def __init__(self, pygame_screen: pygame.Surface, drawing_area: Rectangle):
        super().__init__(pygame_screen, drawing_area)
        self.big_font = ft.SysFont("Comic Sans MS", 32)
        self.reg_font = ft.SysFont("Comic Sans MS", 18)

    def draw(self):
        self.draw_text(self.big_font, 30, 30, text="Legend", color=white)
        self.draw_colors()

    def draw_colors(self):
        col_width = 300
        row_height = 45
        top_padding = 80  # take into account lettering "Legend"
        row_items = (self.area.height - top_padding) // row_height
        for idx, r_tpe in enumerate(RoomType):
            y = top_padding + (idx % row_items) * row_height
            col = idx // row_items
            x = col * col_width + 30
            self.draw_rect(x, y, 30, 30, get_color_for_room(r_tpe))
            self.draw_text(self.reg_font, x + 40, y + 8, text=r_tpe.value, color=white)
