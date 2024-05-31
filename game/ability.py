


class Ability():

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def bonus_score_on_tile(self):
        match self.name:
            case "Ancient":
                return "Desert", 1
            case "Hungry":
                return "Fruits", 1
            case _:
                return None, 0

    def bonus_score_on_attack(self):
        match self.name:
            case "Victorious":
                return 1
            case _:
                return 0

    def bonus_start_score(self):
        match self.name:
            case "Wealthy":
                return 8
            case _:
                return 0

    def bonus_first_attack(self):
        match self.name:
            case "Dino Tamers":
                return True
            case _:
                return False


    def bonus_current_power(self):
        match self.name:
            case "Lykanous":
                return True
            case _:
                return False

    def bonus_defence(self):
        match self.name:
            case "Fortress":
                return 1, False
            case "Dino Tamers":
                return 10, True
            case _:
                return 0, False

    def is_flying(self):
        match self.name:
            case "Flying":
                return True
            case _:
                return False
