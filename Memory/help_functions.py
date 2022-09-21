"""Define help functions for GUI menu."""

import tkinter as tk
from pathlib import Path
from os.path import dirname, join

TEXT_FOLDER = join(Path(dirname(__file__)).parent, 'text_files')


def print_rules() -> None:
    """
    Display rules and gameplay.

    Load a text files 'rules_eng.txt'.
    Open a second window.
    Write the content of the text document.
    Returns
    -------
    None.
    """
    ruleWindow = tk.Toplevel()
    ruleWindow.resizable(False, False)
    ruleWindow.title("How to play?")
    with open(f'{TEXT_FOLDER}/rules_eng.txt') as f:
        gameRules = f.read()
    lab_Rule = tk.Label(ruleWindow, text=gameRules,
                        fg="black", anchor="e", justify=tk.LEFT)
    lab_Rule.pack(side=tk.TOP)
    ruleWindow.mainloop()


def about() -> None:
    """
    Display licence information.

    Load the text document 'about.txt'.
    Open a secondary window.
    Write the content of the text document.

    Returns
    -------
    None.
    """
    aboutWindow = tk.Toplevel()
    aboutWindow.title("About")
    with open(f'{TEXT_FOLDER}/about.txt') as f:
        about = f.read()
    lbl_about = tk.Label(aboutWindow, text=about,
                         fg="black", anchor="e", justify=tk.LEFT)
    lbl_about.pack(side=tk.TOP)
    aboutWindow.mainloop()
