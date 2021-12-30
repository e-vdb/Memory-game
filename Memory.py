#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:10:51 2021

@author: Emeline

Memory game with tkinter

Memory for one or two human players


"""

import random
import tkinter as tk
from help_functions import printRules, about

# global variables
turnedCards=0 # Number of visible cards
turnedCardsIm=[] # List of index of turned over cards
turnedCardNb=[] # List of index of played cards
foundCards=[] # List of index of found pairs 
cardsValues=[] # List of index of cards
playersNb=2
scorePlayer1=0
scorePlayer2=0
idCurrentPlayer=1
rowNb=5
colNb=4
cardsNb=colNb*rowNb # Total number of cards
pairsNb=cardsNb//2 # Number of different pairs
themeList=['Peanuts','Cartoon']
theme=random.choice(themeList)


def resetGlobal():
    '''
    Resets scores
    
    Returns
    -------
    None.

    '''
    global foundCards,scorePlayer1,scorePlayer2,idCurrentPlayer
    scorePlayer1=0
    scorePlayer2=0
    idCurrentPlayer=1
    foundCards=[]
  

def reinit(): 
    '''
    Hides all cards and resets the number of visible cards

    Returns
    -------
    None.

    '''
    global turnedCards,foundCards
    for i in range(cardsNb):
        if i not in foundCards:
            but_cards[i].configure(image=hiddenCard)
    turnedCards=0

 
def load_cards():
    '''
    Returns
    -------
    memoryCards : list
        List containing unique cards (images) chosen randomly for the memory game  

    '''
    global theme
    chosenCards=[]
    totalNb=17
    idCard=[i for i in range(1,totalNb+1)]
    chosenCards=random.sample(idCard,k=pairsNb)
    memoryCards=[tk.PhotoImage(file=str('Images/'+theme+'/carte-'+str(card)+'.gif')) for card in chosenCards]
    return memoryCards


def initiateGame():
    '''
    Returns
    -------
    mixedCards : list
        List of pairs of cards (images object) randomly mixed.

    '''
    memoryCards=load_cards()*2
    mixedCards=random.sample(memoryCards,k=len(memoryCards)) 
    return mixedCards


# Show visible face of cards 
def show(item):
    global turnedCards,foundCards
    if item not in foundCards:
        if turnedCards==0:
            but_cards[item].configure(image=cardsValues[item])
            turnedCards+=1
            turnedCardsIm.append(cardsValues[item])
            turnedCardNb.append(item)
        elif turnedCards==1:
            if item!=turnedCardNb[len(turnedCardNb)-1]:
                but_cards[item].configure(image=cardsValues[item])
                turnedCards+=1
                turnedCardsIm.append(cardsValues[item])
                turnedCardNb.append(item)
    if turnedCards==2:
        window.after(2000,check)

# Verify whether the chosen cards are identical
def check():
    global turnedCards,attempts,foundCards,playersNb
    if turnedCards==2: 
        if turnedCardsIm[len(turnedCardsIm)-1]==turnedCardsIm[len(turnedCardsIm)-2]:
            foundCards.append(turnedCardNb[len(turnedCardNb)-1])
            foundCards.append(turnedCardNb[len(turnedCardNb)-2])
            but_cards[turnedCardNb[len(turnedCardNb)-1]].configure(image=blankCard)
            but_cards[turnedCardNb[len(turnedCardNb)-2]].configure(image=blankCard)
            incrementScorePlayer()
        elif playersNb==2:
            switchPlayers()
        reinit()

 
def incrementScorePlayer():
    '''
    Increments the score of the current player

    Returns
    -------
    None.

    '''
    global scorePlayer1,scorePlayer2
    if idCurrentPlayer==1:
        scorePlayer1+=1
        lab_scorePlayer1.configure(text=str(scorePlayer1))
    elif idCurrentPlayer==2:
        scorePlayer2+=1
        lab_scorePlayer2.configure(text=str(scorePlayer2))


def switchPlayers():
    '''
    Switches current player

    Returns
    -------
    None.

    '''
    global idCurrentPlayer
    if idCurrentPlayer==1:
        idCurrentPlayer=2
        lab_Player1.configure(fg='black')
        lab_Player2.configure(fg='red')
    else:
        idCurrentPlayer=1
        lab_Player2.configure(fg='black')
        lab_Player1.configure(fg='red')

# Add a frame with hidden cards (buttons)
def frameCardsButtons():
    global but_cards,frameCards,cardsNb,rowNb,colNb,hiddenCard,theme
    filename='Images/'+theme+'/carte-0.gif'
    hiddenCard=tk.PhotoImage(file =filename)
    frameCards.destroy()
    frameCards=tk.Frame(window)
    frameCards.pack(side=tk.BOTTOM)
    but_cards=[]
    for i in range(cardsNb):
        but_cards.append(tk.Button(frameCards, image=hiddenCard,command=lambda x=i:show(x)))    
    for count in range(cardsNb):
        but_cards[count].grid(row=count//rowNb, column=count%rowNb)

def frameTheme():
    global frame,frameCards,themeList,themeCards
    frameCards.destroy()
    frame.destroy()
    frame=tk.Frame(window,height=500,width=500)
    frame.pack(side=tk.TOP)
    lab_Message=tk.Label(frame,text="Choose the theme you want to play with ")
    lab_Message.grid(row=0, column=1)
    but_themes=[]
    for count,themeCard in enumerate(themeCards):
        but_themes.append(tk.Button(frame, image=themeCard,command=lambda x=count:playTheme(x)))
    for count,but_theme in enumerate(but_themes):
        but_theme.grid(row=1, column=1+count)
        

def newGame5x4():
    '''
    Sets grid dimensions to 5x4 and lauches a new game

    Returns
    -------
    None.

    '''
    global cardsValues,rowNb,colNb,cardsNb,pairsNb,but_cards,frameCards
    rowNb=5
    colNb=4
    gameCurrentDim()
    

def newGame5x6():
    '''
    Sets grid dimensions to 5x6 and lauches a new game

    Returns
    -------
    None.

    '''
    global cardsValues,rowNb,colNb,cardsNb,pairsNb,frameCards
    rowNb=5
    colNb=6
    gameCurrentDim()


def onePlayer():
    '''
    Launches a new game for one player (solo mode)

    Returns
    -------
    None.

    '''
    global playersNb
    playersNb=1
    gameCurrentDim()
    

def twoPlayers():
    '''
    Launches a new game for two players

    Returns
    -------
    None.

    '''
    global playersNb
    playersNb=2
    gameCurrentDim()

   
def gameCurrentDim():
    '''
    Resets global variables and load a new memory to start a new game with current dimensions

    Returns
    -------
    None.

    '''
    global cardsValues,rowNb,colNb,cardsNb,pairsNb,frameCards,playersNb
    if playersNb==1:
        stat1player()
    else:
        displayScore()
    cardsNb=colNb*rowNb 
    pairsNb=cardsNb//2 
    cardsValues=initiateGame()
    resetGlobal()
    frameCardsButtons()

def playTheme(x):
    global theme
    theme=themeList[x]
    gameCurrentDim()

def displayScore():
    global lab_Player1,lab_Player2,lab_scorePlayer1,lab_scorePlayer2,frame
    frame.destroy()
    frame=tk.Frame(window)
    frame.pack(side=tk.TOP)
    lab_Player1=tk.Label(frame,text='PLAYER 1 : ',font=("Helvetica",20),fg='red')
    lab_Player1.pack(side=tk.LEFT)
    
    lab_scorePlayer1=tk.Label(frame,text='0', font=("Helvetica", 20))
    lab_scorePlayer1.pack(side=tk.LEFT)
    
    lab_Player2=tk.Label(frame,text='  PLAYER 2 : ',font=("Helvetica",20),fg='black')
    lab_Player2.pack(side=tk.LEFT)
    
    lab_scorePlayer2=tk.Label(frame,text='0', font=("Helvetica", 20))
    lab_scorePlayer2.pack(side=tk.LEFT)

def stat1player():
    global frame,lab_Player1,lab_scorePlayer1
    frame.destroy()
    frame=tk.Frame(window)
    frame.pack(side=tk.TOP)
    lab_Player1=tk.Label(frame,text='Pairs of cards = ',font=("Helvetica",20),fg='black')
    lab_Player1.pack(side=tk.LEFT)
    lab_scorePlayer1=tk.Label(frame,text='0', font=("Helvetica", 20))
    lab_scorePlayer1.pack(side=tk.LEFT)



############################################################################################


# graphics window
window = tk.Tk()
window.title("Memory game")
frame=tk.Frame(window,height=500,width=500)
frame.pack(side=tk.TOP)
frameCards=tk.Frame(window)
frameCards.pack(side=tk.BOTTOM)

# menus
top = tk.Menu(window)
window.config(menu=top)
jeu = tk.Menu(top, tearoff=False)
top.add_cascade(label='Game', menu=jeu)
submenu = tk.Menu(jeu, tearoff=False)
jeu.add_cascade(label='New Game', menu=submenu)
submenu.add_command(label='Dim 5x4', command=newGame5x4)
submenu.add_command(label='Dim 5x6', command=newGame5x6)
jeu.add_command(label='Close', command=window.destroy)

players_menu = tk.Menu(top,tearoff=False)
top.add_cascade(label='Players',menu=players_menu)
players_menu.add_command(label='1 player',command=onePlayer)
players_menu.add_command(label='2 players',command=twoPlayers)

themeMenu = tk.Menu(top,tearoff=False)
top.add_command(label='Choose theme',command=frameTheme)

help_menu = tk.Menu(top, tearoff=False)
top.add_cascade(label='Help',menu=help_menu)
help_menu.add_command(label='How to play?', command=printRules)
help_menu.add_command(label='About', command=about)


# images 
blankCard = tk.PhotoImage(file='Images/blankCard.gif')
themeCards = [tk.PhotoImage(file=str('Images/'+theme+'/carte-1.gif')) for theme in themeList]
    
# start-up
frameTheme()
window.mainloop()

