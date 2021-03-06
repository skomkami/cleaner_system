import random
import networkx as nx
import json
import sys
import time
import math
import os

import model.model
from model.model import Floor, RoomSimulation, RoomType, Cleaner
from drawer.simulation_drawer import SimulationDrawer
from typing import List


class Simulation:

    floor: Floor
    rooms: List[RoomSimulation]
    cleaners = []
    people_paths = []
    graph = None
    drawer: SimulationDrawer = None
    running = False
    weather_dirt_factor: float
    movement_counter = 20
    headless = False

    def __init__(self, floor, options):
        self.floor = floor
        self.rooms = self.floor.get_all_room_simulations()
        self.weather_dirt_factor = 0.1
        self.graph = self.create_floor_graph(self.rooms)
        self.source = None
        self.destination = None
        if '--headless' in options:
            self.headless = True
            print('running in headless mode')
        else:
            self.drawer = SimulationDrawer(floor)

    def create_floor_graph(self, rooms):
        graph = dict()
        for room in rooms:
            graph[room.id] = room.connected_to
        g = nx.DiGraph()
        g.add_nodes_from(graph.keys())
        for k, v in graph.items():
            g.add_edges_from(([(k, t) for t in v]))
            g.add_edges_from(([(t, k) for t in v]))
        return g

    def find_shortest_path(self, room1: str, room2: str):
        try:
            path = nx.shortest_path(self.graph, room1, room2)
        except Exception:
            return None
        return path

    def move_cleaners(self):
        for cleaner in self.cleaners:
            cleaner.move_along_path()

    def move_people(self):
        for path in self.people_paths:
            if len(path) < 2:
                path.pop(0)
                self.people_paths.remove(path)
            else:
                room1 = self.floor.get_room_simulation(path[0])
                room2 = self.floor.get_room_simulation(path[1])
                model.model.move_person(room1, room2)
                path.pop(0)

    def find_nearest_cleaner(self, room: str):
        nearest_rooms = list(nx.bfs_tree(self.graph, room))  # TODO maybe make this field in Room class
        for room2 in nearest_rooms:
            room3 = self.floor.get_room_simulation(room2)
            if room3.cleaners:
                cleaner = room3.prepare_cleaner_to_move()
                if cleaner:
                    path = self.find_shortest_path(room2, room)
                    cleaner.path = [self.floor.get_room_simulation(room) for room in path]
                    return cleaner
        return None

    def add_cleaner(self, room: str):
        room = self.floor.get_room_simulation(room)
        if room:
            cleaner = Cleaner(room.id)
            room.cleaners.append(cleaner)
            self.cleaners.append(cleaner)

    # Defines example of simulation
    def initialize_simulation(self):
        cleaner_possibilities = [room.id for room in self.rooms if (room.room_type in [RoomType.LaboratoryRoom,
                                                                 RoomType.LectureHall, RoomType.Administration])]
        cleaner_amount = math.ceil(len(cleaner_possibilities)/5)
        rooms_with_cleaner = random.sample(cleaner_possibilities, cleaner_amount)

        for room in rooms_with_cleaner:
            self.add_cleaner(room)
        source_possibilities = [room.id for room in self.rooms if (room.room_type in [RoomType.Entrance])]
        source = random.choice(source_possibilities)
        if len(source_possibilities) > 1:
            source_possibilities.remove(source)
        self.source = self.floor.get_room_simulation(source)
        destination = random.choice(source_possibilities)
        self.destination = self.floor.get_room_simulation(destination)
        self.source.people = 5

    def calculate_people_movement(self, rooms):
        if self.movement_counter > 0:
            self.movement_counter -= 1
            self.add_people()
        elif self.movement_counter > -10:
            self.movement_counter -= 1
        else:
            self.remove_people(rooms)

    def add_people(self):
        self.source.people = 5
        possibilities = [room for room in self.rooms if (room.room_type not in [RoomType.Entrance, RoomType.Toilet,
                                                                           RoomType.Hall])]
        destination = random.choice(possibilities)
        self.source.spawn_dirt(self.weather_dirt_factor)
        for i in range(5):
            path = self.find_shortest_path(self.source.id, destination.id)
            if path:
                self.people_paths.append(path)

    def remove_people(self, rooms):
        possibilities = [room for room in rooms if (room.room_type not in [RoomType.Entrance, RoomType.Toilet,
                                                                           RoomType.Hall] and room.people > 0)]
        if not possibilities:
            return
        room = random.choice(possibilities)
        for i in range(random.randint(2, 4)):
            path = self.find_shortest_path(room.id, self.destination.id)
            if path:
                self.people_paths.append(path)
            # path = self.find_shortest_path(room.id, 'tl')
            # if path:
            #    self.people_paths.append(path)

    def run_simulation(self):
        self.initialize_simulation()
        self.running = True
        step = 0
        simulation_save = []
        #prev_dest_people = 0
        while self.running:
            try:
                running = True
                # TODO cleaners movement rules
                for room in [room for room in self.rooms if room.people == 0 and room.room_type != RoomType.Hall and not room.cleaner_is_requested]:
                    if room.get_dirt_psqm() > 2.0:
                        cleaner = self.find_nearest_cleaner(room.id)
                        if cleaner:
                            room.cleaner_is_requested = True
                self.move_cleaners()
                self.move_people()
                self.calculate_people_movement(self.rooms)
                for room in self.rooms:
                    room.clean()
                    if room.dirt == 0 and len(room.busy_cleaners) > 0:
                        room.free_cleaners()
                values = dict()
                for room in self.rooms:
                    # 0 - cleaners, 1 - moving cleaners, 2 - busy cleaners, 3 - people, 4 - d
                    values[room.id] = [len(room.cleaners), len(room.moving_cleaners), len(room.busy_cleaners), room.people,
                                            round(room.get_dirt_psqm(), 2)]
                simulation_save.append(values)
                values = json.dumps(values)
                step += 1
                #prev_dest_people = self.destination.people
                if self.drawer and not self.headless:
                    running = self.drawer.draw_from_simulation(values)
                else:
                    print(step)
                    time.sleep(0.5)
                if self.movement_counter < 0:
                    self.destination.people = 0
                if not running:
                    raise KeyboardInterrupt
            except KeyboardInterrupt:
                output = dict()
                output['steps'] = simulation_save
                if not os.path.exists('cleaners_output'):
                    os.makedirs('cleaners_output')
                with open('cleaners_output/output.json', 'w+') as outfile:
                    json.dump(output, outfile)
                sys.exit(0)
