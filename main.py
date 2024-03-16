import pygame as pg
import pygame.key as key
import pygame.mouse as mouse
import copy
import time
import math
import draw
import gameplay
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

game = gameplay.Gameplay()
player, objects = game.player, game.objects

lastFrame = 0

state = "running"

while state:
    if state == "running":
        dTime = time.time() - lastFrame
        #if dTime != 0: print(1 / dTime)  # uncomment to print fps into console
        lastFrame = time.time()
        dTime = min(dTime, 0.1)
        keys = key.get_pressed()
        mouseMovement = mouse.get_rel()[0] * 400 / width

        player.move(dTime, mouseMovement, keys, mapArray)

        game.mainLoop(dTime, mapArray)

        for object in objects:
            object.move(dTime, player, mapArray)

    elif state == "paused":
        pass

    for event in pg.event.get():
        if event.type == pg.QUIT:
            state = False
            pg.quit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot(objects, mapArray, player, dTime)
            elif event.button == 3:
                player.switchWeapons()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                state = 0
                mouse.set_visible(True)
                pg.event.set_grab(False)
                pg.quit()
                state = 0
                break
            elif event.key == pg.K_e:  # interaction with objects
                toDestroy = []
                for object in objects:
                    if 1 > math.sqrt((object.pos[0] - player.position[0]) ** 2 + (object.pos[1] - player.position[1]) ** 2):
                        if object.interact(player):
                            toDestroy.append(objects.index(object))
                toDestroy.sort(reverse=True)
                for index in toDestroy: objects.pop(index)
            elif event.key == pg.K_p:
                if state == "running":  # pause the game
                    state = "paused"
                    mouse.set_visible(True)
                    pg.event.set_grab(False)
                elif state == "paused": #unpause the game
                    state = "running"
                    mouse.set_visible(False)
                    pg.event.set_grab(True)
                    mouse.get_rel() #get rid of accumulated mouse movement

    if state:
        draw.frame(surface, width, height, mapArray, player, objects)
        pg.display.flip()
