from datetime import datetime, timedelta
import pygame
from drawer.color import *
from drawer.drawer import Drawer
from drawer.rectangle import Rectangle


class TimerDrawer(Drawer):
    def __init__(self, pygame_screen: pygame.Surface, drawing_area: Rectangle):
        super().__init__(pygame_screen, drawing_area)
        self.big_font = pygame.freetype.SysFont("Comic Sans MS", 32)
        self.reg_font = pygame.freetype.SysFont("Comic Sans MS", 24)
        self.date = datetime.today()

    def tick_and_draw(self):
        self.draw_text(self.big_font, 30, 30, text="Timer", color=white)
        self.date = self.date + timedelta(minutes=5)
        date_str = self.date.strftime("%a %H:%M")
        self.draw_rect(30, 80, 250, 50)
        self.draw_text(self.reg_font, 30, 80, text=date_str, color=white)
