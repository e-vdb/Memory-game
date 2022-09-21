import tkinter as tk
from Memory.help_functions import print_rules, about
from Memory.game import Game

# GUI
window = tk.Tk()
window.title("Memory game")
frame = tk.Frame(window, height=500, width=500)
frame.pack(side=tk.TOP)
frame_cards = tk.Frame(window)
frame_cards.pack(side=tk.BOTTOM)

memory_game = Game(window, frame, frame_cards)
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

players_menu = tk.Menu(top,tearoff=False)
top.add_cascade(label='Players',menu=players_menu)
players_menu.add_command(label='1 player', command=lambda x=1: memory_game.set_nb_players_and_start(x))
players_menu.add_command(label='2 players', command=lambda x=2: memory_game.set_nb_players_and_start(x))

theme_menu = tk.Menu(top, tearoff=False)
top.add_cascade(label='Theme', menu=theme_menu)
theme_menu.add_command(label='Choose theme', command=memory_game.set_up_theme_frame)

help_menu = tk.Menu(top, tearoff=False)
top.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='How to play?', command=print_rules)
help_menu.add_command(label='About', command=about)

# Launch GUI
memory_game.set_up_theme_frame()
window.mainloop()
