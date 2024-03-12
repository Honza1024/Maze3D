class Object:

    def __init__(self, typ, pos, sprite, health = False):
        self.typ = typ
        self.pos = (pos[0] + 1, pos[1] + 1)
        self.sprite = sprite
        self.health = health