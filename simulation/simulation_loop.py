import pygame
import copy
import networkx as nx

import model.model
from drawer.draw_floor import draw_floor
from drawer.legend_drawer import LegendDrawer
from drawer.room_drawer import RoomDrawer
from drawer.rectangle import Rectangle
from model.model import Floor, RoomSimulation


class Simulation:

    rect_size = 25
    img_height = 800
    img_width = 1500
    screen = pygame.display.set_mode((img_width, img_height))
    color_red = (255, 0, 0)
    color_green = (0, 255, 0)
    floor: Floor
    BLACK = (0, 0, 0)
    cleaner_paths = []
    graph = None

    def create_floor_graph(self, rooms):
        graph = dict()
        for room in rooms:
            graph[room.room.id] = room.room.connected_to
        g = nx.DiGraph()
        g.add_nodes_from(graph.keys())
        for k, v in graph.items():
            g.add_edges_from(([(k, t) for t in v]))
            g.add_edges_from(([(t, k) for t in v]))
        return g

    def find_shortest_path(self, room1, room2):
        path = nx.shortest_path(self.graph, room1, room2)
        return path

    def move_cleaners(self):
        for path in self.cleaner_paths:
            if len(path) < 2:
                self.cleaner_paths.remove(path)
            else:
                model.model.move_cleaner(self.floor.get_room_simulation(path[0]), self.floor.get_room_simulation(path[1]))
                path.pop(0)

    def find_nearest_cleaner(self, room):
        nearest_rooms = list(nx.bfs_tree(self.graph, room))
        for room2 in nearest_rooms:
            if self.floor.get_room_simulation(room2).cleaners > 0:
                return self.find_shortest_path(room2, room)

    def add_cleaner(self, room):
        room = self.floor.get_room_simulation(room)
        room.cleaners += 1

    def run_simulation(self, floor):
        rooms_with_cleaner = ['cs2', 'hr', 'w240']
        self.floor = floor
        running = True
        pygame.init()
        font = pygame.font.SysFont('Arial', 12)
        rooms = [RoomSimulation(room, 0) for room in self.floor.get_all_rooms()]
        floor.room_simulations = rooms
        for room in rooms_with_cleaner:
            self.add_cleaner(room)
        self.graph = self.create_floor_graph(rooms)
        step = 0
        room_drawer = RoomDrawer(
            self.screen,
            Rectangle(0, 0, self.img_width, self.img_height - 200),
            border_width=2,
            blocks_x=self.floor.get_blocks_x(),
            blocks_y=self.floor.get_blocks_y()
        )
        legend_drawer = LegendDrawer(self.screen, Rectangle(0, 600, self.img_width, 200))
        #path = self.find_shortest_path('cs2', 'w240')
        path = self.find_nearest_cleaner('tl')
        print(path)
        self.cleaner_paths.append(path)
        while running:
            draw_floor(self.floor, room_drawer)
            legend_drawer.draw()
            # if step == 1:
            #     move_cleaner(floor0.get_room('r5'), floor0.get_room('cs2'))
            # if step == 2:
            #     move_cleaner(floor0.get_room('cs2'), floor0.get_room('r6'))
            for room in rooms:
                if room.cleaners > 0:
                    rect = pygame.Rect(room.room.pos_x - 15, self.img_height - room.room.pos_y, self.rect_size, self.rect_size)
                    rect.center = (room.room.room_center_x + 15, room.room.room_center_y)
                    pygame.draw.rect(self.screen, self.color_red, rect)
                    text = font.render(str(room.cleaners), True, self.BLACK)
                    text_rect = text.get_rect()
                    text_rect.center = rect.center
                    self.screen.blit(text, text_rect)
                if room.people > 0:
                    rect2 = pygame.Rect(room.room.pos_x, self.img_height - room.room.pos_y, self.rect_size, self.rect_size)
                    rect2.center = (room.room.room_center_x - 15, room.room.room_center_y)
                    pygame.draw.rect(self.screen, self.color_green, rect2)
                    text2 = font.render(str(room.people), True, self.BLACK)
                    text_rect2 = text2.get_rect()
                    text_rect2.center = rect2.center
                    self.screen.blit(text2, text_rect2)
            self.move_cleaners()
            step_text = font.render(str(step), True, self.BLACK)
            stepRectD = step_text.get_rect()
            stepRectD.topleft = (5, 500)
            self.screen.blit(step_text, stepRectD)
            pygame.display.update()
            step += 1
            pygame.time.delay(1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
