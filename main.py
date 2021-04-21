from copy import deepcopy
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo
from checkers.game import Game

game = Game()
chess_game = Game()
montecarlo = MonteCarlo(Node(chess_game))
