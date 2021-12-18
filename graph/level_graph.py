import pygraphviz as pgv
import graphviz as gv
from model.model import Room, RoomType


class LevelGraph(pgv.AGraph):
    def __init__(self, *args):
        super(LevelGraph, self).__init__(strict=False, directed=False, *args)
        # self.graph_attr['rankdir'] = 'LR'
        self.node_attr['shape'] = 'Mrecord'
        self.graph_attr['splines'] = 'ortho'
        self.graph_attr['nodesep'] = '0.8'
        # self.graph_attr['size'] = '4,8!'
        self.node_attr['style'] = 'filled'
        self.edge_attr.update(penwidth='2')

    def add_room(self, r: Room):
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

        super(LevelGraph, self).add_node(r.id, shape="circle", label=r.id, penwidth='3',  width=".7", height=".7",
                                         fillcolor=color)

    def add_pass(self, r1: str, r2: str):
        super(LevelGraph, self).add_edge(r1, r2)
