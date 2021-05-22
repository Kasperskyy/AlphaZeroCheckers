import random

import numpy as np
from copy import deepcopy

from agent import Agent
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo
from checkers.game import Game
import InputBuilder

##### PETLA GIER
historicalBoards = None
game = None
currInput = None


def selfplay(numbgame, model):
    global game, historicalBoards, currInput

    doPrints = False  # set to True to see console

    totalData = []
    for i in range(numbgame):
        game = Game()

        montecarlo = MonteCarlo(Node(game), model, model)
        gameData = []
        historicalBoards = InputBuilder.HistoricalBoards()
        montecarlo.child_finder = child_finder
        if doPrints:
            print("game " + str(i))
        montecarlo.root_node.player_number = game.whose_turn()

        while not (game.is_over()):
            # game state
            currInput = InputBuilder.build_board_planes(17, historicalBoards, game)
            if doPrints:
                print("turn " + str(len(game.moves)))
            montecarlo.simulate(40)  # lets start with 200 and work our way up #dont put a value less than 2 !

            probabilities_value = montecarlo.get_probabilities()
            probabilities = InputBuilder.convert_to_output(game.get_possible_moves(), probabilities_value)
            currPlayer = game.whose_turn()

            if len(game.moves) < 20:
                montecarlo.root_node = montecarlo.make_exploratory_choice()
            else:
                montecarlo.root_node = montecarlo.make_choice()
            montecarlo.root_node.visits -= 1

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


def evaluate(bestmodel, challenger, num_games):
    global game, historicalBoards, currInput
    doPrints = False  # ChangHe to True to print information in console


    evaluationThreshold = 0.55  # new model must win 55% of games to be declared the winner
    victoryCounter = 0

    for i in range(num_games):
        game = Game()
        historicalBoards = InputBuilder.HistoricalBoards()
        if random.random() < 0.5:  # who goes first
            p1 = Agent(True)  # change to True to play yourself!
            p2 = Agent(False)
            challengerIndex = 2
        else:
            p1 = Agent(False)  # change to True to play yourself!
            p2 = Agent(True)
            challengerIndex = 1
         #   montecarlo = MonteCarlo(Node(game), bestmodel, challenger)
         #   challengerIndex = 2
        #else:
        montecarlo = MonteCarlo(Node(game), challenger, bestmodel)

        montecarlo.child_finder = child_finder
        montecarlo.root_node.player_number = game.whose_turn()
        while not (game.is_over()):
            currInput = InputBuilder.build_board_planes(17, historicalBoards, game)
            if doPrints:
                print("turn " + str(len(game.moves)))
                print("possible: " + str(game.get_possible_moves()))
            if game.whose_turn() == 1:
                move = p1.make_move(montecarlo)
            else:
                move = p2.make_move(montecarlo)
            if doPrints:
                print(move)
            game.move(move)
        if game.get_winner() == challengerIndex:
            victoryCounter += 1
    #if victoryCounter / num_games >= evaluationThreshold:  # did you win 55% of the games at least?
        #return True
    #else:
     #   return False
    return victoryCounter / num_games


def child_finder(node, self):
    global currInput,game
    '''
    currINPUT FOR CURRENT STATE OF THE GAME!
    '''
    x = currInput

    x = x[np.newaxis, :, :]
    expert_policy_values, win_value = self.model[game.whose_turn() - 1].predict(x)
    for move in node.state.get_possible_moves():
        child = Node(deepcopy(node.state))
        child.state.move(move)
        child.player_number = child.state.whose_turn()
        child.policy_value = InputBuilder.get_child_policy_value(move, expert_policy_values)  # should return a probability value between 0 and 1
        node.add_child(child)
    if node.parent is not None:
        node.update_win_value(win_value)
