# Memory-game

## Summary 
Memory game for one player (solo mode) or two players.

Code written in python3 with graphics user interface (GUI) using Tkinter.

## Memory
Memory consists in finding pairs of cards.

To learn more about this game, visit https://en.wikipedia.org/wiki/Concentration_(card_game)

## Repository content
To play the game, save the following files in the same directory.

* Memory.py : Python script
* Images folder :  characters pictures (in .gif) for GUI 
* about.txt : plain text document that contains copyright and license information
  

## Tkinter interface

### Start-up interface

Choose characters for the memory among

*  Peanuts (by Charles M. Schulz)
*  Cartoon (images from https://www.apprendre-en-ligne.net/pj/memory/index.html )
*  Add your own theme !!!
     * Add a folder with characters images using the following name (carte-number.gif)
     * In the Python script, add the folder name to themeList=['Peanuts','Cartoon'] 


![theme](https://user-images.githubusercontent.com/82372483/120066821-91396b80-c078-11eb-919d-94f5eccfdf3d.png)

### Two players

Play with a friend

![2players](https://user-images.githubusercontent.com/82372483/120066843-aca47680-c078-11eb-8249-9032a438a1d4.png)


### One player (solo mode)

Play alone

![1player](https://user-images.githubusercontent.com/82372483/120066846-b29a5780-c078-11eb-9acc-1edab2e3d5b0.png)

![game](https://user-images.githubusercontent.com/82372483/120066908-1a50a280-c079-11eb-9c4b-4964744e7a09.png)


### About

From the GUI you can read license information.

## Tasks list
- [ ] Document code
- [x] Implement versus AI mode
- [ ] Implement versus AI mode with different difficulty levels
- [x] Add more themes
- [x] Add script to process images for memory game
