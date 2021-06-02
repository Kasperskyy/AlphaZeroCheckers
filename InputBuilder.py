from enum import Enum
import numpy as np


class Player_id(Enum):
    BLACK_PLAYER = 1
    WHITE_PLAYER = 2


# Dictionaries
policyIndex = {
    0: {
        5: 0,
        4: 1,
        -3: 2,
        -4: 3,
        9: 4,
        7: 5,
        -7: 6,
        -9: 7},
    1: {
        4: 0,
        3: 1,
        -4: 2,
        -5: 3,
        9: 4,
        7: 5,
        -7: 6,
        -9: 7}
}
player_name = {
    1: "black",
    2: "white"
}
player_number = {
    "black": 0,
    "white": 1
}
turns = {
    0: {
        Player_id.BLACK_PLAYER.value: 0,
        Player_id.WHITE_PLAYER.value: 2
    },
    1: {
        Player_id.BLACK_PLAYER.value: 1,
        Player_id.WHITE_PLAYER.value: 3
    }
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





def build_board_planes(plane_count, game, currPlayer):
    board_size_x = game.board.width
    board_size_y = game.board.height
    board_planes = np.zeros((board_size_x, board_size_y, plane_count), dtype=np.int)
    current_player = currPlayer


    for piece in game.board.pieces:
        if piece.captured is False:
            x, y = getCoords(piece.position, board_size_x, board_size_y, player_name[current_player])
            if piece.king is False:
                board_planes[x][y][turns[0][piece.player]] = 1
            else:
                board_planes[x][y][turns[1][piece.player]] = 1
              # put 1 on the player's position (in his orientation)

    if game.board.player_turn == Player_id.BLACK_PLAYER.value:
        board_planes[:, :, (plane_count - 1)] = np.ones((board_size_x, board_size_y), dtype=int)

    return board_planes


def get_child_policy_value(child, policy):
    policy = policy[0]
    rowType = 8 * np.math.floor(((child[0] - 1) / 8)+0.5)
    if rowType < child[0]:
        distance = 0
    else:
        distance = 1
    destination = policyIndex[distance][child[1] - child[0]]
    index = (len(policy) / 32) * (child[0] - 1) + destination
    return policy[int(index)]
#each 8 is one piece. each board has 8 values, from 0 to 7; 0- move north east, 1 - move north west, 2- move south east, 3- move south west, 4- jump north east, 5- jump north west, 6- jump south east, 7- jump south west


def convert_to_output(children, probabilities_value):
    probabilities = np.zeros(256)
    counter = 0
    for i in children:
        rowType = 8 * np.math.floor(((i[0] - 1) / 8)+0.5)
        if rowType < i[0]:
            distance = 0
        else:
            distance = 1
        destination = policyIndex[distance][i[1] - i[0]]
        index = (len(probabilities) / 32) * (i[0] - 1) + destination
        probabilities[int(index)] = probabilities_value[counter]
        counter += 1
    return probabilities
