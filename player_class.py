import mapa


class Player:

    def __init__(self, pos, dir):
        self.position = [pos[0], pos[1]]
        self.direction = dir
        self.fov = 1.2
        self.noDeformation = True
        self.speed = 1.5
        self.sensitivity = 0.05
        self.thickness = 0.06


    def collide(self, mapArray):
        #if inside a wall, get pushed away
        if mapa.isWall(int(self.position[0]), int(self.position[1]), mapArray):
            relativeX = (self.position[0] % 1) - 0.5
            relativeY = (self.position[1] % 1) - 0.5
            iteration = 1
            while True: #find closest free tile
                freeTiles = []
                for x in range(-iteration, iteration + 1):
                    for y in range(-iteration, iteration + 1):
                        if x == 0 and y == 0:
                            continue
                        if not mapa.isWall(int(self.position[0] + x * iteration), int(self.position[1] + y * iteration), mapArray):
                            freeTiles.append((x, y))
                if len(freeTiles):
                    break
                iteration += 1
            distances = []
            for tile in freeTiles:
                distances.append((self.position[0] - (int(self.position[0]) + tile[0] + 0.5)) ** 2 + (self.position[1] - (int(self.position[1]) + tile[1] + 0.5)) ** 2)
            closest = freeTiles[distances.index(min(distances))]
            # teleport to the closest tile
            if closest[0] != 0:
                self.position[0] = int(self.position[0]) + closest[0] + (self.thickness if closest[0] > 0 else 1 - self.thickness)
            if closest[1] != 0:
                self.position[1] = int(self.position[1]) + closest[1] + (self.thickness if closest[1] > 0 else 1 - self.thickness)
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
