import math
import random
import player_class
import object_class
import weapons
from settings import *


class Gameplay:

    def __init__(self):
        if MODE == "demo":
            self.player = player_class.Player((1, 1), 0, 1.5, 0.06, 100, ["default"])
            self.objects = [object_class.getObject("test", (5, 5), id="test"),
                            object_class.getObject("ammo", (3, 1), "default", 20, "first ammo"),
                            object_class.getObject("weapon", (3, 1), "default")]
            self.phase = 0
        elif MODE == "survival":
            self.player = player_class.Player((16, 16), 0, 1.5, 0.06, 100, ["hand gun", "rifle"])
            self.objects = [object_class.getObject("ammo", (18, 15), "hand gun", 20, "first ammo"),
                            object_class.getObject("ammo", (18, 17), "rifle", 8, "first ammo")]
            self.phase = "rest"
            self.wave = 15
            self.scores = {"spider": 1, "giant": 8}
            self.spawnRate = ["spider", "spider", "spider", "giant"]
        self.gameTime = 0
        self.lastObjectCount = len(self.objects)
        self.dead = []


    def mainLoop(self, dTime, mapArray, state):
        self.gameTime += dTime
        if MODE == "survival":
            waveDuration = 30
            if self.phase == "wave":
                if self.gameTime % waveDuration < 0:  # end wave
                    self.phase = "rest"
                if int(self.gameTime) != int(self.gameTime - dTime):  # once a second
                    if self.gameTime % (500 / (self.wave * DIFFICULTY)) < 1:  # every few seconds
                        enemy = random.choice(self.spawnRate)
                        dir = random.random() * math.pi * 2
                        dist = 5  # spawn distance from player
                        pos = (math.cos(dir) * dist + self.player.position[0], math.sin(dir) * dist + self.player.position[1])
                        self.objects.append(object_class.getObject(enemy, pos))
            elif self.phase == "rest":
                if 10 < self.gameTime % waveDuration < 11:  # start new wave
                    self.phase = "wave"
                    for _ in range(self.wave * DIFFICULTY // 10):
                        enemy = random.choice(self.spawnRate)
                        dir = random.random() * math.pi * 2
                        dist = 10  # spawn distance from player
                        pos = (math.cos(dir) * dist, math.sin(dir) * dist)
                        self.objects.append(object_class.getObject(enemy, pos))
            if self.dead:
                for object in self.dead:
                    if object.typ in ["ammo", "health", "weapon"]: continue
                    self.player.score += self.scores[object.typ] * self.wave * DIFFICULTY // 10
                    rand = random.random()
                    if rand > 10 / DIFFICULTY: continue
                    rand = random.random()
                    if rand < 1 - (2 / DIFFICULTY):
                        self.objects.append(object_class.getObject("ammo", object.pos, random.choice(self.player.ownedWeapons).name, DIFFICULTY, offset=False))
                    else:
                        self.objects.append(object_class.getObject("health", object.pos, 15, offset=False))
                self.dead = False
            if self.player.health <= 0:  # if dying, die
                return "defeat"
            self.lastObjectCount = len(self.objects)
            return state
        elif MODE == "demo":
            if self.player.health <= 0:
                self.player.score = 1000 / self.player.score
                return "defeat"
            if state == "running":
                self.player.score += dTime
            if self.phase == 0:
                if not object_class.getObjectByID("test", self.objects):
                    self.phase = 1
                    self.objects.append(object_class.getObject("ammo", (5, 5), "default", 20, "test ammo"))
                    return state
                if (self.player.activeWeapon.ownedAmmo == 0 and self.player.activeWeapon.ammo and
                        object_class.getObjectByID("test", self.objects).maxHealth != object_class.getObjectByID("test", self.objects).health and
                        not object_class.getObjectByID("spare ammo", self.objects)):
                    self.objects.append(object_class.getObject("ammo", (3, 1), "default", 20, "spare ammo"))
                return state
            elif self.phase == 1:
                if not object_class.getObjectByID("test ammo", self.objects):
                    self.objects.append(object_class.getObject("spider", (1, 0)))
                    self.objects.append(object_class.getObject("spider", (0, 1)))
                    self.phase = 2
                return state
            elif self.phase == 2:
                if not len(self.objects):
                    self.objects.append(object_class.getObject("weapon", (1, 1), "rifle"))
                    self.objects.append(object_class.getObject("health", (2, 1), 20))
                    self.phase = 3
                return state
            elif self.phase == 3:
                if not len(self.objects):
                    self.objects.append(object_class.getObject("ammo", (self.player.position[0] + math.cos(self.player.direction) * 2, self.player.position[1] + math.sin(self.player.direction) * 2), "rifle", 10))
                    self.phase = 4
                return state
            elif self.phase == 4:
                if not len(self.objects):
                    self.objects.append(object_class.getObject("giant", (1, 1)))
                    self.phase = 5
            elif self.phase == 5:
                if self.player.activeWeapon.ownedAmmo == 0 and len(self.objects) == 1:
                    self.objects.append(object_class.getObject("ammo", (random.randint(0, 6), random.randint(0, 6)), "rifle", 10))
                elif not len(self.objects):
                    self.objects.append(object_class.getObject("weapon", (1, 1), "rifle"))
                    self.phase = 6
            elif self.phase == 6:
                pass
            return state
