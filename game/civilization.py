import ability
import species


class Civilization():
    def __init__(self, species, ability):
        self.species = species
        self.ability = ability
        self.number = species.number + ability.number