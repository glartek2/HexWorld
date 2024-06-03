class Ability:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def bonus_score_on_tile(self):
        return None, 0

    def bonus_score_on_attack(self):
        return 0

    def bonus_start_score(self):
        return 0

    def bonus_first_attack(self):
        return False

    def bonus_current_power(self):
        return False

    def bonus_defence(self):
        return 0, False

    def is_flying(self):
        return False


class Ancient(Ability):
    def bonus_score_on_tile(self):
        return "Desert", 1


class Hungry(Ability):
    def bonus_score_on_tile(self):
        return "Fruits", 1


class Victorious(Ability):
    def bonus_score_on_attack(self):
        return 1


class Wealthy(Ability):
    def bonus_start_score(self):
        return 8


class DinoTamers(Ability):
    def bonus_first_attack(self):
        return True

    def bonus_defence(self):
        return 10, True


class Lykanous(Ability):
    def bonus_current_power(self):
        return True


class Fortress(Ability):
    def bonus_defence(self):
        return 1, False


class Flying(Ability):
    def is_flying(self):
        return True


class AbilityFactory:
    @staticmethod
    def create_ability(name, number):
        ability_classes = {
            "Ancient": Ancient,
            "Hungry": Hungry,
            "Victorious": Victorious,
            "Wealthy": Wealthy,
            "Dino Tamers": DinoTamers,
            "Lykanous": Lykanous,
            "Fortress": Fortress,
            "Flying": Flying
        }
        ability_class = ability_classes.get(name, Ability)
        return ability_class(name, number)

