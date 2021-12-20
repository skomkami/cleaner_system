import pygame
from drawer.rectangle import Rectangle


class Drawer:
    def __init__(self, pygame_screen: pygame.Surface, drawing_area: Rectangle):
        self.pygame_screen = pygame_screen
        self.area = drawing_area

    def draw_rect(self, x: int, y: int, width: int, height: int, color: pygame.Color = pygame.Color(0, 0, 0)):
        rect = pygame.Rect(x + self.area.start_x, self.area.start_y + y, width, height)
        pygame.draw.rect(self.pygame_screen, color, rect)

    def draw_text(self, font, x: int, y: int, text: str,
                  color: pygame.Color = pygame.Color(0, 0, 0)):
        font.render_to(self.pygame_screen, (x+self.area.start_x, y+self.area.start_y), text, color)
