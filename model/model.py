from dataclasses import dataclass
from enum import Enum
from typing import List


class RoomType(Enum):
    LectureHall = 'LectureHall'
    LaboratoryRoom = 'LaboratoryRoom'
    Hall = 'Hall'
    Toilet = 'Toilet'
    Administration = 'Administration'
    Entrance = 'Entrance'


@dataclass
class Room:
    id: str
    room_type: RoomType
    connected_to: List[str]
    # position on graph
    pos_x: int
    pos_y: int
    #
    room_center_x = 0
    room_center_y = 0
    width: int
    height: int

    def surface(self):
        return self.width * self.height

    def end_x(self):
        return self.pos_x+self.width

    def end_y(self):
        return self.pos_y+self.height


class RoomSimulation:

    room: Room
    cleaners = 0
    free_cleaners: int
    people = 5

    def __init__(self, room, cleaners):
        self.room = room
        self.cleaners = cleaners


@dataclass
class Floor:
    level_no: int
    rooms: List[Room]
    room_simulations: List[RoomSimulation] = None

    def get_room(self, rid: str):
        return next((room for room in self.rooms if room.id == rid), None)

    def get_room_simulation(self, rid: str):
        return next((room for room in self.room_simulations if room.room.id == rid), None)

    def get_max_room_surface(self):
        return max(map(lambda r: r.surface(), self.rooms))

    def get_all_rooms(self):
        return self.rooms

    def get_blocks_x(self):
        return max(map(lambda r: r.end_x(), self.rooms))

    def get_blocks_y(self):
        return max(map(lambda r: r.end_y(), self.rooms))


class Cleaner:
    location: Room


def move_person(room1, room2):
    if room1.people > 0:
        room1.people -= 1
        room2.people += 1


def move_cleaner(room1, room2):
    if room1.cleaners > 0:
        room1.cleaners -= 1
        room2.cleaners += 1
