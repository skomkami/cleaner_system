import random
import networkx as nx
import time
import json
import sys

import model.model
from model.model import Floor, RoomSimulation, RoomType
from drawer.simulation_drawer import SimulationDrawer


class Simulation:

    floor: Floor
    cleaner_paths = []
    people_paths = []
    graph = None
    drawer: SimulationDrawer
    running = False

    def __init__(self, floor):
        self.floor = floor
        self.rooms = [RoomSimulation(room, 0) for room in self.floor.get_all_rooms()]
        floor.room_simulations = self.rooms
        self.drawer = SimulationDrawer(floor)
        self.graph = self.create_floor_graph(self.rooms)

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
        try:
            path = nx.shortest_path(self.graph, room1, room2)
        except Exception:
            return None
        return path

    def move_cleaners(self):
        for path in self.cleaner_paths:
            if not path:
                self.cleaner_paths.remove(path)
                continue
            if len(path) == 1:
                room = self.floor.get_room_simulation(path[0])
                if room.cleaners > 0:
                    room.cleaners -= 1
                    room.busy_cleaners += 1
                elif room.moving_cleaners > 0:
                    room.moving_cleaners -= 1
                    room.busy_cleaners += 1
            if len(path) < 2:
                self.cleaner_paths.remove(path)
            else:
                model.model.move_cleaner(self.floor.get_room_simulation(path[0]), self.floor.get_room_simulation(path[1]))
                path.pop(0)

    def move_people(self):
        for path in self.people_paths:
            if not path:
                self.people_paths.remove(path)
                continue
            if len(path) < 2:
                self.people_paths.remove(path)
            else:
                room1 = self.floor.get_room_simulation(path[0])
                room2 = self.floor.get_room_simulation(path[1])
                model.model.move_person(room1, room2)
                path.pop(0)

    def find_nearest_cleaner(self, room):
        nearest_rooms = list(nx.bfs_tree(self.graph, room))
        for room2 in nearest_rooms:
            if self.floor.get_room_simulation(room2).cleaners > 0:
                room3 = self.floor.get_room_simulation(room2)
                model.model.prepare_cleaner(room3)
                return self.find_shortest_path(room2, room)

    def add_cleaner(self, room):
        room = self.floor.get_room_simulation(room)
        if room:
            room.cleaners += 1

    def add_free_cleaner(self, room):
        room = self.floor.get_room_simulation(room)
        room.free_cleaners += 1

    #Defines example of simulation
    def initialize_simulation(self):
        rooms_with_cleaner = ['cs2', 'hr', 'w240', '214', '218', 'wc_3', '224']
        for room in rooms_with_cleaner:
            self.add_cleaner(room)

    # TODO people movement simulation
    def calculate_people_movement(self, rooms):
        room = random.choice([room for room in rooms if room.people > 0])
        for i in range(random.randint(2, 4)):
            path = self.find_shortest_path(room.room.id, 'stairway_1')
            if path:
                self.people_paths.append(path)
            path = self.find_shortest_path(room.room.id, 'tl')
            if path:
                self.people_paths.append(path)

    def run_simulation(self):
        self.initialize_simulation()
        self.running = True
        step = 0
        simulation_save = []
        while self.running:
            try:
                for room in self.rooms:
                    room.dirt += room.people
                self.calculate_people_movement(self.rooms)
                # TODO cleaners movement rules
                for room in [room for room in self.rooms if room.people == 0 and room.room.room_type != RoomType.Hall and not room.cleaner_is_requested]:
                    if room.get_dirt_psqm() > 5.0:
                        path = self.find_nearest_cleaner(room.room.id)
                        if path:
                            self.cleaner_paths.append(path)
                            room.cleaner_is_requested = True
                self.move_cleaners()
                self.move_people()
                for room in self.rooms:
                    room.clean()
                    if room.dirt == 0 and room.busy_cleaners > 0:
                        room.cleaners = room.busy_cleaners
                        room.busy_cleaners = 0
                values = dict()
                for room in self.rooms:
                    # 0 - cleaners, 1 - moving cleaners, 2 - busy cleaners, 3 - people, 4 - d
                    values[room.room.id] = [room.cleaners, room.moving_cleaners, room.busy_cleaners, room.people,
                                            round(room.get_dirt_psqm(), 2)]
                simulation_save.append(values)
                values = json.dumps(values)
                if self.drawer:
                    self.drawer.draw_from_simulation(values)
                step += 1
            except KeyboardInterrupt:
                # TODO better file write management
                # TODO better exit management
                output = dict()
                output['steps'] = simulation_save
                with open('output/output.json', 'w+') as outfile:
                    json.dump(output, outfile)
                sys.exit(0)
