
import numpy as np
# Game size
game_size = 10

# Number of games to play
num_episodes = 100


if 'ledge' == 'nim':
    # Number of simulations (and therefore rollouts) for each move
    M = 500

    # For Nim, number of pieces at the beginning
    N = 99

    # For Nim, number of pieces allowed to remove
    K = 7

    # Number of games in a batch
    G = 4

    # Player to start, 1,2,3
    P = 1
else:
    # Number of games in a batch
    G = 4

    # Player to start, 1,2,3
    P = 1

    # Number of simulations (and therefore rollouts) for each move
    M = 500

    # For Ledge, initial board
    def create_B_init(length: int, num_copper: int):
        # Length of board, number of coppers on the board
        board = np.zeros(length)
        # Find boardcells for all coind, cant crash with each other
        copper_indices = np.random.choice(length, num_copper+1, replace=False)
        # Place gold coin on one of the boardcells (random)
        board[copper_indices[0]] = 2
        # Place copper coins on the remaining generated boardcells
        board[copper_indices[1:]] = 1
        return board
