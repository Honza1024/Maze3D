import player_class
import object_class
import weapons
from settings import *


def start():
    player = player_class.Player((1, 1), 0, 1.5, 0.06, 100, ["default"])
    objects = []
    objects.append(object_class.getObject("test", (3, 1), "default"))
    return player, objects
