import math
import random
import player_class
import object_class
import weapons
from settings import *


class Gameplay:

    def __init__(self):
        self.player = player_class.Player((1, 1), 0, 1.5, 0.06, 100, ["default"])
        self.objects = [object_class.getObject("test", (5, 5), id="test"),
                        object_class.getObject("ammo", (3, 1), "default", 20, "first ammo")]
        self.phase = 0


    def mainLoop(self, dTime, mapArray):
        if self.phase == 0:
            if not object_class.getObjectByID("test", self.objects):
                self.phase = 1
                self.objects.append(object_class.getObject("ammo", (5, 5), "default", 20, "test ammo"))
                return
            if (self.player.activeWeapon.ownedAmmo == 0 and self.player.activeWeapon.ammo and
                    object_class.getObjectByID("test", self.objects).maxHealth != object_class.getObjectByID("test", self.objects).health and
                    not object_class.getObjectByID("spare ammo", self.objects)):
                self.objects.append(object_class.getObject("ammo", (3, 1), "default", 20, "spare ammo"))
            return
        elif self.phase == 1:
            if not object_class.getObjectByID("test ammo", self.objects):
                self.objects.append(object_class.getObject("spider", (1, 0)))
                self.objects.append(object_class.getObject("spider", (0, 1)))
                self.phase = 2
            return
        elif self.phase == 2:
            if not len(self.objects):
                self.objects.append(object_class.getObject("weapon", (1, 1), "rifle"))
                self.phase = 3
            return
        elif self.phase == 3:
            if not len(self.objects):
                self.objects.append(object_class.getObject("ammo", (self.player.position[0] + math.cos(self.player.direction) * 2, self.player.position[1] + math.sin(self.player.direction) * 2), "rifle", 10))
                self.phase = 4
            return
        elif self.phase == 4:
            if not len(self.objects):
                self.objects.append(object_class.getObject("giant", (1, 1)))
                self.phase = 5
        elif self.phase == 5:
            if self.player.activeWeapon.ownedAmmo == 0 and len(self.objects) == 1:
                self.objects.append(object_class.getObject("ammo", (random.randint(0, 6), random.randint(0, 6)), "rifle", 10))
