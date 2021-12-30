from dataclasses import dataclass
from typing import Dict

from model.time import WeekDay, Time
from model.weather import WeatherState


@dataclass
class TimeWindow:
    weekday: WeekDay
    start: Time
    end: Time

    def __key(self):
        return self.weekday, self.start, self.end

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, TimeWindow):
            return self.__key() == other.__key()
        return NotImplemented


@dataclass
class RoomStats:
    room_id: str
    no_visitors: int
    coming_visitors: int
    leaving_visitors: int
    dirt_delta: float


@dataclass
class TimeWindowStats:
    weather: WeatherState
    rooms_states: Dict[str, RoomStats]


@dataclass
class SimulationHistoryStats:
    state: Dict[TimeWindow, TimeWindowStats]
