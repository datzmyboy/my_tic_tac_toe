from GAME import Game,winner_for_columns,winner_for_diagonal,winner_for_row
import random

g = Game() # imported game class
while g.running: # inside the game class we have an instance of the menu class so that we can access some of the attributes
    g.menu.display_menu() # sample accesing display menu method in the menu class from Game Class
    if g.playing: # if the condtion is true play the game
        g.main_loop()
    if g.game2.playing2: # if the condtion is true play the game
        g.game2.main_loop2()