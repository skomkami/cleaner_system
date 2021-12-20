from model.model import RoomType

blue = "#285CBD"
celadon = "#00BFB2"
light_orange = "#FFCB58"
green = "#5A9E2F"
orange = "#FF9057"
yellow = "#F5F0AC"
light_gray = "#D3D3D3"
white = "#FFFFFF"


def get_color_for_room(r_type: RoomType):
    c = blue
    if r_type == RoomType.Administration: c = celadon
    if r_type == RoomType.LaboratoryRoom: c = light_orange
    if r_type == RoomType.Entrance: c = green
    if r_type == RoomType.LectureHall: c = orange
    if r_type == RoomType.Hall: c = yellow
    return c
