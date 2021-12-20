from drawer.room_drawer import RoomDrawer
from model.model import Floor


def draw_floor(floor: Floor, drawer: RoomDrawer):

    for room in floor.rooms:
        drawer.draw_room(room)
    for room in floor.rooms:
        for connection in room.connected_to:
            connected_room = floor.get_room(connection)
            drawer.draw_connection(room, connected_room)
