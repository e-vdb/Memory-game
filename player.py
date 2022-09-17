

class Player:
    """A class to represent a player in a memory game."""
    def __init__(self, name='Player'):
        self.score = 0
        self.name = name

    def reset_score(self):
        self.score = 0

    def increment_score(self):
        self.score += 1
