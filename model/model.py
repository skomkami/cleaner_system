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


@dataclass
class Floor:
    level_no: int
    rooms: List[Room]

    def getRoom(self, rid: str):
        return next((room for room in self.rooms if room.id == rid), None)
