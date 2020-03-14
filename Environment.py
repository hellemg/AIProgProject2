from Game import Nim, Ledge
from GlobalConstants import *

class Environment:
    def __init__(self, game_type: str):
        # Game type: nim or ledge
        self.game_type = game_type

        # TODO: method to generate new state from state and action
        # - state should be ndarray, so state = board and a new state can be generated from an action

    def generate_child_state_from_action(self, state, action):
        """
        :param state: board, either ndarray (ledge) or int (nim)
        :param action: tuple with action to do
        """
        return self.game.get_state_from_state_action(state, *action)

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

    def get_init(self, state):
        # Returns init for 
        if self.game_type == 'nim':
            # Return N and K
            return (int(state), K)
        elif self.game_type == 'ledge':
            # Return numpy array from state
            return np.array([int(c) for c in state])
        else:
            raise ValueError('{} not valid game_type'.format(game_type))

    def set_game(self, init: tuple):
        if self.game_type == 'nim':
            self.game = Nim(*init)
        elif self.game_type == 'ledge':
            self.game = Ledge(init)
        else:
            raise ValueError('{} not valid game_type'.format(game_type))

    def get_environment_state(self):
        # State of the game
        return self.game.get_game_state()

    def generate_child_state(self, action):
        # Gets a child state without changing the environment
        return self.game.get_state_from_action(*action)

    def check_if_child_is_win(self, action):
        # Checks if an action leads to a win
        return self.game.does_action_give_win(*action)

    def move_to_child_state(self, action, p_num, verbose=True):
        # Do an action and get the resulting state
        player = p_num%2+1
        self.game.do_player_move(*action, player, verbose)

    def get_environment_status(self):
        # win, loose, play
        return self.game.game_status()

    def get_environment_value(self, player_num):
        # Quit playing, so someone has won
        # If player_num == 1, then 'win' is +1
        # If player_num == 2, then 'win' is -1 (means that player 2 won)
        if player_num == 1:
            return 1
        elif player_num == 2:
            return -1

    def get_possible_actions(self):
        # returns possible actions
        return self.game.get_possible_actions()
    
class Environment2:
    def __init__(self, game_type: str):
        # Game type: nim or ledge
        self.game_type = game_type
        self.set_game()
        
        # TODO: method to generate new state from state and action
        # - state should be ndarray, so state = board and a new state can be generated from an action

    def set_game(self):
        """
        :param init: K for nim
        """
        if self.game_type == 'nim':
            self.game = Nim(1000, K)
        elif self.game_type == 'ledge':
            self.game = Ledge(np.array([1,2,3,4,8]))
        else:
            raise ValueError('{} not valid game_type'.format(game_type))

    def generate_child_state_from_action(self, state, action):
        """
        :param state: board, either ndarray (ledge) or int (nim)
        :param action: tuple with action to do
        """
        return self.game.get_state_from_state_action(state, *action)

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