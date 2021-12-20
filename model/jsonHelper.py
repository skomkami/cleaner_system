from model.model import Floor, Room
import json

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

def loader(obj):
    if 'level_no' in obj:
        return Floor(obj['level_no'],obj['rooms'])
    return Room(obj['id'],obj['surface'],obj['room_type'],obj['connected_to'],obj['pos_x'],obj['pos_y'])

def fromFile(filePath):
    with open(filePath,'r', encoding='utf-8') as f:
        return json.load(f, object_hook=loader)

def toFile(obj,filePath):
    with open(filePath,'w', encoding='utf-8') as f:
        json.dump(obj, f, default=dumper, indent=2)
    