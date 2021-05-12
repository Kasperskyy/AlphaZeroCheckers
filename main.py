import random
import numpy as np
from copy import deepcopy
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo
from checkers.game import Game
import InputBuilder
import ResNetCheckers
import MonteCarlo


##### PETLA GIER


def selfplay(numbgame, Model):
    for i in range(numbgame):

        game = Game()

        montecarlo = MonteCarlo(Node(game))
        mcts = MonteCarlo.MCTS(Model)
        gameData = np.array()
        montecarlo.child_finder = mcts.child_finder

        while not (game.is_over()):
            historicalBoards = InputBuilder.HistoricalBoards()
            montecarlo.simulate(1600)
            if len(game.moves) < 20:
                montecarlo.root_node = montecarlo.make_exploratory_choice()
            else:
                montecarlo.root_node = montecarlo.make_choice()

            # add boardstate
            gameState = InputBuilder.build_board_planes(17, historicalBoards, game)

            game.move(montecarlo.root_node[-1])

            # add probabilities
            probabilities = Node.get_score(montecarlo.root_node)        # TO DO - check if get_score is what we need

            moveData = np.array(gameState, probabilities)  # moveData[]= consists of 3 elements- the game state, the search probabilities, the winner(added after game is over)
            # gameData.app [nalesnikPauliny, probabilities, gamevalue(-1/0/1)]

        winner = game.get_winner()
        if winner == 1:     # black
            gameValue = 1
        elif winner is None:
            gameValue = 0
        else:
            gameValue = -1
        moveData = np.append(gameValue)
        gameData = np.append(moveData)

        # array of moves.app(gameData)
        history_moves = np.array(game.moves())
        trainingSet = history_moves.append(gameData)   #  [array of moves [nalesnikPauliny, gamevalue(-1/0/1) , probabilities]  ]

        board_size_x = game.board.width  # 4
        board_size_y = game.board.height  # 8


historicalBoards = InputBuilder.HistoricalBoards()
#  theModel = ResNetCheckers.build()
