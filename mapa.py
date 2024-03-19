import math
import random


def create(width, height, string):
    mapa = [[1]]
    for _ in range(height):
        mapa[0].append(1) #add a line of walls to hide the error happenning when player (x) coordinate is negative
    for x in range(width):
        mapa.append([])
        mapa[-1].append(1) #add a line of walls to hide the error happenning when player (y) coordinate is negative
        for y in range(height):
            if string[x + y * width] in ["w", "W"]:  #0 -> nothing
                mapa[-1].append(1)                   #1 -> wall
            else:
                mapa[-1].append(0)
    return mapa


def getDistance(mapArray, position, direction):
    horizontal = checkHorizontal(mapArray, position, direction)
    vertical = checkVertical(mapArray, position, direction)
    return (horizontal, False) if horizontal < vertical else (vertical, True)



def checkHorizontal(mapArray, position, direction):
    atan = -1 / (math.tan(direction) if direction else 100000000)
    if math.sin(direction) < -0.00001: #looking up
        rayY = int(position[1]) - 0.00000001
        rayX = (position[1] - rayY) * atan + position[0]
        dy = -1.0001
        dx = -dy * atan
    elif math.sin(direction) > 0.00001: #looking down
        rayY = int(position[1]) + 1
        rayX = (position[1] - rayY) * atan + position[0]
        dy = 1.0001
        dx = -dy * atan
    else:
        return 100000
    for _ in range(len(mapArray[0])):
        if isWall(int(rayX), int(rayY), mapArray): #hit wall
            break
        else:
            rayX += dx
            rayY += dy
    return math.sqrt(((rayX - position[0]) ** 2) + ((rayY - position[1]) ** 2))



def checkVertical(mapArray, position, direction):
    ntan = -(math.tan(direction) if direction else 100000000)
    if math.cos(direction) < -0.00001: #looking left
        rayX = int(position[0]) - 0.00000001
        rayY = (position[0] - rayX) * ntan + position[1]
        dx = -1.0001
        dy = -dx * ntan
    elif math.cos(direction) > 0.00001: #looking right
        rayX = int(position[0]) + 1
        rayY = (position[0] - rayX) * ntan + position[1]
        dx = 1.0001
        dy = -dx * ntan
    else:
        return 100000
    for _ in range(len(mapArray)):
        if isWall(int(rayX), int(rayY), mapArray): #hit wall
            break
        else:
            rayX += dx
            rayY += dy
    return math.sqrt(((rayX - position[0]) ** 2) + ((rayY - position[1]) ** 2))



def isWall(x, y, mapArray):
    if x < 0 or y < 0 or x >= len(mapArray) or y >= len(mapArray[0]): #out of bounds
        return 1
    return mapArray[x][y]



def show(mapArray):
    print(" ", end = "")
    for x in range(len(mapArray[0])):
        print("-", end = "")
    print()
    for x in range(len(mapArray)):
        print("|", end = "")
        for y in range(len(mapArray[0])):
            if mapArray[x][y] == 1: print("w", end = "")
            else: print(".", end = "")
        print("|")
    print(" ", end = "")
    for x in range(len(mapArray[0])):
        print("-", end = "")


def getMap(name, width=32, height=32, wallRate=0.3):
    if name == "survival":
        string = ""
        for _ in range(width * height):
            if 14 < _ // 32 < 18 and 15 < _ % 32 < 19:
                string += "."
            else:
                string += "w" if random.random() < 0.3 else "."
        return create(width, height, string)
    if name == "demo":
        return create(6, 6, ("......"
                             "......"
                             "..w..."
                             "......"
                             "......"
                             "......"))
