from enum import IntEnum
import re


class WeekDay(IntEnum):
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
    Sun = 7

    def __str__(self):
        return self.name


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
