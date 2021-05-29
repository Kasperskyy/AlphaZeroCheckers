import random
from copy import deepcopy

import numpy as np

# library imparaai montecarlo - https://pypi.org/project/imparaai-montecarlo/
from montecarlo.node import Node


class MonteCarlo:

    def __init__(self, root_node, model=None):
        self.model = model
        self.root_node = root_node
        self.child_finder = None
        self.node_evaluator = lambda child, montecarlo: None

    def make_choice(self):
        best_children = []
        most_visits = float('-inf')

        for child in self.root_node.children:
            if child.visits > most_visits:
                most_visits = child.visits
                best_children = [child]
            elif child.visits == most_visits:
                best_children.append(child)

        return random.choice(best_children)

    # function added by us
    def get_probabilities(self):
        children_visits = map(lambda child: child.visits, self.root_node.children)
        children_visit_probabilities = [visit / self.root_node.visits for visit in children_visits]
        return children_visit_probabilities

    def make_exploratory_choice(self):
        children_visits = map(lambda child: child.visits, self.root_node.children)
        children_visit_probabilities = [visit / self.root_node.visits for visit in children_visits]
        random_probability = random.uniform(0, 1)
        probabilities_already_counted = 0.

        for i, probability in enumerate(children_visit_probabilities):
            if probabilities_already_counted + probability >= random_probability:
                return self.root_node.children[i]

            probabilities_already_counted += probability

    def simulate(self, expansion_count=1, currentPlayer=None):
        for i in range(expansion_count):
            current_node = self.root_node

            while current_node.expanded:
                current_node = current_node.get_preferred_child(currentPlayer)

            self.expand(current_node, currentPlayer)

    def expand(self, node, currentPlayer):
        self.child_finder(node, self, currentPlayer)
        # rolloutccode commented out as we don't need it
        # for child in node.children:
        #    child_win_value = self.node_evaluator(child, self)
        #
        #    if child_win_value != None:
        #        child.update_win_value(child_win_value)
        #
        #    if not child.is_scorable():
        #        self.random_rollout(child)
        #        child.children = []

        if len(node.children):
            node.expanded = True

    def random_rollout(self, node):
        self.child_finder(node, self)
        child = random.choice(node.children)
        node.children = []
        node.add_child(child)
        child_win_value = self.node_evaluator(child, self)
        if child_win_value != None:
            node.update_win_value(child_win_value)
        else:
            self.random_rollout(child)

    '''
               picks a random move from the avaiable moves
               checks if this node is alReady in the mcts tree
               if it is, set it as the root node, subtract 1 from visits
               if it isn't, add it with zero visits and set as root node
               '''

    def non_user_expand(self, currentPlayer, move):
        found = False
        for x in self.root_node.children:
            if x.state.moves[-1] == move:
                self.root_node = x
                if self.root_node.visits != 0:
                    self.root_node.visits -= 1
                found = True
                break
        if not found:
            child = Node(deepcopy(self.root_node.state))
            child.state.move(move)
            child.historical_boards = deepcopy(self.root_node.historical_boards)
            child.player_number = child.state.whose_turn()
            self.root_node.add_child(child)
            self.root_node = child
