from Game import Nim, Ledge
from GlobalConstants import *

class Environment:
    def __init__(self, game_type: str, verbose = True):
        # Game type: nim or ledge
        self.game_type = game_type
        self.verbose = verbose

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
        # Do an action and get the resulting state
        self.game.do_player_move(*action)

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
    