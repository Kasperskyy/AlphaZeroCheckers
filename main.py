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
Model = None
historicalBoards = None
game = None
currInput = None


def selfplay(numbgame, model):
    global game, Model, historicalBoards, currInput
    Model = model

    for i in range(numbgame):
        game = Game()

        montecarlo = MonteCarlo(Node(game))
        gameData = np.array()
        historicalBoards = InputBuilder.HistoricalBoards()
        montecarlo.child_finder = child_finder
        montecarlo.root_node.player_number = game.state.whose_turn()

        while not (game.is_over()):
            currInput = InputBuilder.build_board_planes(17, historicalBoards, game)
            montecarlo.simulate(1)          # 1600
            if len(game.moves) < 20:
                montecarlo.root_node = montecarlo.make_exploratory_choice()
            else:
                montecarlo.root_node = montecarlo.make_choice()

            # add boardstate
            gameState = InputBuilder.build_board_planes(17, currInput, game)

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


def child_finder(node, self):
    x = currInput
    x = x[np.newaxis, :, :]
    expert_policy_values, win_value = Model.predict(x)
    for move in node.state.get_possible_moves():
        child = Node(deepcopy(node.state))
        child.state.move(move)
        child.player_number = child.state.whose_turn()
        child.policy_value = InputBuilder.get_child_policy_value(move, expert_policy_values)  # should return a probability value between 0 and 1
        node.add_child(child)
    node.update_win_value(win_value)

