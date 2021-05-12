from copy import deepcopy
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo
from checkers.game import Game
import InputBuilder
import numpy as np

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
        # gameData[]
        historicalBoards = InputBuilder.HistoricalBoards()
        montecarlo.child_finder = child_finder
        print("game " + str(i))
        montecarlo.root_node.player_number = game.state.whose_turn()
        while not (game.is_over()):
            currInput = InputBuilder.build_board_planes(17, historicalBoards, game)
            # moveData[]= consists of 3 elements- the game state, the search probabilties, the winner(added after game is over)
            print("turn " + str(len(game.moves)))
            montecarlo.simulate(1)
            if (len(game.moves) < 20):
                montecarlo.root_node = montecarlo.make_exploratory_choice()
            else:
                montecarlo.root_node = montecarlo.make_choice()
            game.move(montecarlo.root_node.state.moves[-1])
            # add boardstate
            # add probabilities
            # gameData.app [nalesnikPauliny,probabilities, gamevalue(-1/0/1) , ]
        game.get_winner()
        # petla zeby dodac odpowiednie game value


def child_finder(node, self):
    x = currInput
    x = x[np.newaxis, :, :]
    expert_policy_values, win_value = Model.predict(x)
    for move in node.state.get_possible_moves():
        child = Node(deepcopy(node.state))
        child.state.move(move)
        child.player_number = child.state.whose_turn()
        child.policy_value = InputBuilder.get_child_policy_value(move, expert_policy_values) #should return a probability value between 0 and 1
        node.add_child(child)
    node.update_win_value(win_value)



# array of moves.app(gameData)
#  [array of moves [nalesnikPauliny, gamevalue(-1/0/1) , probabilities]  ]


#  board_size_x = game.board.width  # 4
# board_size_y = game.board.height  # 8

# historicalBoards = InputBuilder.HistoricalBoards()
#  theModel = ResNetCheckers.build()


# while not (game.is_over()):
# x = InputBuilder.build_board_planes(17, historicalBoards, game)
# possible_moves = game.get_possible_moves()
# rand_v = random.choice(possible_moves)
# game.move(rand_v)
# x = x[np.newaxis, :, :]
# policy, value = theModel.predict(x)
# print("CICHAJ")
