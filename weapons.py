import math
import draw
from settings import *


class Weapon:

    weapons = []
    lastShot = 0
    def __init__(self, name, draw, shoot, reload, loop, damage, ammo, maxAmmo, knockback=0.):
        self.name = name
        self.drawWeaponPrivate = draw
        self.shoot = shoot
        self.reload = reload
        self.loopPrivate = loop
        self.damage = damage
        self.ammo = min(ammo, maxAmmo)
        self.maxAmmo = maxAmmo
        self.ownedAmmo = max(0, ammo - maxAmmo)
        self.state = 0
        self.kb = knockback
        self.weapons.append(self)


    def draw(self, surface, depthBuf, width, height):
        midX = width // 2
        midY = height // 2
        lastShot = self.lastShot
        self.drawWeaponPrivate(surface, width, height, depthBuf, midX, midY, self)


    def loop(self, dTime):
        self.lastShot += dTime
        self.loopPrivate(self, dTime)


    def getWeapon(self, name, set=False):
        if isinstance(set, list):
            for weapon in set:
                if weapon.name == name:
                    return set.pop(set.index(weapon))
            return False
        for weapon in self.weapons:
            if weapon.name == name:
                return weapon
        return False


    def knockback(self, object, player):
        if not self.kb: return
        relX = object.pos[0] - player.position[0]
        relY = object.pos[1] - player.position[1]
        distance = math.sqrt(relX ** 2 + relY ** 2)
        direction = math.atan(relY / relX) if relX else math.pi / 2
        if relX < 0: direction += math.pi
        object.pos[0] += math.cos(direction) * self.kb
        object.pos[1] += math.sin(direction) * self.kb



# default weapon
def drawDefault(surface, width, height, depthBuf, midX, midY, weapon):
    if weapon.lastShot > 0.1 or weapon.ammo == "reloading":
        draw.drawRect(surface, midX, height, width // 8, height // 5, (50, 50, 50),depthBuf, 0, False, (0.5, 1))
        draw.drawRect(surface, midX, height - (height // 5), width // 60, height // 20, (50, 50, 50),depthBuf, 0, False, (0.5, 1))
    else:
        draw.drawRect(surface, midX, height - (height // 10), width // 8, height // 5, (50, 50, 50),depthBuf, 0, False, (0.5, 1))
        draw.drawRect(surface, midX, height - (height // 5) - (height // 10), width // 60, height // 20, (50, 50, 50),depthBuf, 0, False, (0.5, 1))

def shootDefault(weapon):
    if weapon.ammo == "reloading":
        return False
    if weapon.lastShot > 0.3 and weapon.ammo > 0:
        weapon.ammo -= 1
        weapon.lastShot = 0
        return True
    return False

def reloadDefault(weapon):
    weapon.ammo = "reloading"
    weapon.lastShot = 0

def loopDefault(weapon, dTime):
    if weapon.ammo == "reloading" and weapon.lastShot > 1:
        weapon.ammo = min(weapon.maxAmmo, weapon.ownedAmmo)
        weapon.ownedAmmo = max(0, weapon.ownedAmmo - weapon.maxAmmo)
    if type(weapon.ammo) == type(1):
        if weapon.ammo <= 0 and weapon.ownedAmmo > 0:
            weapon.ammo = "reloading"
            weapon.lastShot = 0
    if weapon.ammo == "reloading":
        weapon.state = (weapon.lastShot) / 1
    elif weapon.lastShot < 0.3:
        weapon.state = weapon.lastShot / 0.3
    else:
        weapon.state = 0

def damageDefault(distance, direct, dTime, weapon):
    return 10

Weapon("default", drawDefault, shootDefault, reloadDefault, loopDefault, damageDefault, 0, 6, 0.02)
Weapon("hand gun", drawDefault, shootDefault, reloadDefault, loopDefault, damageDefault, 0, 6, 0.02)


# rifle
def drawRifle(surface, width, height, depthBuf, midX, midY, weapon):
    if weapon.lastShot > 0.1 or weapon.ammo == "reloading":
        draw.drawRect(surface, midX, height, width // 5, height // 5, (50, 50, 50), depthBuf, 0, False, (0.5, 1))
        draw.drawRect(surface, midX - width // 40, height - (height // 5), width // 60, height // 20, (50, 50, 50), depthBuf, 0, False, (0.5, 1))
        draw.drawRect(surface, midX + width // 40, height - (height // 5), width // 60, height // 20, (50, 50, 50), depthBuf, 0, False, (0.5, 1))
    else:
        draw.drawRect(surface, midX, height - (height // 20), width // 5, height // 5, (50, 50, 50), depthBuf, 0, False, (0.5, 1))
        draw.drawRect(surface, midX - width // 40, height - (height // 5) - (height // 20), width // 60, height // 20, (50, 50, 50), depthBuf, 0, False, (0.5, 1))
        draw.drawRect(surface, midX + width // 40, height - (height // 5) - (height // 20), width // 60, height // 20, (50, 50, 50), depthBuf, 0, False, (0.5, 1))

def shootRifle(weapon):
    if weapon.ammo == "reloading":
        return False
    if weapon.lastShot > 0 and weapon.ammo > 0:
        weapon.ammo -= 1
        weapon.lastShot = 0
        return True
    return False

def reloadRifle(weapon):
    weapon.ammo = "reloading"
    weapon.lastShot = 0

def loopRifle(weapon, dTime):
    if weapon.ammo == "reloading" and weapon.lastShot > 1.5:
            weapon.ammo = min(weapon.maxAmmo, weapon.ownedAmmo)
            weapon.ownedAmmo = max(0, weapon.ownedAmmo - weapon.maxAmmo)
    if type(weapon.ammo) == type(1):
        if weapon.ammo <= 0 and weapon.ownedAmmo > 0:
            weapon.ammo = "reloading"
            weapon.lastShot = 0
    if weapon.ammo == "reloading":
        weapon.state = weapon.lastShot / 1.5
    else:
        weapon.state = 0

def damageRifle(distance, direct, dTime, weapon):
    return 80

Weapon("rifle", drawRifle, shootRifle, reloadRifle, loopRifle, damageRifle, 0, 2, 0.15)
