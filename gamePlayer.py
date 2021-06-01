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

        montecarlo = MonteCarlo(Node(game), model)
        gameData = []
        historicalBoards = InputBuilder.HistoricalBoards()
        montecarlo.child_finder = child_finder
        if doPrints:
            print("game " + str(i))
        montecarlo.root_node.player_number = game.whose_turn()

        while not (game.is_over()):
            # game state

            if doPrints:
                print("turn " + str(len(game.moves)))
            currPlayer = game.whose_turn()
            currInput = InputBuilder.build_board_planes(17, historicalBoards, game, currPlayer)
            montecarlo.simulate(2, currPlayer)  # lets start with 200 and work our way up #dont put a value less than 2 !

            probabilities_value = montecarlo.get_probabilities()
            probabilities = InputBuilder.convert_to_output(game.get_possible_moves(), probabilities_value)


            if len(game.moves) < 20:
                montecarlo.root_node = montecarlo.make_exploratory_choice()
            else:
                montecarlo.root_node = montecarlo.make_choice()
            if montecarlo.root_node.visits != 0:
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
    doPrints = True  # ChangHe to True to print information in console


    evaluationThreshold = 0.55  # new model must win 55% of games to be declared the winner
    victoryCounter = 0

    for i in range(num_games):
        game = Game()
        p1 = Agent(2, 1, False)  # change to True to play yourself!
        p2 = Agent(2, 2, False)
        if random.random() < 0.5:  # who goes first
            challengerIndex = 2
            montecarloP1 = MonteCarlo(Node(game), bestmodel)
            montecarloP2 = MonteCarlo(Node(game), challenger)
        else:
            challengerIndex = 1
            montecarloP1 = MonteCarlo(Node(game), challenger)
            montecarloP2 = MonteCarlo(Node(game), bestmodel)
         #   montecarlo = MonteCarlo(Node(game), bestmodel, challenger)
         #   challengerIndex = 2
        print(challengerIndex)


        montecarloP1.child_finder = child_finder
        montecarloP2.child_finder = child_finder
        montecarloP1.root_node.player_number = 1
        montecarloP2.root_node.player_number = 2
        while not (game.is_over()):
            #currInput = InputBuilder.build_board_planes(17, historicalBoards, game)

            if doPrints:
                if p1.botcategory == 0 and p2.botcategory == 0:
                    print("turn " + str(len(game.moves)))
                    print("possible: " + str(game.get_possible_moves()))
            if game.whose_turn() == 1:
                move = p1.make_move(montecarloP1, montecarloP2, game)
            else:
                move = p2.make_move(montecarloP2, montecarloP1, game)
            # if doPrints:
               # print(move)
            game.move(move)
        if game.get_winner() == challengerIndex:
            victoryCounter += 1
            print("chall dub")
        elif game.get_winner() == None:
            print("tie")
        else:
            print("loss")
    #if victoryCounter / num_games >= evaluationThreshold:  # did you win 55% of the games at least?
        #return True
    #else:
     #   return False
    return victoryCounter / num_games

