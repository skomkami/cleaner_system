from model.schedule.schedule import Meeting, WeekDay, Schedule, Time

meetings = [
    Meeting('1', WeekDay.Mon, '16:00', '17:00', 15),
    Meeting('1', WeekDay.Thu, '17:30', '18:30', 12),
    Meeting('1', WeekDay.Thu, '18:30', '20:00', 13),
    Meeting('2', WeekDay.Mon, '16:00', '18:00', 15),
    Meeting('2', WeekDay.Mon, '18:00', '20:00', 16),
]

time: Time = '25:00'
schedule = Schedule(meetings)

search_meeting = schedule.get_meeting_for('1', WeekDay.Thu, '18:00')

print(search_meeting)

print(schedule.schedule)
