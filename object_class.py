import math
import copy
import draw
import mapa
from settings import *


class Object:

    def __init__(self, typ, sprite, health=0, speed=0., damage=0, retreat=0.):
        self.typ = typ
        self.pos = [0, 0]
        self.sprite = sprite
        self.health = health
        self.maxHealth = health
        self.speed = speed
        self.damage = damage
        self.retreat = retreat
        self.thickness = len(sprite.mask) * sprite.scale / 1000


    def move(self, dTime, player, mapArray, objects):
        relX = self.pos[0] - player.position[0]
        relY = self.pos[1] - player.position[1]
        dist = math.sqrt(relX ** 2 + relY ** 2)
        relX /= dist
        relY /= dist
        if self.typ in ["giant", "spider"]:  # go towards player
            self.pos[0] -= relX * self.speed * dTime
            self.pos[1] -= relY * self.speed * dTime
        if dist < player.thickness + self.thickness:  # attack
            player.health -= self.damage
            self.pos[0] += relX * self.speed * self.retreat
            self.pos[1] += relY * self.speed * self.retreat
        for object in objects:  # collision with other objects
            relX = self.pos[0] - object.pos[0]
            relY = self.pos[1] - object.pos[1]
            if object is self: continue
            if abs(relX) > 1 or abs(relY) > 1: continue
            if relX == 0: self.pos[0] += 0.1
            if relY == 0: self.pos[1] += 0.1
            dist = math.sqrt(relX ** 2 + relY ** 2)
            if dist < 0.1: dist = 0.141
            if dist < self.thickness + object.thickness:
                relX /= dist
                relY /= dist
                self.pos[0] += relX * (self.thickness + object.thickness - dist) / 2
                self.pos[1] += relX * (self.thickness + object.thickness - dist) / 2
                object.pos[0] -= relX * (self.thickness + object.thickness - dist) / 2
                object.pos[1] -= relX * (self.thickness + object.thickness - dist) / 2
        if self.typ in ["giant", "spider", "ammo", "weapon", "test"]:  # collision with walls
            self.collide(mapArray)

    def collide(self, mapArray):
        # if inside a wall, get pushed away
        if mapa.isWall(int(self.pos[0]), int(self.pos[1]), mapArray):
            iteration = 1
            while True:  # find closest free tile
                freeTiles = []
                for x in range(-iteration, iteration + 1):
                    for y in range(-iteration, iteration + 1):
                        if x == 0 and y == 0:
                            continue
                        if not mapa.isWall(int(self.pos[0] + x * iteration), int(self.pos[1] + y * iteration),
                                           mapArray):
                            freeTiles.append((x, y))
                if len(freeTiles):
                    break
                iteration += 1
            distances = []
            for tile in freeTiles:
                distances.append((self.pos[0] - (int(self.pos[0]) + tile[0] + 0.5)) ** 2 + (
                            self.pos[1] - (int(self.pos[1]) + tile[1] + 0.5)) ** 2)
            closest = freeTiles[distances.index(min(distances))]
            # teleport to the closest tile
            if closest[0] != 0:
                self.pos[0] = int(self.pos[0]) + closest[0] + (
                    self.thickness if closest[0] > 0 else 1 - self.thickness)
            if closest[1] != 0:
                self.pos[1] = int(self.pos[1]) + closest[1] + (
                    self.thickness if closest[1] > 0 else 1 - self.thickness)
        # keep some distance from walls
        if self.pos[0] % 1 < self.thickness:
            if mapa.isWall(int(self.pos[0]) - 1, int(self.pos[1]), mapArray):
                self.pos[0] += self.thickness - (self.pos[0] % 1)
        if self.pos[0] % 1 > 1 - self.thickness:
            if mapa.isWall(int(self.pos[0]) + 1, int(self.pos[1]), mapArray):
                self.pos[0] -= self.thickness - (1 - (self.pos[0] % 1))
        if self.pos[1] % 1 < self.thickness:
            if mapa.isWall(int(self.pos[0]), int(self.pos[1]) - 1, mapArray):
                self.pos[1] += self.thickness - (self.pos[1] % 1)
        if self.pos[1] % 1 > 1 - self.thickness:
            if mapa.isWall(int(self.pos[0]), int(self.pos[1]) + 1, mapArray):
                self.pos[1] -= self.thickness - (1 - (self.pos[1] % 1))


    def interact(self, player):
        if self.typ == "ammo":
            player.activeWeapon.getWeapon(self.weapon).ownedAmmo += self.ammo
            return True
        elif self.typ == "weapon":
            weapon = player.activeWeapon.getWeapon(self.weapon, player.otherWeapons)
            if weapon:
                player.ownedWeapons.insert(1, weapon)
                player.switchWeapons()
            return True
        elif self.typ == "health":
            player.health = min(player.health + self.weapon, player.maxHealth)
            return True
        return False


