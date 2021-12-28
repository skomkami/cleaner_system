import pygame
import json
import sys

from drawer.draw_floor import draw_floor
from drawer.legend_drawer import LegendDrawer
from drawer.room_drawer import RoomDrawer
from drawer.rectangle import Rectangle
from drawer.timer_drawer import TimerDrawer
from model.model import Floor


class SimulationDrawer:

    rect_size = 25
    img_height = 800
    img_width = 1500
    screen = pygame.display.set_mode((img_width, img_height))
    color_red = (255, 0, 0)
    color_blue = (0, 0, 255)
    color_green = (0, 255, 0)
    color_yellow = (255, 255, 0)
    BLACK = (0, 0, 0)
    floor: Floor
    room_drawer: RoomDrawer
    timer_width = 250

    def __init__(self, floor):
        pygame.init()
        self.floor = floor
        self.room_drawer = RoomDrawer(
            self.screen,
            Rectangle(0, 0, self.img_width, self.img_height - 200),
            border_width=2,
            blocks_x=self.floor.get_blocks_x(),
            blocks_y=self.floor.get_blocks_y()
        )
        self.legend_drawer = LegendDrawer(self.screen, Rectangle(self.timer_width, 600, self.img_width - 150, 200))
        self.timer_drawer = TimerDrawer(self.screen, Rectangle(0, 600, self.timer_width, 200))
        self.rooms = [room for room in self.floor.get_all_rooms()]
        self.font = pygame.font.SysFont('Arial', 12)
        self.running = True

    def draw_from_file(self, filepath):
        save = None
        # TODO Exception handling here
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                save = json.load(f)
        except Exception:
            pass
        save = save['steps']
        for step in save:
            self.draw_frame(step)

    def draw_from_simulation(self, frame):
        frame = json.loads(frame)
        self.draw_frame(frame)

    def draw_frame(self, frame):
        if not self.running:
            return
        pygame.time.wait(500)
        self.screen.fill(self.BLACK)
        self.legend_drawer.draw()
        self.timer_drawer.tick_and_draw()
        draw_floor(self.floor, self.room_drawer)
        room_names = frame.keys()
        for room in room_names:
            room_stats = frame[room] # 0 - cleaners, 1 - moving cleaners, 2 - busy cleaners, 3 - people, 4 - dirt
            room = self.floor.get_room(room)
            if room_stats[0] > 0 or room_stats[1] > 0:
                rect = pygame.Rect(room.pos_x - 15, self.img_height - room.pos_y - 15, self.rect_size,
                                   self.rect_size)
                rect.center = (room.room_center_x + 15, room.room_center_y - 15)
                pygame.draw.rect(self.screen, self.color_red, rect)
                text = self.font.render(str(room_stats[0] + room_stats[1]), True, self.BLACK)
                text_rect = text.get_rect()
                text_rect.center = rect.center
                self.screen.blit(text, text_rect)
            if room_stats[2] > 0:
                rect = pygame.Rect(room.pos_x - 15, self.img_height - room.pos_y - 15, self.rect_size,
                                   self.rect_size)
                rect.center = (room.room_center_x + 15, room.room_center_y + 15)
                pygame.draw.rect(self.screen, self.color_blue, rect)
                text = self.font.render(str(room_stats[2]), True, self.BLACK)
                text_rect = text.get_rect()
                text_rect.center = rect.center
                self.screen.blit(text, text_rect)
            if room_stats[3] > 0:
                rect2 = pygame.Rect(room.pos_x, self.img_height - room.pos_y - 15, self.rect_size,
                                    self.rect_size)
                rect2.center = (room.room_center_x - 15, room.room_center_y - 15)
                pygame.draw.rect(self.screen, self.color_green, rect2)
                text2 = self.font.render(str(room_stats[3]), True, self.BLACK)
                text_rect2 = text2.get_rect()
                text_rect2.center = rect2.center
                self.screen.blit(text2, text_rect2)
            rect3 = pygame.Rect(room.pos_x, self.img_height - room.pos_y - 15, self.rect_size, self.rect_size)
            rect3.center = (room.room_center_x - 15, room.room_center_y + 15)
            pygame.draw.rect(self.screen, self.color_yellow, rect3)
            text3 = self.font.render(str(room_stats[4]), True, self.BLACK)
            text_rect3 = text3.get_rect()
            text_rect3.center = rect3.center
            self.screen.blit(text3, text_rect3)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                self.running = False
                sys.exit(0)



