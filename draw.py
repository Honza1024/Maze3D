import pygame as pg
import pygame.gfxdraw as draw
import math
import mapa
from debug import *


class Sprite:

    def __init__(self, mask, height, color, anchor = False):
        self.mask = mask
        self.pos = (0, 0)
        self.height = height
        self.color = color
        self.anchor = anchor


def frame(surface, width, height, mapArray, player, objects):
    depthBuf = [[1000000 for i in range(height)] for j in range(width)]
    #drawGui(surface, width, height, player, depthBuf)
    sprites = []
    for object in objects:
        sprite = object.sprite
        sprite.pos = object.pos
        sprites.append(sprite)
    drawSprites(surface, width, height, depthBuf, player, sprites)
    drawMap(surface, width, height, mapArray, player, depthBuf)


def drawSprites(surface, width, height, depthBuf, player, sprites):
    for sprite in sprites:
        mask = sprite.mask
        color = sprite.color
        pPosX, pPosY = player.position
        relX, relY = sprite.pos[0] - pPosX, sprite.pos[1] - pPosY
        if relX == 0:
            if relY > 0:
                direction = math.pi / 2
            elif relY == 0:
                return #if the sprite is on players position, just ignore it
            else:
                direction = 3 * math.pi / 2
        elif relY > 0:
            direction = math.atan(relY / relX)
            if relX < 0:
                direction += math.pi
        else:
            direction = math.atan(relY / relX)
            if relX < 0:
                direction += math.pi
        direction = (direction - player.direction) % (2 * math.pi)
        if direction > math.pi:
            direction -= 2 * math.pi
        if abs(direction) > 1.5:
            continue
        x = width / 2 + (direction / player.fov) * width
        distance = math.sqrt((pPosX - sprite.pos[0]) ** 2 + (pPosY - sprite.pos[1]) ** 2)
        if distance < 0.1: continue
        distance = distance * math.cos(direction)
        depth = distance
        scale = 5 / distance
        y = (height / 2) + sprite.height * (1 / distance) * (height / 2)
        print(direction, relX, relY)

        drawSprite(surface, width, height, int(x), int(y), scale, depthBuf, mask, depth, color)


def drawSprite(surface, width, height, midX, bottomY, scale, depthBuf, mask, depth, color):
    sizeX = int(len(mask) * scale)
    sizeY = int(len(mask[0]) * scale)
    cornerX = midX - sizeX // 2
    cornerY = bottomY - sizeY
    for x in range(sizeX):
        pixelX = cornerX + x
        for y in range(sizeY):
            pixelY = cornerY + y
            if not (0 <= pixelX < width and 0 <= pixelY < height):
                continue
            isColored = mask[int(x / (scale - 0.001))][int(y / (scale + 0.001))]
            if True and depth < depthBuf[pixelX][pixelY]:
                drawPixel(surface, pixelX, pixelY, color, depthBuf, depth)


def drawGui(surface, width, height, player, depthBuf):
    for x in range(10):
        for y in range(10):
            drawPixel(surface, x, y, (255, 255, 255), depthBuf, -1)
    drawLine(surface, (10, 10), (300, 200), 1, (255, 255, 255), depthBuf, -1)


def drawPixel(surface, x, y, color, depthBuf, depth):
    draw.pixel(surface, x, y, color)
    depthBuf[x][y] = depth


def drawLine(surface, start, end, thickness, color, depthBuf, depth):
    x1, y1 = start
    x2, y2 = end
    if x1 == x2 and y1 == y2:
        drawPixel(surface, start[0], start[1], color, depthBuf, depth)

    dx = x2 - x1
    ax = abs(dx) * 2
    sx = 1
    if dx < 0: sx = -1
    dy = y2 - y1
    ay = abs(dy) * 2
    sy = 1
    if dy < 0: sy = -1

    if ax > ay:
        d = ay - (ax // 2)
        while x1 != x2:
            drawPixel(surface, x1, y1, color, depthBuf, depth)
            if d >= 0:
                y1 += sy
                d -= ax
            x1 += sx
            d += ay
    else:
        d = ax - (ay // 2)
        while y1 != y2:
            drawPixel(surface, x1, y1, color, depthBuf, depth)
            if d >= 0:
                x1 += sx
                d -= ay
            y1 += sy
            d += ax

    drawPixel(surface, x2, y2, color, depthBuf, depth)


def drawMap(surface, width, height, mapArray, player, depthBuf):
    for x in range(width):
        direction = (player.direction + ((x / width) - 0.5) * player.fov) % (2 * math.pi)
        distance, vertical = mapa.getDistance(mapArray, player.position, direction)
        if player.noDeformation: #make walls look straight
            distance *= math.cos(((x / width) - 0.5) * player.fov)
        wallTop = (height / 2) - ((0.5 * height) / distance)
        wallBottom = height / 2 + 0.5 * height / distance
        for y in range(height):
            if distance < depthBuf[x][y]:
                if y < wallTop:
                    color = (50, 50, 255) #sky
                elif y < wallBottom:
                    color = (111, 111, 111) if vertical else (130, 130, 130) #wall
                else:
                    color = (128, 30, 30) #floor
                draw.pixel(surface, x, y, color)