def evaluateplayer(model, num_games, player1, player2):
    global game, historicalBoards, currInput
    doPrints = True  # ChangHe to True to print information in console


    evaluationThreshold = 0.55  # new model must win 55% of games to be declared the winner
    victoryCounter = 0
    visualizable = int(
        input("Do you want game to be visualizable 0(not_visualizable), 1(visualizable):\n"))
    cheer = int(input("Choose cheer player to cheer 0(human), 1(random), 2(alphazero):\n"))
    for i in range(num_games):
        game = Game()
        if (player1 == 0 and player2 == 1) or (player1 == 1 and player2 == 0):

            if random.random() < 0.5:  # who goes first
                p1 = Agent(0, 1,visualizable)  # change to True to play yourself!
                p2 = Agent(1, 2,visualizable)
                if cheer == 0:
                    challengerIndex = 1
                else:
                    challengerIndex = 2
                print("You are black!")
            else:
                p1 = Agent(1, 1,visualizable)  # change to True to play yourself!
                p2 = Agent(0, 2,visualizable)
                if cheer == 0:
                    challengerIndex = 2
                else:
                    challengerIndex = 1
                print("You are white!")
        elif (player1 == 0 and player2 == 2) or (player1 == 2 and player2 == 0):
            if random.random() < 0.5:  # who goes first
                p1 = Agent(0, 1,visualizable)  # change to True to play yourself!
                p2 = Agent(2, 2,visualizable)
                if cheer == 0:
                    challengerIndex = 1
                else:
                    challengerIndex = 2
                print("You are black!")
            else:
                p1 = Agent(2, 1,visualizable)  # change to True to play yourself!
                p2 = Agent(0, 2,visualizable)
                if cheer == 0:
                    challengerIndex = 2
                else:
                    challengerIndex = 1
                print("You are white!")
        elif (player1 == 1 and player2 == 2) or (player1 == 2 and player2 == 1):
            if random.random() < 0.5:  # who goes first
                p1 = Agent(1, 1,visualizable)  # change to True to play yourself!
                p2 = Agent(2, 2,visualizable)
                if cheer == 1:
                    challengerIndex = 1
                else:
                    challengerIndex = 2
            else:
                p1 = Agent(2, 1,visualizable)  # change to True to play yourself!
                p2 = Agent(1, 2,visualizable)
                if cheer == 1:
                    challengerIndex = 2
                else:
                    challengerIndex = 1
        #if random.random() < 0.5:  # who goes first
        #   p1 = Agent(0, 1)  # change to True to play yourself!
        #  p2 = Agent(2, 2)
        # challengerIndex = 2
        #print("You are black!")
        #else:
        #   p1 = Agent(2, 1)  # change to True to play yourself!
        #  p2 = Agent(0, 2)
        # challengerIndex = 1
        #print("You are white!")
        #   montecarlo = MonteCarlo(Node(game), bestmodel, challenger)
        #   challengerIndex = 2
        #else:
        montecarlo = MonteCarlo(Node(game), model)

        montecarlo.child_finder = child_finder
        montecarlo.root_node.player_number = game.whose_turn()
        while not (game.is_over()):
            #currInput = InputBuilder.build_board_planes(17, historicalBoards, game)

            if doPrints:
                if(p1.botcategory != 0 and p2.botcategory != 0):
                    print("turn " + str(len(game.moves)))
                    #print("possible: " + str(game.get_possible_moves()))
            if game.whose_turn() == 1:
                move = p1.make_move(montecarloActive = montecarlo, game = game, montecarloPassive = None)
            else:
                move = p2.make_move(montecarloActive = montecarlo, game = game, montecarloPassive = None)
            # if doPrints:
               # print(move)
            game.move(move)
        if game.get_winner() == challengerIndex:
            victoryCounter += 1
    #if victoryCounter / num_games >= evaluationThreshold:  # did you win 55% of the games at least?
        #return True
    #else:
     #   return False
    return victoryCounter / num_games


def child_finder(node, self, callingPlayer):

    '''
    currINPUT FOR CURRENT STATE OF THE GAME!
    '''

    if node.historical_boards is None:
        node.historical_boards = InputBuilder.HistoricalBoards()
    x = InputBuilder.build_board_planes(17, node.historical_boards, node.state, callingPlayer)
    x = x[np.newaxis, :, :]
    node.original_player = callingPlayer
    expert_policy_values, win_value = self.model.predict(x)
    for move in node.state.get_possible_moves():
        child = Node(deepcopy(node.state))
        child.state.move(move)
        child.historical_boards = deepcopy(node.historical_boards)
        child.player_number = child.state.whose_turn()
        child.policy_value = InputBuilder.get_child_policy_value(move, expert_policy_values)  # should return a probability value between 0 and 1
        node.add_child(child)
    if node.parent is not None:
        node.update_win_value(float(win_value), callingPlayer)
