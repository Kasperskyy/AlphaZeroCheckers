import pickle
import random
import numpy as np
from copy import deepcopy
from agent import Agent
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo
from checkers.game import Game
import InputBuilder





def selfplay(numbgame, model):
    doPrints = False  # set to True to see console
    totalData = []
    for i in range(numbgame):
        game = Game()
        montecarlo = MonteCarlo(Node(game), model)
        gameData = []
        montecarlo.child_finder = child_finder
        #if doPrints:
        print("game " + str(i))
        montecarlo.root_node.player_number = game.whose_turn()

        while not (game.is_over()):
            # game state

            if doPrints:
                print("turn " + str(len(game.moves)))

            currPlayer = game.whose_turn()
            currInput = InputBuilder.build_board_planes(5, game, currPlayer)
            montecarlo.simulate(50, currPlayer)  # number of simulations per turn. do not put less than 2
            probabilities_value = montecarlo.get_probabilities(currPlayer)
            probabilities = InputBuilder.convert_to_output(game.get_possible_moves(), probabilities_value)


            montecarlo.root_node = montecarlo.make_exploratory_choice(currPlayer)
            #else:
            #    montecarlo.root_node = montecarlo.make_choice(currPlayer) #rest of moves are the network playing "optimally"

            if montecarlo.root_node.visits[montecarlo.root_node.original_player - 1] != 0:
                montecarlo.root_node.visits[montecarlo.root_node.original_player - 1] -= 1

            game.move(montecarlo.root_node.state.moves[-1])
            gameData.append((currInput, probabilities, 0, currPlayer))
            if len(game.moves) >= 120:    # game too long, auto-draw
                break
        winner = game.get_winner()
        for game in gameData:
            data = list(game)
            if data[3] == winner:
                data[2] = 1
            elif winner is not None:
                data[2] = -1
            else:
                data[2] = 0 #already equal to zero but done for clarity
            totalData.append((data[0], data[1], data[2]))
        with open("TrainingData.txt", "wb") as fp:
            pickle.dump(totalData, fp)
    return totalData

def evaluate(bestmodel, challenger, num_games):
    global game
    victoryCounter = 0
    doPrints = True
    for i in range(num_games):
        game = Game()
        p1 = Agent(2, 1, False)
        p2 = Agent(2, 2, False)
        if random.random() < 0.5:  # who goes first
            challengerIndex = 2
            montecarloP1 = MonteCarlo(Node(game), bestmodel)
            montecarloP2 = MonteCarlo(Node(game), challenger)
        else:
            challengerIndex = 1
            montecarloP1 = MonteCarlo(Node(game), challenger)
            montecarloP2 = MonteCarlo(Node(game), bestmodel)
        montecarloP1.child_finder = child_finder
        montecarloP2.child_finder = child_finder
        montecarloP1.root_node.player_number = 1
        montecarloP2.root_node.player_number = 2
        while not (game.is_over()):
            if game.whose_turn() == 1:
                move = p1.make_move(montecarloP1, montecarloP2, game)
            else:
                move = p2.make_move(montecarloP2, montecarloP1, game)
            game.move(move)
        if doPrints:
            if game.get_winner() == challengerIndex:
                victoryCounter += 1
                print("challenger has won")
            elif game.get_winner() is None:
                print("tie")
            else:
                print("challenger has lost")
    return victoryCounter / num_games

def evaluateplayer(model, num_games, player1, player2):
    global game
    doPrints = False

    victoryCounter = 0
    drawCounter = 0
    visualizable = int(
        input("Do you want game to be visualizable 0(not_visualizable), 1(visualizable):\n"))
    cheer = int(input("Choose player to cheer[their wins count as your wins] 0(human), 1(random), 2(alphazero):\n"))
    if visualizable == 1:
        orient = int(input("Choose player at the bottom of the screen black(0), white(1): \n"))
    order = int(input("Choose who plays black[black is always first] random(0), first player(1), second player(2) "))
    for i in range(num_games):
        game = Game()
        if (order == 0 and random.random() < 0.5) or order == 1:
            p1 = Agent(player1, 1, visualizable, orient)
            p2 = Agent(player2, 1, visualizable, orient)
        else:
            p1 = Agent(player2, 1, visualizable, orient)
            p2 = Agent(player1, 1, visualizable, orient)
        challengerIndex = cheer + 1
        if cheer == 0:
            print("Cheering black!")
        else:
            print("Cheering white!")

        montecarlo = MonteCarlo(Node(game), model)
        montecarlo.child_finder = child_finder
        montecarlo.root_node.player_number = game.whose_turn()
        print("Game number " + str(i))
        while not (game.is_over()):
            if doPrints:
                if(p1.botcategory != 0 and p2.botcategory != 0):
                    print("turn " + str(len(game.moves)))
            if game.whose_turn() == 1:
                move = p1.make_move(montecarloActive = montecarlo, game = game, montecarloPassive = None)
            else:
                move = p2.make_move(montecarloActive = montecarlo, game = game, montecarloPassive = None)
            game.move(move)
        if game.get_winner() == challengerIndex:
            victoryCounter += 1
        if game.get_winner() is None:
            drawCounter += 1

    return victoryCounter, drawCounter

def child_finder(node, self, callingPlayer):

    x = InputBuilder.build_board_planes(5, node.state, callingPlayer)
    x = x[np.newaxis, :, :]
    node.original_player = callingPlayer
    expert_policy_values, win_value = self.model.predict(x)
    for move in node.state.get_possible_moves():
        child = Node(deepcopy(node.state))
        child.state.move(move)
        child.player_number = child.state.whose_turn()
        child.policy_value = InputBuilder.get_child_policy_value(move, expert_policy_values)
        node.add_child(child)
    if node.parent is not None:
        if node.original_player != node.player_number:
            win_value *= -1
        node.update_win_value(float(win_value), callingPlayer)
