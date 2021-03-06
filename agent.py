import random
import numpy as np
from sty import fg
import InputBuilder


def BoardVisualization(game, orientation):
            print(
                "==============================================================================================================")
            matrix = np.zeros((8, 8), dtype=int)
            matrix_is_king = np.zeros((8, 8), dtype=bool)
            template_matrix = np.array([[29, 0, 30, 0, 31, 0, 32, 0],
                                        [0, 25, 0, 26, 0, 27, 0, 28],
                                        [21, 0, 22, 0, 23, 0, 24, 0],
                                        [0, 17, 0, 18, 0, 19, 0, 20],
                                        [13, 0, 14, 0, 15, 0, 16, 0],
                                        [0, 9, 0, 10, 0, 11, 0, 12],
                                        [5, 0, 6, 0, 7, 0, 8, 0],
                                        [0, 1, 0, 2, 0, 3, 0, 4]], dtype=int)

            if orientation == 0:
                orientation_str = "black"
            else:
                template_matrix = np.rot90(template_matrix, 2)
                orientation_str = "white"
            template_matrix = ([list(sublist[::-1]) for sublist in template_matrix])

            list_positions = list(game.board.searcher.position_pieces.values())
            for i in list_positions:
                is_king = i.king
                player_number = i.player
                curr_position = i.position
                if curr_position < 5 or (13 > curr_position > 8) or (21 > curr_position > 16) or (29 > curr_position > 24):
                    curr_position = curr_position * 2
                else:
                    curr_position = curr_position * 2 - 1
                x, y = InputBuilder.getCoords(position=curr_position, gameWidth=8, gameHeight=8, orientation= orientation_str)
                matrix[x][y] = player_number
                matrix_is_king[x][y] = is_king


            display_matrix = np.rot90(matrix, 3)
            display_matrix = ([list(sublist[::-1]) for sublist in display_matrix])
            matrix_is_king = np.rot90(matrix_is_king, 3)
            matrix_is_king = ([list(sublist[::-1]) for sublist in matrix_is_king])



            for i in range(8):
                row_str = ""
                template_str = ""
                for j in range(8):
                    ## Template matrix
                    templ_str = str(template_matrix[i][j])
                    if 10 > int(templ_str) > 0:
                        templ_str = ' ' + templ_str + ' ';
                    elif templ_str == '0':
                        templ_str = " _ "
                    else:
                        templ_str = ' ' + templ_str
                  
                    add_str = str(display_matrix[i][j])  # 1 2 0
                    if add_str == '0':
                        add_str = "\033[0m" + " _ "
                    if add_str == '1':
                        if matrix_is_king[i][j]:
                            add_str = fg.black + ' K '
                        else:
                            add_str = fg.black + ' ??? '
                    if add_str == '2':
                        if matrix_is_king[i][j]:
                            add_str = fg.white + ' K '
                        else:
                            add_str = fg.white + ' ??? '

                    row_str = row_str + add_str + "\033[0m" + "|"
                    template_str = template_str + templ_str + "\033[0m" + "|"
                print(row_str + "       " + "|" + template_str)




class Agent:
    def __init__(self, botcategory,number,visualizable, orientation):
        self.botcategory = botcategory
        self.number = number
        self.visualizable = visualizable
        self.orienation = orientation

    def make_move(self, montecarloActive=None, montecarloPassive=None, game=None):
        if self.visualizable:
            BoardVisualization(game, self.orienation)
        if self.botcategory == 0:
            print("turn " + str(len(game.moves)))
            if game.whose_turn() == 1:
                print("BLACK move!!")
            else:
                print("WHITE move!!")
            while(True):
                print("possible: " + str(game.get_possible_moves()))
                move = input("Give move!!!!!!\n")
                move = move.split()
                try:
                    move[0]=int(move[0])
                    move[1] = int(move[1])
                    if (move in game.get_possible_moves()):
                        break;
                except ValueError:
                    print("Not an int!")
                print(
                    "==============================================================================================================")

            montecarloActive.non_user_expand(move, self.number)
            return move
        elif self.botcategory == 1:
            possible_moves = []
            for x in montecarloActive.root_node.state.get_possible_moves():
                possible_moves.append(x)
            move = random.choice(possible_moves)
            montecarloActive.non_user_expand(move, self.number)
            return move
        else:
            montecarloActive.simulate(100, self.number)
            montecarloActive.root_node = montecarloActive.make_choice(self.number)
            if montecarloActive.root_node.visits[(montecarloActive.root_node.original_player) - 1] != 0:
                montecarloActive.root_node.visits[(montecarloActive.root_node.original_player) - 1] -= 1
            if montecarloPassive is not None:
                montecarloPassive.non_user_expand(montecarloActive.root_node.state.moves[-1], self.number)
            return montecarloActive.root_node.state.moves[-1]
