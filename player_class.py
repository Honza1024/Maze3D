import pygame as pg
import math
import copy
import mapa
import weapons
from settings import *


class Player:

    def __init__(self, pos, dir, speed, thickness, health, ownedWeapons):
        self.position = [pos[0] + 1, pos[1] + 1]  # adding 1 to account for the added rows of walls on x=0 and y=0
        self.direction = dir
        self.fov = FOV
        self.noDeformation = NO_DEFORMATION
        self.speed = speed
        self.sensitivity = MOUSE_SENSITIVITY
        self.thickness = thickness
        self.otherWeapons = copy.copy(weapons.Weapon.weapons)
        self.ownedWeapons = []
        for name in ownedWeapons:
            self.ownedWeapons.append(self.otherWeapons[0].getWeapon(name, self.otherWeapons))
        self.activeWeapon = self.ownedWeapons[0]
        self.health = health


    def collide(self, mapArray):
        #if inside a wall, get pushed away
        if mapa.isWall(int(self.position[0]), int(self.position[1]), mapArray):
            iteration = 1
            while True: #find closest free tile
                freeTiles = []
                for x in range(-iteration, iteration + 1):
                    for y in range(-iteration, iteration + 1):
                        if x == 0 and y == 0:
                            continue
                        if not mapa.isWall(int(self.position[0] + x * iteration), int(self.position[1] + y * iteration), mapArray):
                            freeTiles.append((x, y))
                if len(freeTiles):
                    break
                iteration += 1
            distances = []
            for tile in freeTiles:
                distances.append((self.position[0] - (int(self.position[0]) + tile[0] + 0.5)) ** 2 + (self.position[1] - (int(self.position[1]) + tile[1] + 0.5)) ** 2)
            closest = freeTiles[distances.index(min(distances))]
            # teleport to the closest tile
            if closest[0] != 0:
                self.position[0] = int(self.position[0]) + closest[0] + (self.thickness if closest[0] > 0 else 1 - self.thickness)
            if closest[1] != 0:
                self.position[1] = int(self.position[1]) + closest[1] + (self.thickness if closest[1] > 0 else 1 - self.thickness)
        # keep some distance from walls
        if self.position[0] % 1 < self.thickness:
            if mapa.isWall(int(self.position[0]) - 1, int(self.position[1]), mapArray):
                self.position[0] += self.thickness - (self.position[0] % 1)
        if self.position[0] % 1 > 1 - self.thickness:
            if mapa.isWall(int(self.position[0]) + 1, int(self.position[1]), mapArray):
                self.position[0] -= self.thickness - (1 - (self.position[0] % 1))
        if self.position[1] % 1 < self.thickness:
            if mapa.isWall(int(self.position[0]), int(self.position[1]) - 1, mapArray):
                self.position[1] += self.thickness - (self.position[1] % 1)
        if self.position[1] % 1 > 1 - self.thickness:
            if mapa.isWall(int(self.position[0]), int(self.position[1]) + 1, mapArray):
                self.position[1] -= self.thickness - (1 - (self.position[1] % 1))


    def move(self, dTime, mouseMovement, keys, mapArray):
        self.direction = (self.direction + dTime * mouseMovement * self.sensitivity) % (2 * math.pi)

        if keys[pg.K_w]:
            self.position[0] += self.speed * dTime * math.cos(self.direction)
            self.position[1] += self.speed * dTime * math.sin(self.direction)
        if keys[pg.K_s]:
            self.position[0] -= self.speed * dTime * math.cos(self.direction)
            self.position[1] -= self.speed * dTime * math.sin(self.direction)
        if keys[pg.K_d]:
            self.position[1] += self.speed * dTime * math.cos(self.direction)
            self.position[0] -= self.speed * dTime * math.sin(self.direction)
        if keys[pg.K_a]:
            self.position[1] -= self.speed * dTime * math.cos(self.direction)
            self.position[0] += self.speed * dTime * math.sin(self.direction)

        self.collide(mapArray)

    def shoot(self, objects, mapArray, player, dTime):
        if not player.activeWeapon.shoot(player.activeWeapon): return
        for object in objects:
            if object.maxHealth == 0:
                continue
            relX = object.pos[0] - self.position[0]
            relY = object.pos[1] - self.position[1]
            if relX == 0 and relY == 0:
                continue
            distance = math.sqrt(relX ** 2 + relY ** 2)
            direction = math.atan(relY / relX) if relX else math.pi / 2
            if relX < 0: direction += math.pi
            direction = ((direction - self.direction + math.pi) % (2 * math.pi)) - math.pi
            if mapa.getDistance(mapArray, player.position, player.direction)[0] < distance:
                player.activeWeapon.damage(dTime, 0, distance, player.activeWeapon)
                continue
            if self.noDeformation: distance *= math.cos(direction)
            direction *= WINDOW_SIZE
            size = len(object.sprite.mask[0]) * object.sprite.scale / distance
            direct = 1 - abs(direction / (size / 2))
            if direction - (size / 2) < 0 < direction + (size / 2):  # got hit:
                object.health -= player.activeWeapon.damage(dTime, direct, distance, player.activeWeapon)
            else:
                player.activeWeapon.damage(dTime, direct, distance, player.activeWeapon)
            if object.health <= 0:
                objects.pop(objects.index(object))


    def switchWeapons(self):
        self.ownedWeapons.append(self.ownedWeapons.pop(0))
        self.activeWeapon = self.ownedWeapons[0]
