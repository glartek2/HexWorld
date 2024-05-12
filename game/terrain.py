
class Terrain:
    def __init__(self, name, image, defence, isWater = False):
        self.name = name
        self.image = image
        self.isWater = isWater
        self.defence = defence