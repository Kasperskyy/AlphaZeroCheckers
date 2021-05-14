import random
import numpy as np
from copy import deepcopy
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo
from checkers.game import Game
import InputBuilder
import ResNetCheckers

##### PETLA GIER
Model = None
historicalBoards = None
game = None
currInput = None


def selfplay(numbgame, model):
    global game, Model, historicalBoards, currInput
    Model = model
    totalData = []
    for i in range(numbgame):
        game = Game()

        montecarlo = MonteCarlo(Node(game))
        gameData = []
        historicalBoards = InputBuilder.HistoricalBoards()
        montecarlo.child_finder = child_finder
        print("game " + str(i))
        montecarlo.root_node.player_number = game.whose_turn()

        while not (game.is_over()):
            # game state
            currInput = InputBuilder.build_board_planes(17, historicalBoards, game)
            print("turn " + str(len(game.moves)))
            montecarlo.simulate(500)  # 1600 #dont put a value less than 2 !

            probabilities_value = montecarlo.get_probabilities()
            probabilities = InputBuilder.convert_to_output(game.get_possible_moves(), probabilities_value)
            currPlayer = game.whose_turn()

            if len(game.moves) < 20:
                montecarlo.root_node = montecarlo.make_exploratory_choice()
            else:
                montecarlo.root_node = montecarlo.make_choice()
            montecarlo.root_node.visits = 0

            game.move(montecarlo.root_node.state.moves[-1])
            gameData.append((currInput, probabilities, 0, currPlayer))

        winner = game.get_winner()
        for game in gameData:
            data = list(game)
            if data[3] == winner:
                data[2] = 1
            else:
                data[2] = -1
            totalData.append((data[0], data[1], data[2]))
    return totalData


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
    if node.parent is not None:
        node.update_win_value(win_value)
