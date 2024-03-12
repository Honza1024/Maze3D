import pygame as pg
import pygame.key as key
import pygame.mouse as mouse
import time
import math
import draw
import mapa
import object_class
from player_class import Player
from debug import *


width, height = 400, 300
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Maze3D")
surface = pg.display.set_mode((width, height))

mouse.set_visible(False)
pg.event.set_grab(True)


mapArray = mapa.create(6, 6, ("......"
                              "......"
                              "..w..."
                              "......"
                              "......"
                              "......"))
if DEBUG: mapa.show(mapArray)

sprite = draw.Sprite([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                            [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                     1, (0, 255, 100))
objects = [object_class.Object("smth", (2, 2), sprite)]
"""for i in range(6):
    for j in range(6):
        objects.append(object_class.Object("smth", (i, j), sprite))"""

player = Player((0, 1.999), 0)

lastFrame = 0

state = "running"

while state:
    if state == "running":
        dTime = time.time() - lastFrame
        lastFrame = time.time()
        if DEBUG: print(player.position[0], player.position[1], player.direction)
        keys = key.get_pressed()
        mouseMovement = mouse.get_rel()[0]

        player.direction = (player.direction + dTime * mouseMovement * player.sensitivity) % (2 * math.pi)

        if keys[pg.K_e]:
            player.direction = (player.direction + dTime * 1) % (2 * math.pi)
        if keys[pg.K_q]:
            player.direction = (player.direction + dTime * -1) % (2 * math.pi)
        if keys[pg.K_w]:
            player.position[0] += player.speed * dTime * math.cos(player.direction)
            player.position[1] += player.speed * dTime * math.sin(player.direction)
        if keys[pg.K_s]:
            player.position[0] -= player.speed * dTime * math.cos(player.direction)
            player.position[1] -= player.speed * dTime * math.sin(player.direction)
        if keys[pg.K_d]:
            player.position[1] += player.speed * dTime * math.cos(player.direction)
            player.position[0] -= player.speed * dTime * math.sin(player.direction)
        if keys[pg.K_a]:
            player.position[1] -= player.speed * dTime * math.cos(player.direction)
            player.position[0] += player.speed * dTime * math.sin(player.direction)

        player.collide(mapArray)

        draw.frame(surface, width, height, mapArray, player, objects)

    elif state == "paused":
        pass

    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            state = False
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                state = 0
                mouse.set_visible(True)
                pg.event.set_grab(False)
                pg.quit()
            elif event.key == pg.K_p:
                if state == "running": #pause the game
                    state = "paused"
                    mouse.set_visible(True)
                    pg.event.set_grab(False)
                elif state == "paused": #unpause the game
                    state = "running"
                    mouse.set_visible(False)
                    pg.event.set_grab(True)
                    mouse.get_rel() #get rid of accumulated mouse movement