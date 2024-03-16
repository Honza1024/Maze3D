import pygame as pg
import pygame.gfxdraw as draw
import math
import mapa
from settings import *


class Sprite:

    def __init__(self, mask, height, scale, color, anchor = False):
        self.mask = mask
        self.pos = (0, 0)
        self.height = height
        self.scale = scale
        self.color = color
        self.anchor = anchor


def frame(surface, width, height, mapArray, player, objects):
    surface.lock()
    depthBuf = [[1000000 for i in range(height)] for j in range(width)]
    drawGui(surface, width, height, player, depthBuf)
    drawMap(surface, width, height, mapArray, player, depthBuf)
    sprites = []
    for object in objects:
        sprite = object.sprite
        sprite.pos = object.pos
        sprite.thickness = object.thickness
        sprite.health = object.health / object.maxHealth if object.maxHealth else 1
        sprites.append(sprite)
    drawSprites(surface, width, height, depthBuf, player, sprites)
    surface.unlock()


def drawSprites(surface, width, height, depthBuf, player, sprites):
    for sprite in sprites:
        relX = sprite.pos[0] - player.position[0]
        relY = sprite.pos[1] - player.position[1]
        if relX == 0 and relY == 0:
            continue
        distance = math.sqrt(relX ** 2 + relY ** 2)
        if relX: direction = math.atan(relY / relX)
        else: direction = math.pi / 2
        if relX < 0: direction += math.pi
        direction = ((direction - player.direction + math.pi) % (2 * math.pi)) - math.pi
        if player.noDeformation: distance *= math.cos(direction)
        if distance < sprite.thickness or abs(direction) > 1: continue
        x = (width / 2) + ((direction / player.fov) * width)
        y = (height / 2) + ((sprite.height / distance) * (height / 2))
        scale = (sprite.scale * width) / (distance * 400)
        health = sprite.health

        drawSprite(surface, width, height, int(x), int(y), scale, depthBuf, sprite.mask, distance, sprite.color, health)


def drawSprite(surface, width, height, midX, bottomY, scale, depthBuf, mask, depth, color, health):
    darker = (color[0] * 0.9, color[1] * 0.9, color[2] * 0.9)
    scaleX = int(scale * len(mask))
    scaleY = int(scale * len(mask[0]))
    if midX + scaleX // 2 < 0 or midX - scaleX // 2 > width:
        return
    for x in range(scaleX):
        pixelX = midX + x - scaleX // 2
        if pixelX >= width: break
        elif pixelX < 0: continue
        if depth > depthBuf[pixelX][0]: continue
        for y in range(scaleY):
            pixelY = bottomY + y - scaleY
            if pixelY >= height: break
            elif pixelY < 0: continue
            if mask[min(int((x / scale) + 0.15), len(mask) - 1)][min(int((y / scale) + 0.15), len(mask[0]) - 1)]:
                if y / scaleY < health:
                    drawPixel(surface, pixelX, pixelY, color, depthBuf, depth)
                else:
                    drawPixel(surface, pixelX, pixelY, darker, depthBuf, depth)


def drawGui(surface, width, height, player, depthBuf):
    scale = WINDOW_SIZE / 400
    # draw weapon
    player.activeWeapon.draw(surface, depthBuf, width, height)
    # draw health bar
    drawRect(surface, 10 * scale, 10 * scale, 1 * player.health * scale, 15 * scale, (220, 0, 0), depthBuf, 0)
    if player.health < 100:
        drawRect(surface, (10 + 1 * player.health) * scale, 10 * scale, (100 - 1 * player.health) * scale, 15 * scale, (150, 0, 0), depthBuf, 0)
    #drawLine(surface, (10, 10), (300, 200), 1, (255, 255, 255), depthBuf, -1)


def drawPixel(surface, x, y, color, depthBuf, depth):
    if depth > depthBuf[x][y]: return
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


def drawRect(surface, leftX, topY, width, height, color, depthBuf, depth, checkDepth=False, anchorPoint=(0,0)):
    leftX = int(leftX - (width * anchorPoint[0]))
    topY = int(topY - (height * anchorPoint[1]))
    width = int(width)
    height = int(height)
    if leftX < 0:
        width += leftX
        leftX = 0
    if topY < 0:
        height += topY
        topY = 0
    width = min(width, WINDOW_SIZE - leftX)
    height = min(height, int(WINDOW_SIZE * 3 / 4) - topY)
    for x in range(leftX, leftX + width):
        for y in range(topY, topY + height):
            depthBuf[x][y] = depth
            if checkDepth and depth < depthBuf[x][y]:
                draw.pixel(surface, x, y, color)
    if not checkDepth:
        draw.box(surface, pg.Rect(leftX, topY, width, height), color)



def drawMap(surface, width, height, mapArray, player, depthBuf):
    for x in range(width):
        direction = (player.direction + ((x / width) - 0.5) * player.fov) % (2 * math.pi)
        distance, vertical = mapa.getDistance(mapArray, player.position, direction)
        if player.noDeformation: #make walls look straight
            distance *= math.cos(((x / width) - 0.5) * player.fov)
        depthBuf[x][0] = distance + 0.00001
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

