from dataclasses import dataclass
from enum import Enum
from typing import List
import json

DIRT_MOVEMENT_FACTOR = 0.1

class RoomType(str, Enum):
    LectureHall = 'LectureHall'
    LaboratoryRoom = 'LaboratoryRoom'
    Hall = 'Hall'
    Toilet = 'Toilet'
    Administration = 'Administration'
    Entrance = 'Entrance'

    def toJSON(self):
        return json.dumps(self, default=lambda x: x.value)

@dataclass
class Room:
    # position on pygame drawing
    id: str
    room_type: RoomType
    connected_to: List[str]
    pos_x: int
    pos_y: int
    width: int
    length: int
    room_center_x = 0
    room_center_y = 0

    def surface(self):
        return self.width * self.length

    def end_x(self):
        return self.pos_x+self.width

    def end_y(self):
        return self.pos_y+self.length

@dataclass
class RoomSimulation:
    id: str
    room_type: RoomType
    connected_to: List[str]
    cleaner_is_requested = False
    people = 0
    dirt = 0
    surface: int

    def __init__(self, id, room_type, connected_to, width, height):
        self.id = id
        self.room_type = RoomType(room_type)
        self.connected_to = connected_to
        self.surface = width * height
        self.cleaners = []
        self.moving_cleaners = []
        self.busy_cleaners = []

    def get_dirt_psqm(self):
        return self.dirt / self.surface

    def clean(self):
        self.dirt = max(0, self.dirt - 4 * len(self.busy_cleaners))
    
    def spawn_dirt(self, weather_dirt_factor: float):
        if self.room_type == RoomType.Entrance:
            new_dirt = self.people * weather_dirt_factor
            self.dirt = min(self.dirt + new_dirt, 500)
            # print("Spawning dirt in room", self.id, "in amount", new_dirt)

    def move_dirt_in(self, people_count: int, people_origin_dirtiness: float, id: str):
        new_dirt = DIRT_MOVEMENT_FACTOR *  people_count * people_origin_dirtiness
        # print("Moves dirt to room", self.id, "from", id, "new_dirt", new_dirt)
        self.dirt = min(self.dirt + new_dirt, 500)


    def prepare_cleaner_to_move(self):
        if self.cleaners:
            cleaner = self.cleaners.pop(0)
            self.moving_cleaners.append(cleaner)
            cleaner.status = CleanerStatus.Moving
            return cleaner
        else:
            return None

    def free_cleaners(self):
        self.cleaners = self.busy_cleaners
        self.busy_cleaners = []
        self.cleaner_is_requested = False


@dataclass
class Floor:
    level_no: int
    rooms: List[Room]
    room_simulations: List[RoomSimulation]

    def __init__(self, level_no, rooms):
        self.level_no = level_no
        self.rooms = [room[0] for room in rooms]
        self.room_simulations = [room[1] for room in rooms]

    def get_room(self, rid: str):
        return next((room for room in self.rooms if room.id == rid), None)

    def get_room_simulation(self, rid: str):
        return next((room for room in self.room_simulations if room.id == rid), None)

    def get_max_room_surface(self):
        return max(map(lambda r: r.surface(), self.rooms))

    def get_all_rooms(self):
        return self.rooms

    def get_all_room_simulations(self):
        return self.room_simulations

    def get_blocks_x(self):
        return max(map(lambda r: r.end_x(), self.rooms))

    def get_blocks_y(self):
        return max(map(lambda r: r.end_y(), self.rooms))


class CleanerStatus(str, Enum):
    Free = 'free'
    Moving = 'moving'
    Busy = 'busy'

    def toJSON(self):
        return json.dumps(self, default=lambda x: x.value)


class Cleaner:
    room: str
    status: CleanerStatus.Free
    path = []

    def __init__(self, room):
        self.room = room

    def __move_cleaner(self, room1: RoomSimulation, room2: RoomSimulation):
        if self in room1.moving_cleaners:
            room1.moving_cleaners.remove(self)
            room2.moving_cleaners.append(self)
            self.room = room2.id

    def move_along_path(self):
        if not self.path:
            return
        if len(self.path) == 1:
            if self.path[0].moving_cleaners:
                self.path[0].moving_cleaners.remove(self)
                self.path[0].busy_cleaners.append(self)
                self.status = CleanerStatus.Busy
                self.path = []
        elif len(self.path) > 1:
            self.__move_cleaner(self.path[0], self.path[1])
            self.path.pop(0)

def move_person(room1: RoomSimulation, room2: RoomSimulation):
    if room1.people > 0:
        room2.move_dirt_in(1, room1.dirt, room1.id)
        room1.people -= 1
        room2.people += 1
