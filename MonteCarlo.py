import random
from copy import deepcopy
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo
from checkers.game import Game
import InputBuilder
import ResNetCheckers

class MCTS:
	def __init__(self , neural_network):
		self.neural_network = neural_network

	def child_finder(self, node):
		win_value, expert_policy_values = self.neural_network.predict(node.state)

		for move in node.state.get_possible_moves():
			child = Node(deepcopy(node.state))
			child.state.move(move)
			child.player_number = child.state.whose_turn()
			child.policy_value = get_child_policy_value(child, expert_policy_values) #should return a probability value between 0 and 1
			node.add_child(child)

		node.update_win_value(win_value)


