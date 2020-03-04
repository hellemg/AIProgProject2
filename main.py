import numpy as np

from GlobalConstants import *
from Game import *

if __name__ == '__main__':
    Menu = {
        'T': 'Testspace',
        'M': 'MCTS',
    }['M']

    if Menu == 'Testspace':
        print('Welcome to testspace')

    elif Menu == 'MCTS':
        print('Welcome to MCTS')
        # K = 7
        # nim = Nim(20, K)
        # p = 0
        # while nim.game_status() == 'play':
        #     possible_actions = nim.get_possible_actions()
        #     print(possible_actions)
        #     remove = possible_actions[np.random.randint(len(possible_actions))]
        #     print('P{} '.format(p%2+1), end='')
        #     nim.remove_pieces(remove, True)
        #     nim.game_status()
        #     p += 1
        # exit()

        b_init = create_B_init(10, 5)
        ledge = Ledge(b_init)
        p = 0
        print(ledge.get_game_state())
        while ledge.game_status() =='play':
            print(ledge.get_possible_actions())
            cell = int(input('cell: '))
            dist = int(input('dist: '))
            print('P{} '.format(p%2+1), end='')
            ledge.move_piece(cell, dist, True)

        """
        TODO:
        - verbose
        - final statistics
        - starting player
        """

        """
        TODO:
        - tree policy/simulation policy (greedy or optimism in the face of uncertainty. latter is better)
        - default policy/rollout policy (uniform)
        - P1 policy and P2 policy, wrap in policy-method that takes in which player
        - MAYBE NOT; SEE NEXT POINT table: (s,a) -> s'. nim: a - number. ledge: a - (number, number) (cell, dist). Do I want s -> actions -> s' ? or (s,a) -> s'
        - n(s): node. contains: total count for state N(s), action value Q(s,a), count N(s,a) for each a in A (and child-nodes/parent-node?)
        - For each simulation, add the first state encountered, that is not already represented in the tree, to the search tree.
        """