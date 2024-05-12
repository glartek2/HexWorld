import abilities
import spieces


class Civilization():
    def __init__(self, spieces, abilities):
        self.spieces = spieces
        self.ability = abilities
        self.number = spieces.number + abilities.number