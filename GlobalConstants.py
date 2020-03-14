
import numpy as np

# NOTE: Player 1 is max-player

verbose = False

# Number of games in a batch
G = 10

game_type = 'ledge'

# Number of simulations (and therefore rollouts) for each move
M = 500

# For Nim, number of pieces at the beginning
N = 50

# For Nim, number of pieces allowed to remove
K = 10

# Player to start, 1,2,3
P = 1

# For Ledge, initial board
lenght = 8
num_coppers = 4


def create_B_init(length: int, num_copper: int):
    # Length of board, number of coppers on the board
    board = np.zeros(length, dtype=int)
    # Find boardcells for all coind, cant crash with each other
    copper_indices = np.random.choice(length, num_copper+1, replace=False)
    # Place gold coin on one of the boardcells (random)
    board[copper_indices[0]] = 2
    # Place copper coins on the remaining generated boardcells
    board[copper_indices[1:]] = 1
    return board


#B_init = np.array([1,1,0,2])
#B_init = create_B_init(lenght, num_coppers)
B_init = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 2, 0, 0, 1, 1, 1])
