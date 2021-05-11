import random
import numpy as np
from copy import deepcopy
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo
from checkers.game import Game
import InputBuilder
import ResNetCheckers


game = Game()
board_size_x = game.board.width  # 4
board_size_y = game.board.height  # 8
montecarlo = MonteCarlo(Node(game))
historicalBoards = InputBuilder.HistoricalBoards()
theModel = ResNetCheckers.build()

while not (game.is_over()):
    x = InputBuilder.build_board_planes(17, historicalBoards, game)
    possible_moves = game.get_possible_moves()
    rand_v = random.choice(possible_moves)
    game.move(rand_v)
    x = x[np.newaxis, :, :]
    policy, value = theModel.predict(x)
    print("CICHAJ")