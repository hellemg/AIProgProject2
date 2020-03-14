import numpy as np


class Nim:
    def __init__(self, K):
        # K as defined in GC
        self.K = K

    def get_state_from_state_action(self, total_pieces, num_pieces, player, verbose):
        """
        :param num_pieces: int, pieces getting picked up

        :returns: int, pieces left on the board
        """
        if verbose:
            print('Player {} selects {} stones. Remaining stones = {}'.format(
                player, num_pieces, total_pieces-num_pieces))
        return total_pieces-num_pieces

    def check_game_done(self, total_pieces):
        """
        :param total_pieces: int, pieces on the board

        returns: boolean, if all pieces have been picked up
        """
        return total_pieces == 0

    def get_possible_actions_from_state(self, total_pieces):
        """
        :param total_pieces: int, pieces on the board

        :returns: list tuples with possible actions to take
        """
        # returns list of possible number of pieces to pick up
        max_pieces = np.minimum(self.K, total_pieces)+1
        return [(i,) for i in range(1, max_pieces)]


class Ledge:
    def __init__(self):
        # Last piece that was picked up, player has won if it is gold coin (1)
        self.picked_up = None

    def get_state_from_state_action(self, board, boardcell: int, dist: int, player, verbose):
        """
        :param board: ndarray, ledge-board
        :param boardcell: cell that something should be moved from
        :param dist: distance to the left from boardcell to move item to. Is 0 if boardcell == 0

        :returns: ndarray, new state of the board
        """
        temp_board = board.copy()
        if temp_board[boardcell] == 1:
            piece = 'copper'
        else:
            piece = 'gold'
        # Move piece to new cell. If boardcell == 0, then dist == 0 and nothing happens
        temp_board[boardcell-dist] = temp_board[boardcell]
        # Remoce piece from old cell
        temp_board[boardcell] = 0.
        # print('board and board copy:', self.board, board)
        if verbose:
            if boardcell == 0:
                print('Player {} picks up {}: {}'.format(
                    player, piece, temp_board))
            else:
                print('Player {} moves {} from cell {} to cell {}: {}'.format(
                    player, piece, boardcell, boardcell-dist, temp_board))
        return temp_board

    def check_game_done(self, board):
        """
        :param board: ndarray, ledge-board

        returns: boolean, True if there is no gold piece (2)
        """
        return not 2 in board

    def get_possible_actions_from_state(self, board):
        """
        :param board: ndarray, ledge-board

        :returns: list tuples with possible actions to take
        """
        actions = []
        dists = 0
        for i, cell in enumerate(board):
            # Go through the board from the left to the right
            # If the cell is 0, save it as it can be used for the dist
            # If the cell is not 0, use all saved dists together with the cell
            if cell == 0:
                dists += 1
            else:
                actions += [(i, d+1) for d in range(dists)]
                dists = 0
        # Add first cell to actions, can be picked up
        if board[0] != 0:
            actions.append((0, 0))
        return actions