def getObject(typ, pos, weapon="default", ammo=0, id=False, offset=True):
    if typ in list(objects):
        o = copy.deepcopy(objects[typ])
    else:
        o = copy.deepcopy(objects[False])
    if offset:
        o.pos = [pos[0] + 1, pos[1] + 1]
    else:
        o.pos = pos
    if typ in ["ammo", "weapon", "health"]:
        o.weapon = weapon
    if typ == "ammo":
        o.ammo = ammo
    o.id = id
    return o


def getObjectByID(id, objects, getIndex=False):
    for object in objects:
        if object.id == id:
            if getIndex:
                return object, objects.index(object)
            else:
                return object
    return False


def getMask(xSize, string):
    mask = []
    for _ in range(xSize): mask.append([])
    line = 0
    for char in string:
        if char in ["0", "O", "o", "H"]:
            mask[line].append(1)
        elif char in [".", " ", ","]:
            mask[line].append(0)
        else:
            line -= 1
        line = (line + 1) % xSize
    return mask


objects = {}
objects["giant"] = Object("giant", draw.Sprite(getMask(22, """
.....000000000000.....
.....000000000000.....
.....000000000000.....
.....000..00..000.....
.....000..00..000.....
.....000000000000.....
....00000000000000....
0000000000000000000000
0000000000000000000000
.00000000000000000000.
.00000000000000000000.
.00000000000000000000.
.0000.0000000000.0000.
.0000.0000000000.0000.
.0000.0000000000.0000.
.0000.0000000000.0000.
.0000.0000000000.0000.
0000000000000000000000
0000000000000000000000
0000000000000000000000
......0000000000......
......0000000000......
......0000000000......
......0000000000......
......0000000000......
......0000000000......
......0000000000......
......0000000000......
......0000000000......
......0000000000......
......0000000000......
......0000000000......
......0000000000......"""), 1, 10, (255, 180, 180)), 1000, 0.4, 45, 0.8)

objects["spider"] = Object("spider", draw.Sprite(getMask(20, """
......00000000......
......00000000......
00000000000000000000
00000000000000000000
00....00000000....00
00....00000000....00
00................00
00................00
00................00
00................00"""), 1, 8, (20, 20, 20)), 30, 1.5, 5, 1.)

objects["ammo"] = Object("ammo", draw.Sprite(getMask(20, """
..0000000000000000..
.000000000000000000.
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000"""), 1, 5, (30, 100, 20)), 0, 0)

objects["weapon"] = Object("weapon", draw.Sprite(getMask(20, """
.000000000000000000.
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000"""), 1, 10, (80, 80, 80)), 0, 0)

objects["health"] = Object("health", draw.Sprite(getMask(3, """
.0.
000
.0."""), 1, 30, (0, 200, 0)), 0, 0)

objects["target"] = Object("target", draw.Sprite(getMask(10, """
....00....
..000000..
.00000000.
.00000000.
0000..0000
0000..0000
.00000000.
.00000000.
..000000..
....00...."""), 0.1, 3, (0, 255, 100)), 1)

objects["test"] = Object("test", draw.Sprite(getMask(10, """
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000"""), 1, 20, (255, 0, 0)), 100)

objects["smth"] = Object("smth", draw.Sprite(getMask(10, """
0000000000
0000000000
0000000000
0000000000
0000..0000
0000..0000
0000000000
0000000000
0000000000
0000000000"""), 1, 10, (0, 255, 100)), 0)

objects[False] = Object(False, draw.Sprite(getMask(10, """
0000000000
00.0000000
00.0000000
00.0000000
00.0000000
00.0000000
00.0000000
00.0000000
00.......0
0000000000"""), 1, 30.7, (255, 0, 255)), 0)

