from model.model import Room, RoomType, Floor

hl = Room(id='hl', connected_to=['cs1'], room_type=RoomType.Hall, pos_x=0, pos_y=0, width=4, height=9)
cs1 = Room(id='cs1', connected_to=['cs2'], room_type=RoomType.Hall, pos_x=4, pos_y=4, width=3, height=2)
cs2 = Room(id='cs2', connected_to=['cs3'], room_type=RoomType.Hall, pos_x=7, pos_y=4, width=3, height=2)
cs3 = Room(id='cs3', connected_to=['cs4'], room_type=RoomType.Hall, pos_x=10, pos_y=4, width=3, height=2)
cs4 = Room(id='cs4', connected_to=['cs5'], room_type=RoomType.Hall, pos_x=13, pos_y=4, width=3, height=2)
cs5 = Room(id='cs5', connected_to=['hr'], room_type=RoomType.Hall, pos_x=16, pos_y=4, width=3, height=2)
hr = Room(id='hr', connected_to=['w240'], room_type=RoomType.Hall, pos_x=19, pos_y=4, width=5, height=5)

r224 = Room(id='r224', connected_to=['cs1'], room_type=RoomType.LaboratoryRoom, pos_x=4, pos_y=0, width=4, height=4)
r228 = Room(id='r228', connected_to=['cs2'], room_type=RoomType.LaboratoryRoom, pos_x=8, pos_y=0, width=4, height=4)
r232 = Room(id='r232', connected_to=['cs3'], room_type=RoomType.LaboratoryRoom, pos_x=12, pos_y=0, width=4, height=4)
w240 = Room(id='w240', connected_to=[], room_type=RoomType.LectureHall, pos_x=16, pos_y=0, width=8, height=4)

tl = Room(id='tl', connected_to=['hl'], room_type=RoomType.Toilet, pos_x=4, pos_y=6, width=2, height=3)
r208 = Room(id='r208', connected_to=['cs1'], room_type=RoomType.LaboratoryRoom, pos_x=6, pos_y=6, width=4, height=3)
r212 = Room(id='r212', connected_to=['cs2'], room_type=RoomType.LaboratoryRoom, pos_x=10, pos_y=6, width=3, height=3)
r216 = Room(id='r216', connected_to=['cs3'], room_type=RoomType.LaboratoryRoom, pos_x=13, pos_y=6, width=3, height=3)
tr = Room(id='tr', connected_to=['hr'], room_type=RoomType.Toilet, pos_x=16, pos_y=6, width=3, height=3)

floor0 = Floor(level_no=0, rooms=[hl, cs1, cs2, cs3, cs4, cs5, hr, r224, r228, r232, w240, tl, r208, r212, r216, tr])