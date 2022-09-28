import tkinter as tk
from Memory.help_functions import print_rules, about
from Memory.game import Game


def launch_game() -> None:
    # GUI
    window = tk.Tk()
    window.title("Memory game")

    memory_game = Game(window)
    # menus
    top = tk.Menu(window)
    window.config(menu=top)
    jeu = tk.Menu(top, tearoff=False)
    top.add_cascade(label='Game', menu=jeu)
    submenu = tk.Menu(jeu, tearoff=False)
    jeu.add_cascade(label='New Game', menu=submenu)
    submenu.add_command(label='Dim 5x4', command=lambda x=0: memory_game.set_dim_and_start(x))
    submenu.add_command(label='Dim 5x6', command=lambda x=1: memory_game.set_dim_and_start(x))
    jeu.add_command(label='Close', command=window.destroy)

    players_menu = tk.Menu(top, tearoff=False)
    top.add_cascade(label='Players', menu=players_menu)
    one_player_menu = tk.Menu(players_menu, tearoff=False)
    players_menu.add_cascade(label='One player', menu=one_player_menu)
    one_player_menu.add_command(label='Alone', command=memory_game.play_alone)
    one_player_menu.add_command(label='Vs Computer', command=memory_game.play_against_ai)
    players_menu.add_command(label='2 players', command=memory_game.play_against_human)

    theme_menu = tk.Menu(top, tearoff=False)
    top.add_cascade(label='Theme', menu=theme_menu)
    theme_menu.add_command(label='Choose theme', command=memory_game.set_up_theme_frame)

    help_menu = tk.Menu(top, tearoff=False)
    top.add_cascade(label='Help', menu=help_menu)
    help_menu.add_command(label='How to play?', command=print_rules)
    help_menu.add_command(label='About', command=about)

    # Launch GUI
    window.mainloop()
