import decimal
import random

from model.time import WeekDay


class RandomLstmInput:
    def __init__(self, time_step: int, rooms_no: int):
        # time step in minutes
        self.time_step = time_step
        self.rooms_no = rooms_no

    def generate(self):
        # minutes in day
        with open("random_dirt_values.csv", 'w', encoding='utf-8') as f:
            f.write("time,room1,room2,room3\n")
            end_time = 24 * 60
            for weekday in WeekDay:
                curr_time = 0
                while curr_time < end_time:
                    hour = curr_time // 60
                    minute = curr_time % 60
                    day_time = "{} {:02d}:{:02d}".format(str(weekday), hour, minute)
                    # print(date, end=",")
                    rooms_dirt = []
                    for i in range(0, self.rooms_no):
                        # more dirt before wednesday
                        dirt_delta_in_room = 0
                        if weekday.value < 3:
                            dirt_delta_in_room = float(decimal.Decimal(random.randrange(300, 500)) / 1000)
                        else:
                            dirt_delta_in_room = float(decimal.Decimal(random.randrange(50, 200)) / 1000)
                        rooms_dirt.append(dirt_delta_in_room)
                    rooms_dirt_str = ' '.join([str(dirt) for dirt in rooms_dirt])
                    f.write("{},{}\n".format(day_time, rooms_dirt_str))
                    curr_time += self.time_step


rli = RandomLstmInput(15, 3)
rli.generate()
