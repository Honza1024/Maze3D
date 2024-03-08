import mapa


class Player:

    def __init__(self, pos, dir):
        self.position = [pos[0], pos[1]]
        self.direction = dir
        self.fov = 1.2
        self.noDeformation = True
        self.speed = 1
        self.sensitivity = 0.05
        self.thickness = 0.06


    def collide(self, mapArray):
        #if inside a wall, get pushed away
        if mapa.isWall(int(self.position[0]), int(self.position[1]), mapArray):
            pass #find closest side and move there
        # keep some distance from walls
        if self.position[0] % 1 < self.thickness:
            if mapa.isWall(int(self.position[0]) - 1, int(self.position[1]), mapArray):
                self.position[0] += self.thickness - (self.position[0] % 1)
        if self.position[0] % 1 > 1 - self.thickness:
            if mapa.isWall(int(self.position[0]) + 1, int(self.position[1]), mapArray):
                self.position[0] -= self.thickness - (1 - (self.position[0] % 1))
        if self.position[1] % 1 < self.thickness:
            if mapa.isWall(int(self.position[0]), int(self.position[1]) - 1, mapArray):
                self.position[1] += self.thickness - (self.position[1] % 1)
        if self.position[1] % 1 > 1 - self.thickness:
            if mapa.isWall(int(self.position[0]), int(self.position[1]) + 1, mapArray):
                self.position[1] -= self.thickness - (1 - (self.position[1] % 1))
