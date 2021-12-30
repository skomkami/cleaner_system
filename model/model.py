from dataclasses import dataclass
from enum import Enum
from typing import List
import json


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
    cleaner_is_requested = False
    people = 5
    dirt = 0

    def __init__(self, id, room_type, connected_to, pos_x, pos_y, width, height):
        self.id = id
        self.room_type = RoomType(room_type)
        self.connected_to = connected_to
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.cleaners = []
        self.moving_cleaners = []
        self.busy_cleaners = []

    def surface(self):
        return self.width * self.height

    def end_x(self):
        return self.pos_x+self.width

    def end_y(self):
        return self.pos_y+self.height

    def get_dirt_psqm(self):
        return self.dirt/self.surface()

    def clean(self):
        self.dirt = max(0, self.dirt - 4 * len(self.busy_cleaners))

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

    def get_room(self, rid: str):
        return next((room for room in self.rooms if room.id == rid), None)

    def get_max_room_surface(self):
        return max(map(lambda r: r.surface(), self.rooms))

    def get_all_rooms(self):
        return self.rooms

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

    def __move_cleaner(self, room1: Room, room2: Room):
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


def move_person(room1, room2):
    if room1.people > 0:
        room1.people -= 1
        room2.people += 1
