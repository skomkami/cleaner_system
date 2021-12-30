from dataclasses import dataclass
import re
from typing import List
from utils.dictionary import group
from enum import IntEnum


class WeekDay(IntEnum):
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
    Sun = 7


class Time:
    def __get__(self, obj):
        self.value

    def __set__(self, obj, value):
        pattern = re.compile("^[0-2][0-3]:[0-5][0-9]$")
        match_result = pattern.match(value)
        if match_result is None:
            raise ValueError(value + " is not a valid time. Please use format HH:mm.")
        self.value = value

    # def __init__(self, time: str):
    #     pattern = re.compile("^[0-2][0-3]:[0-5][0-9]$")
    #     match_result = pattern.match(time)
    #     if match_result is None:
    #         raise ValueError(time + " is not a valid time. Please use format HH:mm.")
    #     self.value = time

    def __eq__(self, other):
        return self.value == other.t

    def __ne__(self, other):
        return self.value != other.t

    def __gt__(self, other):
        return self.value > other.t

    def __lt__(self, other):
        return self.value < other.t

    def __le__(self, other):
        return self.value <= other.t

    def __ge__(self, other):
        return self.value >= other.t


@dataclass
class Meeting:
    room_id: str
    weekday: WeekDay
    start: Time
    end: Time
    expectedNoPeople: int


class Schedule:

    # room_id -> weekday -> [Meeting]
    def __init__(self, meetings_list: List[Meeting]):
        roomsSchedules = group(meetings_list, key=lambda m: m.room_id)

        self.schedule = dict()
        for room_id, room_schedule in roomsSchedules.items():
            weekdays_schedule = group(room_schedule, key=lambda m: m.weekday)
            self.schedule.setdefault(room_id, weekdays_schedule)

    def get_meeting_for(self, room_id: str, weekday: WeekDay, time: Time):
        room_day_schedule = self.schedule.get(room_id).get(weekday)
        for meeting in room_day_schedule:
            if meeting.start >= time >= meeting.end:
                return meeting
        return None
