from Memory.player import Player
from random import choice, sample
import tkinter as tk
from typing import List
from pathlib import Path
from os.path import dirname, join


IMAGES_FOLDER = join(Path(dirname(__file__)).parent, 'Images')


class Game:

    def __init__(self, window, frame, frame_cards):
        self.THEMES = ['peanuts', 'Cartoon']
        self.BLANK_CARD = tk.PhotoImage(file=f'{IMAGES_FOLDER}/blankCard.gif')
        self.THEME_CARDS = [tk.PhotoImage(file=str(f'{IMAGES_FOLDER}/{theme}/carte-1.gif')) for theme in self.THEMES]
        self.player_nb = 2
        self.player1 = Player('Player 1')
        self.player2 = Player('Player 2')
        self.current_player = self.player1
        self.DIMENSIONS = [(5, 4), (6, 4)]
        self.game_dim = self.DIMENSIONS[0]
        self.cards_nb = self.game_dim[0] * self.game_dim[1]
        self.pairs_nb = self.cards_nb // 2
        self.theme = choice(self.THEMES)
        self.hidden_card = tk.PhotoImage(file=f'{IMAGES_FOLDER}/{self.theme}/carte-0.gif')
        self.turned_cards_nb = 0  # Number of visible cards
        self.turned_cards_ids = []  # List of index of turned over cards
        self.turned_card_played = []  # List of index of played cards
        self.found_cards = []  # List of index of found pairs
        self.cards_ids = []  # List of index of cards
        self.window = window
        self.main_frame = frame
        self.cards_frame = frame_cards

    def switch_players(self) -> None:
        """
        Switches the current player.

        Returns
        -------
        None.
        """
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.lab_player1.configure(fg='black')
            self.lab_player2.configure(fg='red')
        else:
            self.current_player = self.player1
            self.lab_player2.configure(fg='black')
            self.lab_player1.configure(fg='red')

    def reset_scores(self) -> None:
        """
        Resets scores of both players.
        Returns
        -------
        None.
        """
        self.player1.reset_score()
        self.player2.reset_score()

    def reset_game(self):
        self.reset_scores()
        self.current_player = self.player1
        self.found_cards = []

    def load_cards(self) -> List[tk.PhotoImage]:
        """
        Loads the cards images and returns a list of cards

        Returns
        -------
        List[tk.PhotoImage]
            List containing unique cards (images) chosen randomly for the memory game

        """

        total_nb = 17
        ids_cards = list(range(1, total_nb + 1))
        chosen_cards = sample(ids_cards, k=self.pairs_nb)
        return [tk.PhotoImage(file=str(f'{IMAGES_FOLDER}/{self.theme}/carte-{str(card)}.gif')) for card in chosen_cards]

    def initiate_game(self) -> List[tk.PhotoImage]:
        """
        Returns
        -------
        List[tk.PhotoImage]
            List of pairs of cards (images object) randomly mixed.

        """
        memory_cards = self.load_cards() * 2
        return sample(memory_cards, k=len(memory_cards))

    def set_up_theme_frame(self):
        self.cards_frame.destroy()
        self.main_frame.destroy()
        self.main_frame = tk.Frame(self.window, height=500, width=500)
        self.main_frame.pack(side=tk.TOP)
        lab_Message = tk.Label(self.main_frame, text="Choose the theme you want to play with ")
        lab_Message.grid(row=0, column=1)
        but_themes = []
        for count, theme_card in enumerate(self.THEME_CARDS):
            but_themes.append(tk.Button(self.main_frame, image=theme_card, command=lambda x=count: self.start_theme(x)))
        for count, but_theme in enumerate(but_themes):
            but_theme.grid(row=1, column=1 + count)

    def set_up_memory_frame(self):
        self.cards_frame.destroy()
        self.cards_frame = tk.Frame(self.window)
        self.cards_frame.pack(side=tk.BOTTOM)
        self.but_cards = []
        for i in range(self.cards_nb):
            self.but_cards.append(tk.Button(self.cards_frame, image=self.hidden_card, command=lambda x=i: self.show(x)))
        for count in range(self.cards_nb):
            self.but_cards[count].grid(row=count // self.game_dim[0], column=count % self.game_dim[0])

    # Show visible face of cards
    def show(self, item):

        if item not in self.found_cards:
            if self.turned_cards_nb == 0:
                self.but_cards[item].configure(image=self.cards_ids[item])
                self.turned_cards_nb += 1
                self.turned_cards_ids.append(self.cards_ids[item])
                self.turned_card_played.append(item)
            elif self.turned_cards_nb == 1:
                if item != self.turned_card_played[len(self.turned_card_played) - 1]:
                    self.but_cards[item].configure(image=self.cards_ids[item])
                    self.turned_cards_nb += 1
                    self.turned_cards_ids.append(self.cards_ids[item])
                    self.turned_card_played.append(item)
        if self.turned_cards_nb == 2:
            self.window.after(2000, self.check)

    def check(self):

        if self.turned_cards_nb == 2:
            if self.turned_cards_ids[len(self.turned_cards_ids) - 1] == self.turned_cards_ids[len(self.turned_cards_ids) - 2]:
                self.found_cards.append(self.turned_card_played[len(self.turned_card_played) - 1])
                self.found_cards.append(self.turned_card_played[len(self.turned_card_played) - 2])
                self.but_cards[self.turned_card_played[len(self.turned_card_played) - 1]].configure(image=self.BLANK_CARD)
                self.but_cards[self.turned_card_played[len(self.turned_card_played) - 2]].configure(image=self.BLANK_CARD)
                self.increment_score_player()
            elif self.player_nb == 2:
                self.switch_players()
            self.reinit()

    def reinit(self):
        """
        Hides all cards and resets the number of visible cards

        Returns
        -------
        None.

        """

        for i in range(self.cards_nb):
            if i not in self.found_cards:
                self.but_cards[i].configure(image=self.hidden_card)
        self.turned_cards_nb = 0

    def start_new_game(self):
        """
        Resets global variables and load a new memory to start a new game with current dimensions

        Returns
        -------
        None.

        """

        if self.player_nb == 1:
            self.display_stat_1player()
        else:
            self.display_players_score()

        self.cards_ids = self.initiate_game()
        self.reset_game()
        self.set_up_memory_frame()

    def start_theme(self, x):
        self.theme = self.THEMES[x]
        self.start_new_game()

    def display_players_score(self) -> None:
        self.main_frame.destroy()
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(side=tk.TOP)
        self.lab_player1 = tk.Label(self.main_frame, text='PLAYER 1 : ', font=("Helvetica", 20), fg='red')
        self.lab_player1.pack(side=tk.LEFT)

        self.lab_score_player1 = tk.Label(self.main_frame, text='0', font=("Helvetica", 20))
        self.lab_score_player1.pack(side=tk.LEFT)

        self.lab_player2 = tk.Label(self.main_frame, text='  PLAYER 2 : ', font=("Helvetica", 20), fg='black')
        self.lab_player2.pack(side=tk.LEFT)

        self.lab_score_player2 = tk.Label(self.main_frame, text='0', font=("Helvetica", 20))
        self.lab_score_player2.pack(side=tk.LEFT)

    def display_stat_1player(self):

        self.main_frame.destroy()
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(side=tk.TOP)
        self.lab_player1 = tk.Label(self.main_frame, text='Pairs of cards = ', font=("Helvetica", 20), fg='black')
        self.lab_player1.pack(side=tk.LEFT)
        self.lab_score_player1 = tk.Label(self.main_frame, text='0', font=("Helvetica", 20))
        self.lab_score_player1.pack(side=tk.LEFT)

    def increment_score_player(self) -> None:
        """
        Increments the score of the current player.

        Returns
        -------
        None.

        """

        if self.current_player == self.player1:
            self.player1.increment_score()
            self.lab_score_player1.configure(text=str(self.player1.score))
        else:
            self.player2.increment_score()
            self.lab_score_player2.configure(text=str(self.player2.score))

    def set_dim_and_start(self, x):
        self.game_dim = self.DIMENSIONS[x]
        self.cards_nb = self.game_dim[0] * self.game_dim[1]
        self.start_new_game()

    def set_nb_players_and_start(self, x):
        self.player_nb = x
        self.start_new_game()
