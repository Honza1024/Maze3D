import math
import copy
import draw
import mapa
from settings import *


class Object:

    def __init__(self, typ, sprite, health=0, speed=0., damage=0, retreat=0):
        self.typ = typ
        self.pos = [0, 0]
        self.sprite = sprite
        self.health = health
        self.maxHealth = health
        self.speed = speed
        self.damage = damage
        self.retreat = retreat
        self.thickness = len(sprite.mask) * sprite.scale / WINDOW_SIZE / 2


    def move(self, dTime, player, mapArray):
        relX = self.pos[0] - player.position[0]
        relY = self.pos[1] - player.position[1]
        dist = math.sqrt(relX ** 2 + relY ** 2)
        relX /= dist
        relY /= dist
        if self.typ in ["giant", "spider"]:  # go towards player
            self.pos[0] -= relX * self.speed * dTime
            self.pos[1] -= relY * self.speed * dTime
        if self.typ in ["giant", "spider", "ammo", "weapon", "test"]:  # collision
            self.collide(mapArray)
        if dist < player.thickness + self.thickness:  # attack
            player.health -= self.damage
            self.pos[0] += relX * self.speed * self.retreat
            self.pos[1] += relY * self.speed * self.retreat

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
            player.ownedWeapons.append(player.activeWeapon.getWeapon(self.weapon, player.otherWeapons))
            player.switchWeapons()
            return True
        return False


def getObject(typ, pos, weapon="default", ammo=0, id=False):
    if typ in list(objects):
        o = copy.deepcopy(objects[typ])
    else:
        o = copy.deepcopy(objects[False])
    o.pos = [pos[0] + 1, pos[1] + 1]
    if typ in ["ammo", "weapon"]:
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
......0000000000......"""), 1, 10, (255, 180, 180)), 1000, 0.4, 45, 0.3)

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

