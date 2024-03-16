import time
import draw
from settings import *


class Weapon:

    weapons = []
    lastShot = 0
    def __init__(self, name, draw, damage, ammo, maxAmmo):
        self.name = name
        self.drawWeaponPrivate = draw
        self.damage = damage
        self.ammo = min(ammo, maxAmmo)
        self.maxAmmo = maxAmmo
        self.ownedAmmo = max(0, ammo - maxAmmo)
        self.weapons.append(self)


    def draw(self, surface, depthBuf, width, height):
        midX = width // 2
        midY = height // 2
        lastShot = self.lastShot
        self.drawWeaponPrivate(surface, width, height, depthBuf, midX, midY, lastShot)


    def getWeapon(self, name, set=False):
        if set:
            for weapon in set:
                if weapon.name == name:
                    return set.pop(set.index(weapon))
            return False
        for weapon in self.weapons:
            if weapon.name == name:
                return weapon
        return False



# default weapon
def drawDefault(surface, width, height, depthBuf, midX, midY, lastShot):
    if time.time() - lastShot > 0.1:
        draw.drawRect(surface, midX, height, width // 8, height // 5, (50, 50, 50),depthBuf, 0, False, (0.5, 1))
        draw.drawRect(surface, midX, height - (height // 5), width // 60, height // 20, (50, 50, 50),depthBuf, 0, False, (0.5, 1))
    else:
        draw.drawRect(surface, midX, height - (height // 10), width // 8, height // 5, (50, 50, 50),depthBuf, 0, False, (0.5, 1))
        draw.drawRect(surface, midX, height - (height // 5) - (height // 10), width // 60, height // 20, (50, 50, 50),depthBuf, 0, False, (0.5, 1))

def damageDefault(distance, direct, dTime, weapon):
    if weapon.ammo == "reloading":
        if time.time() - weapon.lastShot > 1.5:
            weapon.ammo = min(weapon.maxAmmo, weapon.ownedAmmo)
            weapon.ownedAmmo = max(0, weapon.ownedAmmo - weapon.maxAmmo)
        else:
            return 0
    if time.time() - weapon.lastShot > 0.3 and weapon.ammo > 0:
        weapon.ammo -= 1
        weapon.lastShot = time.time()
        return 10
    if weapon.ammo <= 0:
        weapon.ammo = "reloading"
    return 0

Weapon("default", drawDefault, damageDefault, 30, 6)
