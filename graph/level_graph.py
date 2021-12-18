import pygraphviz as pgv
from model.model import Room, RoomType


class LevelGraph(pgv.AGraph):
    def __init__(self, *args):
        super(LevelGraph, self).__init__(strict=False, directed=False, *args)
        # self.graph_attr['rankdir'] = 'LR'
        # self.node_attr['shape'] = 'Mrecord'
        self.graph_attr['splines'] = 'ortho'
        self.graph_attr['nodesep'] = '0.7'
        # self.graph_attr['size'] = '4,8!'
        self.node_attr['style'] = 'filled'
        self.edge_attr.update(penwidth='2')

    def add_room(self, r: Room, max_r_surface: float):
        color = "#285CBD"
        if r.room_type == RoomType.Administration:
            color = "#00BFB2"
        if r.room_type == RoomType.LaboratoryRoom:
            color = "#FFCB58"
        if r.room_type == RoomType.Entrance:
            color = "#5A9E2F"
        if r.room_type == RoomType.LectureHall:
            color = "#FF9057"
        if r.room_type == RoomType.Hall:
            color = "#F5F0AC"

        size = r.surface / max_r_surface

        # use label instead of xlabel to print id inside room
        super(LevelGraph, self).add_node(r.id, shape="circle", label="", xlabel=r.id, penwidth='3',  width=size, height=size,
                                         fillcolor=color)

    def add_pass(self, r1: str, r2: str):
        super(LevelGraph, self).add_edge(r1, r2)
