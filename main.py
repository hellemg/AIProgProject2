import numpy as np

from GlobalConstants import *
from Game import *
from Environment import Environment
from MCTS import MCTS

if __name__ == '__main__':
    Menu = {
        'T': 'Testspace',
        'M': 'MCTS',
    }['M']

    if Menu == 'Testspace':
        print('Welcome to testspace')

    elif Menu == 'MCTS':
        print('Welcome to MCTS')

        def get_minimax_functions(p_num):
            if p_num%2+1 == 1:
                return lambda x1,x2: x1+x2, lambda x1,x2: np.max((x1,x2))
            elif p_num%2+1 == 2:
                return lambda x1,x2: x1-x2, lambda x1,x2: np.min((x1,x2))

        env = Environment('ledge')
        env.set_game(B_init)
        mcts = MCTS()
        state = env.get_environment_state()
        while env.get_environment_status() == 'play':
            possible_actions = env.get_possible_actions()
            print('state', state)
            print('possible_actions', possible_actions)
            # TODO: Get the best action by simulating M rollout games

            # Returns: tuple!! containing the best action
            # Do M simulations to get the best move. 1 simulation is
            # s0 is state we begin from
            """
            - tree search: find the root node
            - node expansion: add child states to the tree
            - leaf evaluation: rollout from a leaf node
            - backpropagation: update values for nodes
            """
            # Do M simulations
            print('-------------')
            for i in range(5):
                # ALWAYS P1s turn to do something when a simulation occurs.P1 = 0, P2 = 1
                p_num = 0
                # TODO: Create an initialization that takes in a state
                env = Environment('ledge')
                # Create a board from current state
                init = env.get_init(state)
                env.set_game(init)
                visited_states = []
                actions_done = []
                # Set initial state for simulation
                s = env.get_environment_state()
                # S is not in the tree, add it to the tree. ASSUMING FIRST STATE IS NOT A WIN/LOOSE
                mcts.insert_state(state, possible_actions)
                # Traverse the tree until a leaf node is found
                while s in mcts.states:
                    # TODO: Find out why states are not appending
                    # I do a while statement, as I then need to check for the existence of a
                    # key in a hash table O(1), instead of counting number of states in the tree
                    possible_actions = env.get_possible_actions()
                    combine_func, arg_func = get_minimax_functions(p_num)
                    # TODO: Check that minimax-functions work for player 2 (after fixing visited states)
                    # print('player ',p_num,'combine, arg:', combine_func(6,4), arg_func(9,6))
                    # input()
                    action = mcts.tree_policy(s, possible_actions, combine_func, arg_func)
                    # Do the action
                    env.generate_child_state(action)
                    # Add state and action to lists
                    visited_states.append(s)
                    actions_done.append(action)
                    # Action has been done, next players turn
                    p_num += 1
                    # Get next state
                    s = env.get_environment_state()

                # When s is not in env-states, do rollout. 
                eval = mcts.evaluate_leaf(s, env)
                # Backpropagate values
                print('visited states:', visited_states)
                mcts.backpropagate(visited_states, actions_done, eval)
                input()

            # FOR REAL GAME
            # action = 'get best action from M simulations'#mcts.tree_policy(state, possible_actions, np.sum, np.max)
            # action = mcts.tree_policy(state, possible_actions, np.sum, np.max)
            # print('doing', action)
            # # Do the action
            # env.generate_child_state(action)
            # # Get next state
            # state = env.get_environment_state()
            # input()

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

        # b_init = create_B_init(10, 5)
        # ledge = Ledge(b_init)
        # p = 0
        # print(ledge.get_game_state())
        # while ledge.game_status() =='play':
        #     print(ledge.get_possible_actions())
        #     cell = int(input('cell: '))
        #     dist = int(input('dist: '))
        #     print('P{} '.format(p%2+1), end='')
        #     ledge.move_piece(cell, dist, True)

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


        1. Tree Search - Traversing the tree from the root to a leaf node by using the tree policy.
        suggestions:
        - get_leaf_node(root_state): traverse the tree using the tree policy. tree_policy(state) must be another method

        2. Node Expansion - Generating some or all child states of a parent state, and then connecting the tree
        node housing the parent state (a.k.a. parent node) to the nodes housing the child states (a.k.a. child
        nodes).
        suggestions:
        - isnt this a part of 1 and 3??

        3. Leaf Evaluation - Estimating the value of a leaf node in the tree by doing a rollout simulation using
        the default policy from the leaf node’s state to a final state.
        suggestions:
        - get_leaf_value_estimate(leaf_state): do rollout, needs default_policy_method(state) as well

        4. Backpropagation - Passing the evaluation of a final state back up the tree, updating relevant data (see
        course lecture notes) at all nodes and edges on the path from the final state to the tree root.
        suggestions:
        - all nodes needs to know who their parent is (this is probably where 2. comes in). maybe do as in TD, and have list of visited states?
        - traverse list of visited states and update information in n(s) 
        """
