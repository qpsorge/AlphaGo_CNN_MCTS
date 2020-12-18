import numpy as np
from collections import defaultdict
from abc import ABC, abstractmethod


class MonteCarloTreeSearchNode(ABC):

    def __init__(self, state, parent=None):
        """
        Parameters
        ----------
        state : mctspy.games.common.TwoPlayersAbstractGameState
        parent : MonteCarloTreeSearchNode
        """
        self.state = state
        self.parent = parent
        self.children = []

    @property
    @abstractmethod
    def untried_actions(self):
        """
        Returns
        -------
        list of mctspy.games.common.AbstractGameAction
        """
        pass

    @property
    @abstractmethod
    def q(self):
        pass

    @property
    @abstractmethod
    def n(self):
        pass

    @abstractmethod
    def expand(self):
        pass

    @abstractmethod
    def is_terminal_node(self):
        pass

    @abstractmethod
    def rollout(self):
        pass

    @abstractmethod
    def backpropagate(self, reward):
        pass

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):        
        return possible_moves[np.random.randint(len(possible_moves))]

class TwoPlayersGameMonteCarloTreeSearchNode(MonteCarloTreeSearchNode):

    def __init__(self, state, parent=None):
        super().__init__(state, parent)
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self._untried_actions = None

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        wins = self._results[self.parent.state.next_to_move]
        loses = self._results[-1 * self.parent.state.next_to_move]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.move(action)
        child_node = TwoPlayersGameMonteCarloTreeSearchNode(
            next_state, parent=self
        )
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)







class MCTSNode:
    def __init__(self, board, score=0, parent=None):
        self.board          = board

        self.parent = parent
        self.children = []
        self.is_leaf  = False

        self.visits         = 0
        self.prior          = score
        self.total_value    = 0
        self.value          = 0

        
    # Au début, self.value=0, exploration basée sur l'incertitude
    def get_incertitude(self):
        return self.prior/(1+self.visits)
    
    def is_leaf(self):
        return self.is_leaf

    def best_child(self):
        #c_param = 1.4
        choices_weights = [
            # Methode of choosing best children
            # c.q + c_param * np.sqrt((2 * np.log(c.visits) / (1+c.visits)))
            # q+c*p*sqrt(N)/(1+visits)
            c.value+c.get_incertitude()
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def possible_moves(self, move):
        return self.board.legal_moves()

    def expand_child(self, move):
        """
        Create child node, with board, is_leaf, parent
        NEED TO CHANGE PRIOR TO CNN PREDICTION
        """
        is_leaf, child_board = self.simulate_move(move)
        child       = MCTSNode(child_board,0,parent=self) #CNN.predict(simulated_board) instead of 0
        child.is_leaf = is_leaf
        self.children.append(child)
        return child
    
    def simulate_move(self,move):
        '''
        returns tuple (is_leaf_node, child_board)
        '''
        # On a un plateau en entrée, maj de toutes les données
        simulated_board = self.board.copy()
        color = simulated_board._nextPlayer
        if move != -1: #On passe le -1, la gestion du game over se fera après
            # On ajoute dans la bonne couleur du board
            simulated_board._put_stone(move,color)
            simulated_board._lastPlayerHasPassed = False
            if color == simulated_board._WHITE:
                simulated_board._nbWHITE += 1
                simulated_board._nextPlayer = simulated_board._BLACK
            else:
                simulated_board._nbBLACK += 1
                simulated_board._nextPlayer = simulated_board._WHITE
            return (False,simulated_board)
        else: #On a le cas d'un pass
            simulated_board._gameOver = True
            return (True,simulated_board)



class MCTSTree:
    def __init__(self, node:MCTSNode):
        self.nodeList   = [node]
        self.node       = node

    def select(self, node=None):
        print("select")
        if(self.node.is_leaf()):
            return self.node
        else:
            self.expand() # children created & initialized with prior & rollout
            best_child = self.node.best_child() # select the best
            self.node=best_child
            return self.select(best_child)

    def expand(self):
        # TO DO : self.node.possible_moves(), node.expand(move)
        print("expand")
        for move in self.node.board.legal_moves():
            # Add child
            child = self.node.expand_child(move)
            self.nodeList.append(child)
            # Calculate prior
            child.prior = 0 #CNN.predict(child.board)

        # ADD ROLLOUT
        #
        #
        value = Rollout(self.node)

    def backup(self):
        pass

    def play(self):
        return self.select(self.node.best_child())

self.expand() # children created & initialized with prior & rollout
            best_child = self.node.best_child() # select the best
            self.node=best_child
            return self.select(best_child)


print(f"\nCréation de la board :\n")
from Goban import Board
board = Board()

print(np.array(board.generate_legal_moves()).shape) #81 move possible + pass

print(f"Création du noeud :\n")
base_node = MCTSNode(board, 0)#prior to CNN.predict(board)) instead of 0

print(f"Création du MCTS Tree :\n")
mcts_tree= MCTSTree(base_node)
# First step : expand base node
mcts_tree.expand()
mcts_tree.select()

    
        
        
        