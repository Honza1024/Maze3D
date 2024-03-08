import pygame as pg
import pygame.gfxdraw as draw
import math
import mapa
from debug import *


def frame(surface, screen, width, height, mapArray, player):
    for x in range(width):
        direction = (player.direction + ((x / width) - 0.5) * player.fov) % (2 * math.pi)
        distance, vertical = mapa.getDistance(mapArray, player.position, direction)
        #if DEBUG: print("direction before:", player.direction, "after:", direction)
        if player.noDeformation: #make walls look straight
            distance *= math.cos(((x / width) - 0.5) * player.fov)
            #print(math.cos(x / width - (((width / 2) / height) * player.fov)))
        #if DEBUG: print("distance:", distance)
        wallTop = (height / 2) - ((0.5 * height) / distance)
        wallBottom = height / 2 + 0.5 * height / distance
        #if DEBUG: print("wallTop:", wallTop, "wallBottom:", wallBottom)
        for y in range(height):
            if y < wallTop:
                color = (50, 50, 255) #sky
            elif y < wallBottom:
                color = (111, 111, 111) if vertical else (130, 130, 130) #wall
            else:
                color = (128, 30, 30) #floor
            draw.pixel(surface, x, y, color)
