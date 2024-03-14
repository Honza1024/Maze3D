import pygame as pg
import pygame.key as key
import pygame.mouse as mouse
import copy
import time
import math
import draw
import mapa
import object_class
from player_class import Player
from settings import *


width, height = WINDOW_SIZE, WINDOW_SIZE * 3 // 4
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

objects = [object_class.getObject("testing", [1, 1])]

player = Player((0, 1.999), 0)

lastFrame = time.time()

state = "running"

while state:
    dTime = min(time.time() - lastFrame, 0.2)
    print((int(1 / dTime * 1000) / 1000) if dTime > 0 else "infinity")  # uncomment to see fps in console
    lastFrame = time.time()
    keys = key.get_pressed()
    mouseMovement = mouse.get_rel()[0] * 400 / width

    if state == "running":

        player.move(dTime, mouseMovement, keys, mapArray)

        for object in objects:
            object.move(dTime, player, mapArray)

        draw.frame(surface, width, height, mapArray, player, objects)

    elif state == "paused":
        pass

    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            state = False
            pg.quit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            player.shoot(objects, mapArray)
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