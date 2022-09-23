from Memory.player import Player
from random import choice


class AIPlayer(Player):
    """A class to represent an AI player in a memory game."""

    def __init__(self, name='AIPlayer'):
        super().__init__(name)

    def play_random_cards(self, cards_ids):
        """AI player plays a turn."""
        first_card = choice(cards_ids)
        second_card = choice([id_card for id_card in cards_ids if id_card != first_card])
        return first_card, second_card
