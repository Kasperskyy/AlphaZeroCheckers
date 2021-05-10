import numpy as np
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo
from checkers.game import Game
from tensorflow.keras.models import Model
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Lambda
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
import tensorflow as tf
from tensorflow.python.keras.layers import ReLU, Add
from tensorflow.python.keras.utils.vis_utils import plot_model
from enum import Enum
import random

game = Game()

board_size_x = game.board.width  # 4
board_size_y = game.board.height  # 8


class Player_id(Enum):
    BLACK_PLAYER = 1
    WHITE_PLAYER = 2


player_name = {
    1: "black",
    2: "white"
}


def getCoords(position, gameWidth, gameHeight, orientation):
    if position % gameWidth == 0:
        x = gameWidth - 1
    else:
        x = (position % gameWidth) - 1
    y = (position - 1) // gameWidth
    if orientation == "black":
        x = gameWidth - 1 - x
        y = gameHeight - 1 - y
    return x, y



turns = {
    0: {
        Player_id.BLACK_PLAYER.value: 0,
        Player_id.WHITE_PLAYER.value: 8
    },
    1: {
        Player_id.BLACK_PLAYER.value: 1,
        Player_id.WHITE_PLAYER.value: 9
    },
    2: {
        Player_id.BLACK_PLAYER.value: 2,
        Player_id.WHITE_PLAYER.value: 10
    },
    3: {
        Player_id.BLACK_PLAYER.value: 3,
        Player_id.WHITE_PLAYER.value: 11
    },
    4: {
        Player_id.BLACK_PLAYER.value: 4,
        Player_id.WHITE_PLAYER.value: 12
    },
    5: {
        Player_id.BLACK_PLAYER.value: 5,
        Player_id.WHITE_PLAYER.value: 13
    },
    6: {
        Player_id.BLACK_PLAYER.value: 6,
        Player_id.WHITE_PLAYER.value: 14
    },
    7: {
        Player_id.BLACK_PLAYER.value: 7,
        Player_id.WHITE_PLAYER.value: 15
    }
}


class HistoricalBoards:

    def __init__(self):
        x = game.board.width
        y = game.board.height
        #TO DO - zmienic "8" oraz "8-1"
        self.historic_turns = np.zeros((x,y,2,7), dtype=np.int)
        #[[[[0 for i in range(x)] for j in range(y)] for k in range(2)] for l in range(7)]  # [turn, player, y, x]
        # [x][y][2][7] - koordy, ktory gracz, zapisac 7 ruchow wstecz

    def add_turn(self, black_plane, white_plane):
        self.historic_turns = np.delete(self.historic_turns,7-1, 3)
        #TO DO -
        turn3d = np.array([black_plane, white_plane])
        self.historic_turns = np.insert(self.historic_turns, 0, turn3d, 3)
        print("gay")
        #self.historic_turns.insert(0, turn3d)

    def get_turn(self, turn_count):
        #TO DO - add parameter orientation
        black_plane = self.historic_turns[turn_count, 0]
        white_plane = self.historic_turns[turn_count, 1]
        return black_plane, white_plane


historical_boards = HistoricalBoards()


def build_board_planes(plane_count):
    board_planes = np.zeros((board_size_x, board_size_y, plane_count), dtype=np.int)

    for player in game.board.searcher.player_positions:
        player_positions = game.board.searcher.player_positions[player]
        for position in player_positions:
            x, y = getCoords(position, board_size_x, board_size_y, player_name[player])
            board_planes[x][y][turns[0][player]] = 1
    historical_boards.add_turn(board_planes[:,:,turns[0][1]], board_planes[:, :, turns[0][2]])

    for i in range(1,7):
        black_plane, white_plane = historical_boards.get_turn(i)
        board_planes[:,:,turns[i][1]] = black_plane
        board_planes[:, :, turns[i][2]] = white_plane

    if game.board.player_turn == Player_id.BLACK_PLAYER:
        board_planes[:,:,(plane_count - 1)] = np.ones((board_size_x, board_size_y), dtype=int)

    return board_planes



while not (game.is_over()):
    build_board_planes(17)
    possible_moves = game.get_possible_moves()
    rand_v = random.choice(possible_moves)
    game.move(rand_v)


if game.get_winner() is None:
    print("There is no winner")
else:
    print("And the winner iiiis player: ", game.get_winner())
