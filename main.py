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
        # gameData[]
        montecarlo.child_finder = mcts.child_finder
        while not (game.is_over()):
           #moveData[]= consists of 3 elements- the game state, the search probabilties, the winner(added after game is over)
            montecarlo.simulate(1600)
            if(len(game.moves) <20):
                montecarlo.root_node = montecarlo.make_exploratory_choice()
            else:
                montecarlo.root_node = montecarlo.make_choice()
            game.move(montecarlo.root_node[-1])
            #add boardstate
            #add probabilities
            #gameData.app [nalesnikPauliny, gamevalue(-1/0/1) , probabilities]
        game.get_winner()
        #petla zeby dodac odpowiednie game value

    #array of moves.app(gameData)
#  [array of moves [nalesnikPauliny, gamevalue(-1/0/1) , probabilities]  ]


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
