import random
import numpy as np
from copy import deepcopy
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo
from checkers.game import Game
import InputBuilder
import ResNetCheckers
import MCTS
##### PETLA GIER



def selfplay(numbgame, Model):
    for i in range(numbgame):

        game = Game()

        montecarlo = MonteCarlo(Node(game))
        mcts = MCTS(Model)
        montecarlo.child_finder = mcts.child_finder
        while not (game.is_over()):
            montecarlo.simulate(1600)
            if(len(game.moves) <20):
                montecarlo.root_node = montecarlo.make_exploratory_choice()
            else:
                montecarlo.root_node = montecarlo.make_choice()
            game.move(montecarlo.root_node[-1])
            prob = 
        game.get_winner()




        board_size_x = game.board.width  # 4
        board_size_y = game.board.height  # 8

historicalBoards = InputBuilder.HistoricalBoards()
      #  theModel = ResNetCheckers.build()


while not (game.is_over()):
    x = InputBuilder.build_board_planes(17, historicalBoards, game)
    possible_moves = game.get_possible_moves()
    rand_v = random.choice(possible_moves)
    game.move(rand_v)
    x = x[np.newaxis, :, :]
    policy, value = theModel.predict(x)
    print("CICHAJ")
