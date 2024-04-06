

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.current_spiece = None
        self.current_ability = None
        self.old_spiece = None
        self.old_ability = None