class Species:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def can_attack_water(self):
        return False

    def bonus_score(self):
        return None, 0

    def bonus_defence(self):
        return None, 0

    def bonus_attack(self):
        return None, 0

    def bonus_attack_power(self):
        return None, 0

    def death_handling(self):
        return True

    def special_extinction(self):
        return False


class Trytons(Species):
    def can_attack_water(self):
        return True


class Dwarves(Species):
    def bonus_score(self):
        return "Mine", 2


class Humans(Species):
    def bonus_score(self):
        return "Field", 1


class Sorcerers(Species):
    def bonus_score(self):
        return "Magic_Source", 2

    def bonus_attack_power(self):
        return "Magic_Source", 1


class Beastmans(Species):
    def bonus_defence(self):
        return "Forest", 1

    def bonus_attack(self):
        return "Forest", 1


class Giants(Species):
    def bonus_attack(self):
        return "Mountain", 2


class Elves(Species):
    def death_handling(self):
        return False


class Ghouls(Species):
    def special_extinction(self):
        return True


class SpeciesFactory:
    @staticmethod
    def create_species(name, number):
        species_classes = {
            "Trytons": Trytons,
            "Dwarves": Dwarves,
            "Humans": Humans,
            "Sorcerers": Sorcerers,
            "Beastmans": Beastmans,
            "Giants": Giants,
            "Elves": Elves,
            "Ghouls": Ghouls
        }
        species_class = species_classes.get(name, Species)
        return species_class(name, number)
