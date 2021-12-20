from dataclasses import dataclass, field
from enum import Enum

from typing import List, Optional


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
    '''
    Room surface in m^2
    '''
    surface: float
    room_type: RoomType
    connected_to: List[str]
    # position on graph
    pos_x: Optional[int]
    pos_y: Optional[int]
    cleaners = 1
    people = 1


@dataclass
class Floor:
    level_no: int
    rooms: List[Room]

    def get_room(self, rid: str):
        return next((room for room in self.rooms if room.id == rid), None)

    def get_max_room_surface(self):
        return max(map(lambda r: r.surface, self.rooms))

    def get_all_rooms(self):
        return self.rooms


def move_person(room1, room2):
    if room1.people > 0:
        room1.people -= 1
        room2.people += 1


def move_cleaner(room1, room2):
    if room1.cleaners > 0:
        room1.cleaners -= 1
        room2.cleaners += 1
