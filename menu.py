import pygame as pg
import pygame.gfxdraw as gfxdraw
import pygame.font as font
import draw
from settings import *


class Menu:

    def __init__(self, title="", content=[[]], textSize=10, textColor=(255, 255, 255), background=None, offset=0.1, leftOffset=None, topOffset=None, rightOffset=None, bottomOffset=None):
        self.content = content
        self.textColor = textColor
        self.background = background
        self.lastChosen = [0, 0]

        screenWidth = WINDOW_RESOLUTION * PIXEL_SIZE
        screenHeight = (WINDOW_RESOLUTION * 3 // 4) * PIXEL_SIZE
        if topOffset is None: topOffset = offset
        if leftOffset is None: leftOffset = offset
        if rightOffset is None: rightOffset = offset
        if bottomOffset is None: bottomOffset = offset
        topOffset *= screenHeight
        leftOffset *= screenWidth
        rightOffset *= screenWidth
        bottomOffset *= screenHeight
        self.topOffset = topOffset
        self.leftOffset = leftOffset
        self.rightOffset = rightOffset
        self.bottomOffset = bottomOffset

        self.textSize = (screenHeight * textSize) // 100
        self.font = font.Font(None, self.textSize)

        if len(title):
            rendered = self.font.render(title, False, self.textColor)
            x, y = rendered.get_size()
            x = (screenWidth / 2) - (x / 2)
            y = (topOffset / 2) - (y / 2)
            self.title = [rendered, x, y]
        else:
            self.title = False

        columns = len(self.content)
        strings = len(self.content[0])
        menuLeft = leftOffset
        menuWidth = screenWidth - leftOffset - rightOffset
        menuTop = topOffset
        menuHeight = screenHeight - topOffset - bottomOffset
        self.columnOffset = columnOffset = menuWidth / columns
        self.stringOffset = stringOffset = menuHeight / strings
        for columnIndex, column in enumerate(self.content):
            x = menuLeft + columnIndex * columnOffset
            for stringIndex, string in enumerate(column):
                y = menuTop + stringIndex * stringOffset
                self.content[columnIndex][stringIndex] = [string, self.font.render(string, False, self.textColor)]
                self.content[columnIndex][stringIndex].append(x)
                self.content[columnIndex][stringIndex].append(y)


    def click(self, pos):
        x, y = self.lastChosen
        return self.content[x][y][0]


    def chosen(self, mousePos):
        x, y = mousePos
        x -= self.leftOffset
        x /= self.columnOffset
        x += 0.5
        x = max(x, 0)
        x = int(min(x, len(self.content) - 1))
        y -= self.topOffset
        y /= self.stringOffset
        y += 0.5
        y = max(y, 0)
        y = int(min(y, len(self.content[x]) - 1))
        self.lastChosen = [x, y]
        return [x, y]


    def draw(self, surface, mousePos):
        if self.background is None:
            draw.drawRect(surface, 0, 0, WINDOW_RESOLUTION, WINDOW_RESOLUTION * 3 // 4, (0, 0, 0))
        elif isinstance(self.background, tuple):
            draw.drawRect(surface, 0, 0, WINDOW_RESOLUTION, WINDOW_RESOLUTION * 3 // 4, self.background)
        elif isinstance(self.background, pg.Surface):
            pass  # TODO: resize and show background image
        if self.title:
            rendered, x, y = self.title
            surface.blit(rendered, (x, y))
        for column in self.content:
            for string in column:
                s, rendered, x, y = string
                surface.blit(rendered, (x, y))
        x, y = self.chosen(mousePos)
        _, rect, x, y = self.content[x][y]
        size = self.textSize
        gfxdraw.box(surface, pg.Rect(x - (0.5 * size), y + (size // 8), size / 3, size / 3), self.textColor)


def getMenu(name, player=None):
    if name == "test":
        return Menu("test", [["start", "AAAAA", "bbbbbbbbb", "some thing", "something", "other"],
                             ["ffffff", "aaaaaaaa", "+ěščřžýáíé", "1234567890"],
                             ["uuuuaaaaa", "sjdhf", "idk", "what", "else", "I"],
                             ["should", "put", "in" "here!!!!!!"]], 5, (255, 255, 255))
    if name == "start":
        return Menu("Maze3D", [["start", "quit"]], 15, (255, 255, 255), leftOffset=0.3, topOffset=0.3)
    if name == "paused":
        return Menu("Paused", [["continue", "quit"]], 15, (255, 255, 255), leftOffset=0.3, topOffset=0.3)
    if name == "endScreen":
        return Menu("You died", [["main menu", "retry", "quit"],
                                 ["score:", str(int(player.score * 100))]], 12, (255, 255, 255), leftOffset=0.2, topOffset=0.3)
