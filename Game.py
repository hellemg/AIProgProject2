import numpy as np


class Nim:
    def __init__(self, N, K):
        # N, K as defined in GC
        self.total_pieces = N
        self.K = K
        self.verbose = verbose

    def remove_pieces(self, num_pieces: int, verbose: bool):
        # Remove pieces from pile
        self.total_pieces -= num_pieces
        if verbose:
            print('selects {} stones. Remaining stones = {}'.format(num_pieces, self.total_pieces))

    def game_status(self):
        # win, play (check for current player, cant loose)
        if self.total_pieces == 0:
            return 'win'
        else:
            return 'play'

    
    def get_game_state(self):
        return self.total_pieces


class Ledge:
    def __init__(self, B_init):
        # B_init is a numpy array, 2 is gold, 1 is copper, 0 is empty
        self.board = B_init
        # Last piece that was picked up, player has won if it is gold coin (1)
        self.picked_up = None

    def move_piece(self, boardcell: int, dist: int, verbose: bool):
        if self.board[boardcell] == 1:
            piece = 'copper'
        else:
            piece = 'gold'
        # Pick up from ledge
        if boardcell == 0:
            # Save the picked up piece for game status check
            self.picked_up = self.board[boardcell]
            if verbose:
                print('picks up {}'.format(piece))
        else:
            # Move piece to new cell
            self.board[boardcell-dis] = self.board[boardcell]
            if verbose:
                print('moves {} from cell {} to cell {}: {}'.format(piece, boardcell, boardcell-dist, self.board))
        # Remoce piece from old cell
        self.board[boardcell] = 0.

    def game_status(self):
        # win, play (check for current player, cant loose)
        if self.picked_up == 2:
            return 'win'
        else:
            return 'play'

    def get_game_state(self):
        return self.board