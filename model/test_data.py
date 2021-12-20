from model.model import Room, RoomType, Floor

cs1 = Room(id='cs1', connected_to=['cs2'], surface=20, room_type=RoomType.Hall, pos_x=None, pos_y=None)
cs2 = Room(id='cs2', connected_to=['cs3'], surface=20, room_type=RoomType.Hall, pos_x=None, pos_y=None)
cs3 = Room(id='cs3', connected_to=['cs4'], surface=20, room_type=RoomType.Hall, pos_x=None, pos_y=None)
cs4 = Room(id='cs4', connected_to=[], surface=20, room_type=RoomType.Hall, pos_x=None, pos_y=None)
r1 = Room(id='r1', connected_to=['cs1'], surface=30.5, room_type=RoomType.LaboratoryRoom, pos_x=None, pos_y=None)
r2 = Room(id='r2', connected_to=['cs1'], surface=24.5, room_type=RoomType.LaboratoryRoom, pos_x=None, pos_y=None)
r3 = Room(id='r3', connected_to=['cs2', 'r4'], surface=31, room_type=RoomType.LaboratoryRoom, pos_x=None, pos_y=None)
r4 = Room(id='r4', connected_to=['cs2'], surface=33, room_type=RoomType.LaboratoryRoom, pos_x=None, pos_y=None)
r5 = Room(id='r5', connected_to=['cs2'], surface=36, room_type=RoomType.LaboratoryRoom, pos_x=None, pos_y=None)
r6 = Room(id='r6', connected_to=['cs2'], surface=22, room_type=RoomType.LaboratoryRoom, pos_x=None, pos_y=None)
r7 = Room(id='r7', connected_to=['cs3', 'r8'], surface=11, room_type=RoomType.LaboratoryRoom, pos_x=None, pos_y=None)
r8 = Room(id='r8', connected_to=['cs3'], surface=80, room_type=RoomType.LectureHall, pos_x=None, pos_y=None)
r9 = Room(id='r9', connected_to=['cs3'], surface=60, room_type=RoomType.LectureHall, pos_x=None, pos_y=None)
t1 = Room(id='t1', connected_to=['cs4'], surface=15, room_type=RoomType.Toilet, pos_x=None, pos_y=None)
t2 = Room(id='t2', connected_to=['cs4'], surface=12, room_type=RoomType.Toilet, pos_x=None, pos_y=None)

floor0 = Floor(level_no=0, rooms=[cs1, cs2, cs3, cs4, r1, r2, r3, r4, r5, r6, r7, r8, r9, t1, t2])
