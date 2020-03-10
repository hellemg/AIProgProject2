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

        env = Environment('ledge')
        env.set_game(B_init)
        mcts = MCTS()
        state = env.get_environment_state()
        while env.get_environment_status() == 'play':
            possible_actions = env.get_possible_actions()
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
            for i in range(M):
                # ALWAYS P1s turn to do something when a simulation occurs.P1 = 0, P2 = 1
                env = Environment('ledge')
                # Create a board from current state
                init = env.get_init(state)
                env.set_game(init)
                # Set initial state for simulation
                s = state
                possible_actions = env.get_possible_actions()
                # S is not in the tree, add it to the tree
                # TODO: Do not need to insert state if it is not first round, as recommended action will always have been
                # in the simulation
                if s not in mcts.states:
                    print('...inserting {} into states dict, new node has been created'.format(s))
                    mcts.insert_state(s, possible_actions)
                
                # Traverse tree
                s, visited_states, actions_done, p_num = mcts.traverse_tree(s, env)

                # Expand the tree with one node, s is now a leaf node. This should be added to visited states
                mcts.insert_state(s, possible_actions)
                print('...visited states', visited_states)

                # When s is not in env-states, do rollout. 
                eval = mcts.evaluate_leaf(s, env, p_num)
                # Backpropagate values
                print('visited states:', visited_states)
                mcts.backpropagate(visited_states, actions_done, eval)

            # Best action to do after simulation
            best_sim_val = float('-inf')
            for a, v in mcts.states[state].Q_edge_values.items():
                if v > best_sim_val:
                    best_sim_val = v
                    best_sim_act = a
            print(mcts.states[state].Q_edge_values)
            print('*** best action after simulation is {}, with a value of {}'.format(best_sim_act, best_sim_val))
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
