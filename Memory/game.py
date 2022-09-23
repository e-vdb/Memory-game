from Memory.player import Player
from Memory.ai_player import AIPlayer
from random import choice, sample
import tkinter as tk
from typing import List
from pathlib import Path
from os.path import dirname, join
from time import sleep


IMAGES_FOLDER = join(Path(dirname(__file__)).parent, 'Images')


class Game:

    def __init__(self, window):#, frame, frame_cards):
        self.THEMES = ['peanuts', 'Cartoon']
        self.BLANK_CARD = tk.PhotoImage(file=f'{IMAGES_FOLDER}/blankCard.gif')
        self.THEME_CARDS = [tk.PhotoImage(file=str(f'{IMAGES_FOLDER}/{theme}/carte-1.gif')) for theme in self.THEMES]
        self.player_nb = 1
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.game_over = False

        self.game_mode = "Alone"
        self.ai_player = AIPlayer('AI Player')
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
        self.radio_button_choice = tk.IntVar()
        self.set_radio_buttons()
        self.main_frame = tk.Frame(self.window, height=500, width=500)
        self.cards_frame = tk.Frame(self.window)
        self.set_up_theme_frame()

    def set_initial_game_parameters(self):
        CHOICES = {0: {'mode': 'Alone', 'nb_player': 1},
                   1: {'mode': 'Against AI', 'nb_player': 2},
                   2: {'mode': 'Against Player', 'nb_player': 2}
                   }
        x = self.radio_button_choice.get()
        self.player_nb = CHOICES[x]['nb_player']
        self.game_mode = CHOICES[x]['mode']

    def set_radio_buttons(self):
        self.R1 = tk.Radiobutton(self.window, text="Player alone",
                                 command=self.set_initial_game_parameters, variable=self.radio_button_choice, value=0)
        self.R1.pack(side=tk.LEFT)
        self.R2 = tk.Radiobutton(self.window, text="Player against computer",
                                 command=self.set_initial_game_parameters, variable=self.radio_button_choice, value=1)
        self.R2.pack(side=tk.LEFT)
        self.R3 = tk.Radiobutton(self.window, text="Player against Player",
                                 command=self.set_initial_game_parameters, variable=self.radio_button_choice, value=2)
        self.R3.pack(side=tk.LEFT)

    def remove_radio_buttons(self):
        self.R1.pack_forget()
        self.R2.pack_forget()
        self.R3.pack_forget()

    def set_game_over(self):
        if len(self.found_cards) == self.cards_nb:
            self.game_over = True
            self.open_game_over_window()

    def open_game_over_window(self):
        game_over_window = tk.Toplevel(self.window)
        game_over_window.title("Game Over")
        game_over_window.geometry("300x200")
        label = tk.Label(game_over_window, text="Game Over")
        label.pack()

    def switch_players(self) -> None:
        """
        Switches the current player.

        Returns
        -------
        None.
        """
        if not self.game_over:

            if self.current_player == self.player1:
                self.current_player = self.player2
                self.player1.can_play = False
                self.player2.can_play = True
                self.lab_player1.configure(fg='black')
                self.lab_player2.configure(fg='red')
                if self.game_mode == "Against AI":
                    self.window.after(1000, self.ai_player_turn)
            else:
                self.current_player = self.player1
                self.player1.can_play = True
                self.player2.can_play = False
                self.lab_player2.configure(fg='black')
                self.lab_player1.configure(fg='red')
        else:
            self.player2.can_play = False
            self.player1.can_play = False

    def ai_player_turn(self):
        possible_cards_ids = [i for i in range(self.cards_nb) if i not in self.found_cards]
        first_card, second_card = self.ai_player.play_random_cards(possible_cards_ids)

        self.show_one_card(first_card)
        self.show_one_card(second_card)
        self.window.after(2000, self.check)

    def show_one_card(self, card_id):
        self.but_cards[card_id].configure(image=self.cards_ids[card_id])
        self.turned_cards_nb += 1
        self.turned_cards_ids.append(self.cards_ids[card_id])
        self.turned_card_played.append(card_id)

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
        self.turned_cards_nb = 0
        self.found_cards = []
        self.turned_cards_ids = []
        self.turned_card_played = []

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
        self.remove_radio_buttons()
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
                self.set_game_over()
                if self.game_mode == "Against AI" and self.current_player == self.player2 and not self.game_over:
                    self.window.after(1000, self.ai_player_turn)
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
        Resets game parameters and load a new memory to start a new game with set dimensions and players.

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
        self.player1.can_play = True
        self.player2.can_play = False

    def start_theme(self, x):
        self.theme = self.THEMES[x]
        self.start_new_game()

    def display_players_score(self) -> None:
        """ Set up the frame with the names and scores of both players. """
        self.main_frame.destroy()
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(side=tk.TOP)
        self.lab_player1 = tk.Label(self.main_frame, text=f' {self.player1.name.upper()} : ', font=("Helvetica", 20), fg='red')
        self.lab_player1.pack(side=tk.LEFT)

        self.lab_score_player1 = tk.Label(self.main_frame, text='0', font=("Helvetica", 20))
        self.lab_score_player1.pack(side=tk.LEFT)

        self.lab_player2 = tk.Label(self.main_frame, text=f' {self.player2.name.upper()} : ', font=("Helvetica", 20), fg='black')
        self.lab_player2.pack(side=tk.LEFT)

        self.lab_score_player2 = tk.Label(self.main_frame, text='0', font=("Helvetica", 20))
        self.lab_score_player2.pack(side=tk.LEFT)

    def display_stat_1player(self):
        """ Set up the frame with the name and score of the player. """
        self.main_frame.destroy()
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(side=tk.TOP)
        self.lab_player1 = tk.Label(self.main_frame, text='Pairs of cards = ', font=("Helvetica", 20), fg='black')
        self.lab_player1.pack(side=tk.LEFT)
        self.lab_score_player1 = tk.Label(self.main_frame, text='0', font=("Helvetica", 20))
        self.lab_score_player1.pack(side=tk.LEFT)

    def increment_score_player(self) -> None:
        """ Increments the score of the current player. """
        self.current_player.increment_score()
        if self.current_player == self.player1:
            #self.player1.increment_score()
            self.lab_score_player1.configure(text=str(self.player1.score))
        else:
            #self.player2.increment_score()
            self.lab_score_player2.configure(text=str(self.player2.score))

    def set_dim_and_start(self, x):
        self.game_dim = self.DIMENSIONS[x]
        self.cards_nb = self.game_dim[0] * self.game_dim[1]
        self.start_new_game()

    def play_against_human(self):
        self.player_nb = 2
        self.player1 = Player('Player 1')
        self.player2 = Player('Player 2')
        self.current_player = self.player1
        self.start_new_game()

    def play_alone(self):
        self.player_nb = 1
        self.game_mode = 'Alone'
        self.start_new_game()

    def play_against_ai(self):
        self.player_nb = 2
        self.game_mode = 'Against AI'
        self.player1 = Player('Human')
        self.player2 = AIPlayer('AI')
        self.current_player = self.player1
        self.start_new_game()
