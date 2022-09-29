from Memory.player import Player
from random import choice
import tkinter as tk


class AIPlayer(Player):
    """A class to represent an AI player in a memory game."""

    def __init__(self, name='AIPlayer'):
        super().__init__(name)
        self.memory_board = {}

    def reset_score(self):
        self.score = 0
        self.memory_board = {}

    @staticmethod
    def play_random_cards(cards_ids):
        """AI player plays a turn."""
        first_card = choice(cards_ids)
        second_card = choice([id_card for id_card in cards_ids if id_card != first_card])
        return first_card, second_card

    @staticmethod
    def play_one_random_card(cards_ids):
        return choice(cards_ids)

    def remembers_card(self, card_id, image):
        try:
            if card_id not in self.memory_board[image]['position']:
                self.memory_board[image]['position'].append(card_id)
        except KeyError:
            self.memory_board[image] = {'position': [card_id]}

    def search_pairs(self):
        return next((list_ids['position'] for image, list_ids in self.memory_board.items()
                     if len(list_ids['position']) == 2), None)

    def search_matching_card(self, card_id, image):
        try:
            return next(id_card for id_card in self.memory_board[image]['position'] if id_card != card_id)
        except KeyError:
            return None

    def erase_found_cards(self, image):
        self.memory_board.pop(image)
