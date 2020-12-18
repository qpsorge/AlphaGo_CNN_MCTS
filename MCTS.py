import numpy as np
from collections import defaultdict

from abc import ABC, abstractmethod


class TwoPlayersAbstractGameState(ABC):

    def game_result(self):
        """
        this property should return:
         1 if player #1 wins
        -1 if player #2 wins
         0 if there is a draw
         None if result is unknown
        Returns
        -------
        int
        """
        pass

    def is_game_over(self):
        """
        boolean indicating if the game is over,
        simplest implementation may just be
        `return self.game_result() is not None`
        Returns
        -------
        boolean
        """
        pass

    def move(self, action):
        """
        consumes action and returns resulting TwoPlayersAbstractGameState
        Parameters
        ----------
        action: AbstractGameAction
        Returns
        -------
        TwoPlayersAbstractGameState
        """
        pass

    def get_legal_actions(self):
        """
        returns list of legal action at current game state
        Returns
        -------
        list of AbstractGameAction
        """
        pass



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