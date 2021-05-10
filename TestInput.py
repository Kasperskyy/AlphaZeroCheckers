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

# TO DO - TIDY and ujednolicic wszystkie slowniki i enumeracje
class Player_id(Enum):
    BLACK_PLAYER = 1
    WHITE_PLAYER = 2


player_name = {
    1: "black",
    2: "white"
}

player_number = {
    "black": 0,
    "white": 1
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
        self.historic_turns = np.zeros((x,y,2,2,7), dtype=np.int)        # 4x8x2x2x7
        # [x][y][2][black plane, white plane][7] - koordynacje, pozycje ktorego gracza, orientacja ktorego gracza, ile kolejek temu (o - aktualna, 1- 1 kolejka do tylu itp)


    def add_turn(self, black_plane, white_plane, current_player):
        self.historic_turns = np.delete(self.historic_turns, 7-1, 4)
        turn3d1 = np.array([black_plane, white_plane])
        turn3d2 = np.array([np.rot90(black_plane, 2), np.rot90(white_plane, 2)])

        if current_player == 1:     # black player
            turn4d = np.array([turn3d1, turn3d2])
        else:
            turn4d = np.array([turn3d2, turn3d1])

        turn4d = np.moveaxis(turn4d, 1, -1)      # changing 2x2x4x8 to 4x8x2x2 shape
        turn4d = np.moveaxis(turn4d, 0, -1)

        self.historic_turns = np.insert(self.historic_turns, 0, turn4d, 4)

    def get_turn(self, turn_count, current_player):
        black_plane = self.historic_turns[:,:, player_number['black'], current_player-1, turn_count]
        white_plane = self.historic_turns[:,:,player_number['white'], current_player-1, turn_count]
        return black_plane, white_plane


historical_boards = HistoricalBoards()


def build_board_planes(plane_count):
    board_planes = np.zeros((board_size_x, board_size_y, plane_count), dtype=np.int)

    current_player = game.whose_turn()
    for player in game.board.searcher.player_positions:
        player_positions = game.board.searcher.player_positions[player]
        for position in player_positions:
            x, y = getCoords(position, board_size_x, board_size_y, player_name[current_player])
            board_planes[x][y][turns[0][player]] = 1          # wstawianie 1 na pozycje gracza (w jego orientacji)

    historical_boards.add_turn(board_planes[:,:,turns[0][1]], board_planes[:, :, turns[0][2]], current_player)

    for i in range(1,7):
        black_plane, white_plane = historical_boards.get_turn(i, current_player)
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
