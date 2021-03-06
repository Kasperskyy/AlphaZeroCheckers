import random
from copy import deepcopy
from montecarlo.node import Node


class MonteCarlo:

    def __init__(self, root_node, model=None):
        self.root_node = root_node
        self.child_finder = None
        self.node_evaluator = lambda child, montecarlo: None

        ###Below Code is created by us
        self.model = model
        ###

    def make_choice(self, callingPlayer):
        self.root_node.active = False
        best_children = []
        most_visits = float('-inf')

        for child in self.root_node.children:
            if child.visits[callingPlayer-1] > most_visits:
                most_visits = child.visits[callingPlayer-1]
                best_children = [child]
            elif child.visits[callingPlayer-1] == most_visits:
                best_children.append(child)
        theChoice = random.choice(best_children)
        theChoice.parent = None
        return theChoice

    ###Below Function is created entirely by us
    def get_probabilities(self, callingPlayer):
        children_visits = map(lambda child: child.visits[callingPlayer-1], self.root_node.children)
        children_visit_probabilities = [visit / self.root_node.visits[callingPlayer-1] for visit in children_visits]
        return children_visit_probabilities
    ###

    def make_exploratory_choice(self, callingPlayer):
        self.root_node.active = False
        children_visits = map(lambda child: child.visits[callingPlayer-1], self.root_node.children)
        children_visit_probabilities = [visit / self.root_node.visits[callingPlayer-1] for visit in children_visits]
        random_probability = random.uniform(0, 1)
        probabilities_already_counted = 0.

        for i, probability in enumerate(children_visit_probabilities):
            if probabilities_already_counted + probability >= random_probability:
                self.root_node.children[i].parent = None
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
        if len(node.children):
            node.expanded = True

    ### Below Function is created entirely by us
    def non_user_expand(self, move, callingPlayer):
        found = False
        for x in self.root_node.children:
            if x.state.moves[-1] == move:
                self.root_node = x
                if self.root_node.original_player is not None:
                    if self.root_node.visits[(self.root_node.original_player)-1] != 0:
                        self.root_node.visits[(self.root_node.original_player)-1] -= 1
                found = True
                break
        if not found:
            child = Node(deepcopy(self.root_node.state))
            child.state.move(move)
            child.player_number = child.state.whose_turn()
            self.root_node.add_child(child)
            self.root_node = child
    ###
