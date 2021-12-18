from graph.level_graph import LevelGraph
from model.model import Floor
import pydotplus as pdp


def draw_floor(floor: Floor, filename: str):
    graph = LevelGraph()

    for room in floor.rooms:
        graph.add_room(room)
    for room in floor.rooms:
        for connection in room.connected_to:
            graph.add_pass(room.id, connection)

    graph.draw(filename, prog="dot")
    g = graph.draw(prog="dot")
    parsed = pdp.parse_dot_data(g)
    nodes = parsed.obj_dict['nodes']

    dpi = 4 / 3
    for room in floor.rooms:
        pos: str = nodes[room.id][0]['attributes']['pos']
        (x, y) = map(lambda s: int(float(s)), pos.replace('"', '').split(",", maxsplit=1))
        room.pos_x = x * dpi
        room.pos_y = y * dpi
