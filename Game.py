import numpy as np


class Nim:
    def __init__(self, N, K):
        # N, K as defined in GC
        self.total_pieces = N
        self.K = K

    def do_player_move(self, num_pieces: int, player, verbose):
        # Remove pieces from pile
        self.total_pieces -= num_pieces
        if verbose:
            print('Player {} selects {} stones. Remaining stones = {}'.format(
                player, num_pieces, self.total_pieces))

    def get_state_from_action(self, num_pieces):
        # Simulates a move, but does not change the environment
        return str(self.total_pieces-num_pieces)

    def does_action_give_win(self, num_pieces):
        # Tells if an action taken on the current board results in a win
        return self.total_pieces == num_pieces

    def game_status(self):
        # win, play (check for current player, cant loose)
        if self.total_pieces == 0:
            return 'win'
        else:
            return 'play'

    def get_possible_actions(self):
        # returns list of possible number of pieces to pick up
        max_pieces = np.minimum(self.K, self.total_pieces)+1
        return [(i,) for i in range(1, max_pieces)]

    def get_game_state(self):
        return str(self.total_pieces)


class Ledge:
    def __init__(self, B_init):
        # B_init is a numpy array, 2 is gold, 1 is copper, 0 is empty
        self.board = B_init.copy()
        # Last piece that was picked up, player has won if it is gold coin (1)
        self.picked_up = None

    def do_player_move(self, boardcell: int, dist: int, player, verbose):
        if self.board[boardcell] == 1:
            piece = 'copper'
        else:
            piece = 'gold'
        # Pick up from ledge
        if boardcell == 0:
            # Save the picked up piece for game status check
            self.picked_up = self.board[boardcell]
            # Remoce piece from old cell
            self.board[boardcell] = 0.
            if verbose:
                print('Player {} picks up {}: {}'.format(
                    player, piece, self.board))
        else:
            # Move piece to new cell
            self.board[boardcell-dist] = self.board[boardcell]
            # Remoce piece from old cell
            self.board[boardcell] = 0.
            if verbose:
                print('Player {} moves {} from cell {} to cell {}: {}'.format(
                    player, piece, boardcell, boardcell-dist, self.board))

    def get_state_from_action(self, boardcell: int, dist: int):
        # Simulates a move, but does not change the environment
        board = self.board.copy()
        #print('board and board copy:', self.board, board)
        # Pick up from ledge
        if boardcell == 0:
            # Save the picked up piece for game status check
            #self.picked_up = self.board[boardcell]
            # Remoce piece from old cell
            board[boardcell] = 0.
            #print('board and board copy:', self.board, board)
            return ''.join(map(str, board))
        else:
            # Move piece to new cell
            board[boardcell-dist] = board[boardcell]
            # Remoce piece from old cell
            board[boardcell] = 0.
            #print('board and board copy:', self.board, board)
            return ''.join(map(str, board))

    def does_action_give_win(self, boardcell: int, dist: int):
        # Tells if an action taken on the current board results in a win
        #print('board and boardcell', self.board, boardcell)
        return boardcell==0 and self.board[boardcell] == 2.

    def game_status(self):
        # win, play (check for scurrent player, cant loose)
        if self.picked_up == 2:
            return 'win'
        else:
            return 'play'

    def get_possible_actions(self):
        # Need to return pairs of boardcell (index) and distance (int, how much I can move to the left)
        # Each boardcell can have several dists, I'll return a tuple for each pair
        actions = []
        dists = 0
        for i, cell in enumerate(self.board):
            # Go through the board from the left to the right
            # If the cell is 0, save it as it can be used for the dist
            # If the cell is not 0, use all saved dists together with the cell
            if cell == 0:
                dists += 1
            else:
                actions += [(i, d+1) for d in range(dists)]
                dists = 0
        # Add first cell to actions, can be picked up
        if self.board[0] != 0:
            actions.append((0, 0))
        return actions

    def get_game_state(self):
        return ''.join(map(str, self.board))
