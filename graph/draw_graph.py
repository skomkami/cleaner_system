from drawer.room_drawer import RoomDrawer
from graph.level_graph import LevelGraph
from model.model import Floor
import pydotplus as pdp


def draw_floor(floor: Floor, drawer: RoomDrawer):

    for room in floor.rooms:
        drawer.draw_room(room)
