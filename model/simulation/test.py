from model.simulation.stats import *
from model.weather import WeatherState
from utils.dictionary import group

rooms_stats1 = [
    RoomStats('r1', no_visitors=15, coming_visitors=4, leaving_visitors=7, dirt_delta=0.4),
    RoomStats('r2', no_visitors=10, coming_visitors=8, leaving_visitors=5, dirt_delta=0.7)
]
time_stats1 = TimeWindowStats(WeatherState.Clear, group(rooms_stats1, lambda rs: rs.room_id))

rooms_stats2 = [
    RoomStats('r1', no_visitors=5, coming_visitors=2, leaving_visitors=3, dirt_delta=1.4),
    RoomStats('r2', no_visitors=4, coming_visitors=1, leaving_visitors=2, dirt_delta=1.1)
]
time_stats2 = TimeWindowStats(WeatherState.ThunderStorm, group(rooms_stats2, lambda rs: rs.room_id))

history = SimulationHistoryStats({
    TimeWindow(WeekDay.Thu, '12:00', '12:15'): rooms_stats1,
    TimeWindow(WeekDay.Thu, '12:15', '12:30'): rooms_stats2
})

print(history)