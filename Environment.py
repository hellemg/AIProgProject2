from Game import Nim, Ledge
from GlobalConstants import *


class Environment:
    def __init__(self, game_type: str):
        # Game type: nim or ledge
        self.game = self.set_game(game_type)

    def set_game(self, game_type):
        """
        :param init: K for nim
        """
        if game_type == 'nim':
            return Nim(K)
        elif game_type == 'ledge':
            return Ledge()
        else:
            raise ValueError('{} not valid game_type'.format(game_type))

    def generate_child_state_from_action(self, state, action, p_num=0, verbose=False):
        """
        :param state: board, either ndarray (ledge) or int (nim)
        :param action: tuple with action to do
        """
        player = p_num % 2+1
        return self.game.get_state_from_state_action(state, *action, player, verbose)

    def check_game_done(self, state):
        """
        :param state: board, either ndarray (ledge) or int (nim)

        :returns: boolean, True if the game is done
        """
        return self.game.check_game_done(state)

    def get_possible_actions_from_state(self, state):
        """
        :param state: board, either ndarray (ledge) or int (nim)

        :returns: list of possible actions
        """
        return self.game.get_possible_actions_from_state(state)

    def get_environment_value(self, player_num):
        """
        :param player_num: int, 1 for P1 and 2 for P2

        :returns: 1 if P1 won, -1 if P2 won
        """
        if player_num == 1:
            return 1
        elif player_num == 2:
            return -1
