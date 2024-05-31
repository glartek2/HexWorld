
class Spieces():
    def __init__(self, name, number):
        self.name = name
        self.number = number


    def can_attack_water(self):
        match self.name:
            case "Trytons":
                return True
            case _:
                return False

    def bonus_score(self):
        match self.name:
            case "Dwarves":
                return "Mine", 2
            case "Humans":
                return "Field", 1
            case "Sorcerers":
                return "Magic_Source", 2
            case _:
                return None, 0

    def bonus_defence(self):
        match self.name:
            case "Beastmans":
                return "Forest", 1
            case _:
                return None, 0

    def bonus_attack(self):
        match self.name:
            case "Giants":
                return "Mountain", 2
            case "Beastmans":
                return "Forest", 1
            case _:
                return None, 0

    def bonus_attack_power(self):
        match self.name:
            case "Sorcereres":
                return "Magic_Source", 1
            case _:
                return None, 0

    def death_handling(self):
        match self.name:
            case "Elves":
                return False
        return True


    def special_extinction(self):
        match self.name:
            case "Ghouls":
                return True
        return False
