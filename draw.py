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
        relX = sprite.pos[0] - player.position[0]
        relY = sprite.pos[1] - player.position[1]
        if relX == 0 or relY == 0:
            continue
        distance = math.sqrt(relX ** 2 + relY ** 2)
        direction = math.atan(relY / relX)
        if relX < 0: direction += math.pi
        direction = ((direction - player.direction + math.pi) % (2 * math.pi)) - math.pi
        if player.noDeformation: distance *= math.cos(direction)
        x = (width / 2) + ((direction / player.fov) * width)
        y = (height / 2) + ((sprite.height / distance) * (height / 2))
        scale = 10 / distance

        drawSprite(surface, width, height, int(x), int(y), scale, depthBuf, sprite.mask, distance, sprite.color)


def drawSprite(surface, width, height, midX, bottomY, scale, depthBuf, mask, depth, color):
    scaleX = int(scale * len(mask))
    scaleY = int(scale * len(mask[0]))
    for x in range(scaleX):
        pixelX = midX + x - scaleX // 2
        for y in range(scaleY):
            pixelY = bottomY + y - scaleY
            if 0 <= pixelX < width and 0 <= pixelY < height and mask[int(x / scale)][int(y / scale)]:
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
