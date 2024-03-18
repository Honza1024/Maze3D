import pygame as pg
import pygame.key as key
import pygame.font as font
import pygame.mouse as mouse
import copy
import time
import math
import draw
import gameplay
import mapa
import object_class
import menu
from player_class import Player
from settings import *


font.init()

width, height = WINDOW_RESOLUTION, WINDOW_RESOLUTION * 3 // 4
pg.display.set_caption("Maze3D")
surface = pg.display.set_mode((width * PIXEL_SIZE, height * PIXEL_SIZE))

gameFont = font.Font(None, height * PIXEL_SIZE // 10)

startMenu = menu.getMenu("start")
pauseMenu = menu.getMenu("paused")

mapArray = mapa.create(6, 6, ("......"
                              "......"
                              "..w..."
                              "......"
                              "......"
                              "......"))

game = gameplay.Gameplay()
player, objects = game.player, game.objects

lastFrame = 0

state = "start"

while state:
    if state == "running":
        #time.sleep((0.07))
        dTime = time.time() - lastFrame
        #if dTime != 0: print(1 / dTime)  # uncomment to print fps into console
        lastFrame = time.time()
        dTime = min(dTime, 0.1)
        keys = key.get_pressed()
        mouseMovement = mouse.get_rel()[0]

        player.move(dTime, mouseMovement, keys, mapArray)
        player.activeWeapon.loop(dTime)

        state = game.mainLoop(dTime, mapArray, state)
        if state == "defeat":
            endScreen = menu.getMenu("endScreen", player)
            mouse.set_visible(True)

        for object in objects:
            object.move(dTime, player, mapArray, objects)

    elif state == "start":
        startMenu.draw(surface, mouse.get_pos())

    elif state == "paused":
        pauseMenu.draw(surface, mouse.get_pos())

    elif state == "defeat":
        endScreen.draw(surface, mouse.get_pos())

    for event in pg.event.get():
        if event.type == pg.QUIT:
            state = False
            pg.quit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if state == "running":
                if event.button == 1:
                    player.shoot(objects, mapArray, player, dTime)
                elif event.button == 3:
                    player.switchWeapons()
            elif state in ["start", "paused", "defeat"]:
                if state == "start":
                    action = startMenu.click(mouse.get_pos())
                if state == "paused":
                    action = pauseMenu.click(mouse.get_pos())
                if state == "defeat":
                    action = endScreen.click(mouse.get_pos())
                if state == "defeat":
                    pass
                if action == "continue":
                    mouse.set_visible(False)
                    pg.event.set_grab(True)
                    mouse.get_rel()
                    state = "running"
                elif action == "start" or action == "retry":
                    if player.score or action == "retry":
                        game = gameplay.Gameplay()
                        player, objects = game.player, game.objects
                        state = "running"
                        mouse.set_visible(False)
                        pg.event.set_grab(True)
                        mouse.get_rel()
                    else:
                        mouse.set_visible(False)
                        pg.event.set_grab(True)
                        mouse.get_rel()
                        state = "running"
                elif action == "quit":
                    state = 0
                    mouse.set_visible(True)
                    pg.event.set_grab(False)
                    pg.quit()
                    break
                elif action == "main menu":
                    state = "start"
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if state == "running":  # pause the game
                    state = "paused"
                    mouse.set_visible(True)
                    pg.event.set_grab(False)
                elif state == "paused": #unpause the game
                    state = "running"
                    mouse.set_visible(False)
                    pg.event.set_grab(True)
                    mouse.get_rel() #get rid of accumulated mouse movement
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
            elif event.key == pg.K_r:
                player.activeWeapon.reload(player.activeWeapon)

    if state == "running":
        draw.frame(surface, width, height, mapArray, player, objects, gameFont)
    if state:
        pg.display.flip()
