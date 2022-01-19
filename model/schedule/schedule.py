from dataclasses import dataclass
from typing import List

from model.time import WeekDay, Time
from utils.dictionary import group


@dataclass
class Meeting:
    room_id: str
    weekday: WeekDay
    # TODO KS rozważyć użycie datetime.time - tylko tam z kolei są nadmiarowe dla nas informacje, tj. sekundy, milisekundy i timezone
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
