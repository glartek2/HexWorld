import ability
import spieces


class Civilization():
    def __init__(self, spieces, ability):
        self.spieces = spieces
        self.ability = ability
        self.number = spieces.number + ability.number