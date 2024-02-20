import asyncio
import pygame
import ast

with open('constants.txt','r') as f:
    lines = f.readlines()
glbls = ast.literal_eval(''.join(lines))

# importing the game states
from load_scores import LoadScores
from menu import Menu
from gameplay import GamePlay
from game import Game
from about import About

# initializing pygame and setting the screen resolution
pygame.init()
window = pygame.display.set_mode((glbls['WIDTH'], glbls['HEIGHT']))
pygame.display.set_caption(f"The computer broke.  Land it yourself.")

# Game states
glbls['STATES'] = {
    "LOADSCORES": LoadScores(glbls),
    "MENU": Menu(glbls),
    "GAMEPLAY": GamePlay(glbls),
    "ABOUT" : About(glbls)
}

# Game class instance
game = Game(window, glbls, "LOADSCORES")
asyncio.run(game.run())
