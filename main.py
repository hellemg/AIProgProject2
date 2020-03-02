import numpy as np

from GlobalConstants import *

if __name__ == '__main__':
    Menu = {
        'T': 'Testspace',
        'M': 'MCTS',
    }['M']

    if Menu == 'Testspace':
        print('Welcome to testspace')

    elif Menu == 'MCTS':
        print('Welcome to MCTS')
        


        """
        TODO:
        - verbose
        - final statistics
        - starting player
        """