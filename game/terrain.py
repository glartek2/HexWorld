
class Terrain:
    def __init__(self, image, defence, isWater = False):
        self.image = image
        self.isWater = isWater
        self.defence = defence