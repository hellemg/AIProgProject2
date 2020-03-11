import numpy as np
from Environment import Environment


class Node:
    def __init__(self, state: str, parent, is_final, is_root=False):
        #print('...creating node {}, is final ={}'.format(state, is_final))
        self.name = state
        # Parent is a node
        self.parent = parent
        # Generated, but not visited
        self.N_s = 0
        self.E_t = 0
        # Edge-values, to be set when children are generated
        self.N_sa = {}
        self.Q_sa = {}
        self.E_t = {}
        # Flags to help with traversing methods
        self.is_final_state = is_final
        self.is_root = is_root
        # Newly generated nodes are leaf-nodes
        self.is_leaf = True

    def set_children(self, actions, children):
        """
        :param children: list of actions
        :param actions: list of nodes, children of corresponding actions
        """
        # Set actions and corresponding children of self
        self.actions = tuple(actions)
        self.children = tuple(children)
        self.is_leaf = False
        for a in self.actions:
            self.N_sa[a] = 0
            self.Q_sa[a] = 0
            self.E_t[a] = 0

    def update(self, eval_value):
        # print('...updating values for {}'.format(self.name))
        # Update values for a node
        self.N_s += 1
        self.E_t[self.action_done] += eval_value
        self.N_sa[self.action_done] += 1
        self.Q_sa[self.action_done] = self.E_t[self.action_done] / \
            self.N_sa[self.action_done]
        #self.print_node_values()

    def print_node_values(self):
        print('-N_s: {}\n-E_t: {}\n-N_sa: {}\n-Q_sa: {}'.format(self.N_s,
                                                                self.E_t, self.N_sa, self.Q_sa))

    def set_action_done(self, action):
        self.action_done = action
        #print('...{} action done is {}'.format(self.name, action))


class MCTS:
    def __init__(self, game_type):
        self.game_type = game_type
        self.c = 1
        # Dict to keep different values for nodes
        self.states = {}

    def simulate(self, player_number: int, M: int, init_state):
        # Create a node from begin-state
        node = Node(init_state, parent=None, is_final=False, is_root=True)
        for i in range(M):
            self.p_num = player_number
            #print('--- Simulation {} ---'.format(i+1))

            # 1. Follow tree policy to leaf node
            # TODO: use tree policy to go through the tree until a leaf-node is reached
            # Note: leaf-node may be a final state, but not necessary
            leaf_node = self.traverse_tree(node)

            # 2. When leaf-node is found, expand the leaf to get all children and return one of them (or `node` if it is a final state)
            # TODO: Update env_sim to it represents leaf node
            leaf_node = self.expand_leaf_node(leaf_node)

            # 3. Leaf evaluation
            eval_value = self.evaluate_leaf(leaf_node)

            # 4. Backprop
            self.backpropagate(leaf_node, eval_value)
            #input('...press any key to do next simulation\n\n')
        return self.get_simulated_action(node, player_number)

    def get_simulated_action(self, root_node, sim_player_num):
        #print('END. Get best action for Player {}'.format(sim_player_num%2+1))
        best_sim_action = None
        _, arg_func, best_value = self.get_minimax_functions(sim_player_num)
        #print(arg_func, best_value)
        for a in root_node.actions:
            poss_best_value = root_node.Q_sa[a]
            best_value = arg_func(best_value, root_node.Q_sa[a])
            #print('- action {} gives poss_best_value = {}, best_value = {}'.format(a, poss_best_value, best_value))
            if poss_best_value == best_value:
                #print('found better value:', poss_best_value)
                best_value = poss_best_value
                best_sim_action = a
        return best_sim_action

    def tree_policy(self, node, combine_function, arg_function, best_value):
        # Using UCT to find best action in the tree
        # :returns: index of best action in nodes actions
        # inout: node, possible actions from state,arg_function is either max or min, combine_function is either sum or minus
        #print('.. In tree policy')
        best_action_index = None
        # if arg_function(1, 2) == 2:
        #     print('...Player 1')
        # else:
        #     print('...Player 2')
        # node.print_node_values()
        for i, a in enumerate(node.actions):
            #print('...action {}:'.format(a))
            u = self.c*np.sqrt(np.log(node.N_s)/(1+node.N_sa[a]))
            action_value = node.Q_sa[a]
            possible_best = combine_function(action_value, u)
            best_value = arg_function(possible_best, best_value)
            #print('-u: {}\n-Q: {}\n-poss: {}\n-best: {}'.format(u,
            #                                                    action_value, possible_best, best_value))
            if best_value == possible_best:
                #print('...best value updated')
                best_action_index = i
        return best_action_index

    def traverse_tree(self, root_node):
        # Returns leafnode
        #print('1. Traverse tree with initial state {}, player p_num: {}'.format(
        #    root_node.name, self.p_num))
        node = root_node
        # Traverse until node is a leaf-node or a final state
        while not (node.is_leaf or node.is_final_state):
            combine_func, arg_func, best_value = self.get_minimax_functions(
                self.p_num)
            action_index = self.tree_policy(
                node, combine_func, arg_func, best_value)
            # Set chosen action for traversing later
            node.set_action_done(node.actions[action_index])
            
            old_s = node.name
            trans_action = node.action_done
            
            # Get child-node with same index as best action
            node = node.children[action_index]
            #print('...action {}: {} -> {}'.format(trans_action, old_s, node.name))
            # Next players turn
            self.p_num += 1
        return node

    def expand_leaf_node(self, node):
        # Expand if the node is not a final state
        env = Environment(self.game_type)
        init = env.get_init(node.name)
        env.set_game(init)
        #print('2. Expand leaf node', node.name)
        if not node.is_final_state:
            # Get all action from node, and the resulting states
            edges = env.get_possible_actions()
            child_nodes = []
            #print('... possible actions from {} are {}'.format(node.name, edges))
            for e in edges:
                # Get the child state action `e` would result in
                child_state = env.generate_child_state(action=e)
                is_final = env.check_if_child_is_win(action=e)
                #print('.......',e, is_final)
                # Add child node, with parent `node`
                child_node = Node(child_state, parent=node, is_final=is_final)
                child_nodes.append(child_node)

            node.set_children(edges, child_nodes)
            # print('randomly set - Player {} selects {} stones'.format(
            #     self.p_num % 2+1, edges[-1]))
            #print('randomly set - Player {} does {}'.format(self.p_num % 2+1, edges[-1]))
            node.set_action_done(edges[-1])
            # Moving on to a new layer, so next players turn
            self.p_num += 1
            # Returning last child node, as the value of all child_nodes as unknown
            return child_node
        # return node, to use in evaluation
        else:
            #print('... {} is a final state'.format(node.name))
            return node

    def default_policy(self, possible_actions):
        # Using uniform distribution to get an action
        random_index = np.random.randint(len(possible_actions))
        return possible_actions[random_index]

    def evaluate_leaf(self, node):
        # TODO: I could ensure same env is used everywhere
        # Do rollout on `node` to get value
        #print('3. Evaluate leaf node', node.name)
        env = Environment(self.game_type)
        init = env.get_init(node.name)
        env.set_game(init)
        #print(node.is_final_state)
        if node.is_final_state:
            final_player = (self.p_num-1) % 2+1
            eval_value = env.get_environment_value(final_player)
            #print('Player {} wins, eval_value={}'.format(final_player, eval_value))
            return eval_value
        else: 
            #print(env.get_environment_status())
            while env.get_environment_status() == 'play':
                possible_actions = env.get_possible_actions()
                #print(possible_actions)
                action = self.default_policy(possible_actions)
                env.move_to_child_state(action, self.p_num, verbose=False)
                self.p_num += 1
            final_player = (self.p_num-1) % 2+1
            eval_value = env.get_environment_value(final_player)
            #print('Player {} wins, eval_value={}'.format(final_player, eval_value))
            return eval_value

    def backpropagate(self, node, eval_value):
        #print('4. Backpropagate from state {}, result is {}'.format(
        #    node.name, eval_value))
        # BP until node has no parent
        while not node.is_root:
            # TODO: Update all relevant values
            # Skip leaf node, as it has no N(s,a) values
            node = node.parent
            node.update(eval_value)

    def get_minimax_functions(self, p_num):
        if p_num % 2+1 == 1:
            return lambda x1, x2: x1+x2, lambda x1, x2: np.max((x1, x2)), float("-inf")
        elif p_num % 2+1 == 2:
            return lambda x1, x2: x1-x2, lambda x1, x2: np.min((x1, x2)), float("inf")

            # class MCTS:
            #     def __init__(self, game_type):
            #         self.game_type = game_type
            #         self.c = 1
            #         # Dict to keep different values for nodes
            #         self.states = {}

            #     def get_best_action_by_simulating(self, player_number:int, M: int, state):
            #         """
            #         :param player_number: any int >= 0, which player asking for simulated move
            #         :param state: environment state to begin the simulation from
            #         :returns: action, best action found after M simulations
            #         """
            #         for i in range(M):
            #             # Create a new game for each simulation, beginning from `state`
            #             env_sim = Environment(self.game_type)
            #             init = env_sim.get_init(state)
            #             env_sim.set_game(init)

            #             # When `state` has not been seen before (first simulation of first move)
            #             if state not in self.states:
            #                 print('...inserting {} into states dict, new node has been created'.format(state))
            #                 self.insert_state(state, env_sim.get_possible_actions())

            #             # Step 1: Traverse tree
            #             env_sim, visited_states, actions_done, player_number = self.traverse_tree(env_sim, player_number)

            #             # Step 2: Expand tree with new node
            #             self.node_expansion(env_sim)

            #             # Step 3: Evaluate leaf node
            #             eval = self.evaluate_leaf(env_sim, player_number)

            #             # Step 4: Backpropagation
            #             self.backpropagate(visited_states, actions_done, eval)

            #         # Return the best action
            #         return self.get_best_simulation_action(state)

            #     def traverse_tree(self, env, p_num):
            #         s = env.get_environment_state()
            #         visited_states = []
            #         actions_done = []
            #         # Traverse the tree until a leaf node is found or a final state is reached
            #         while s in self.states:
            #             #print('...in tree search, there are {} states in the tree'.format(len(self.states.keys())))
            #             #for key in self.states.keys():
            #             #    print(key)
            #             #print('........')
            #             combine_func, arg_func, best_value = self.get_minimax_functions(p_num)
            #             possible_actions = env.get_possible_actions()
            #             action = self.tree_policy(s, possible_actions, combine_func, arg_func, best_value)
            #             # Do the action
            #             env.generate_child_state(action, p_num, verbose=False)
            #             # Add state and action to lists
            #             visited_states.append(s)
            #             actions_done.append(action)
            #             # Action has been done, next players turn
            #             p_num += 1

            #             # Old state for printing
            #             old_s = s

            #             # Get next state and possible actions
            #             s = env.get_environment_state()
            #             possible_actions = env.get_possible_actions()

            #             # Printing state transition
            #             #print('-- action {}: {} -> {}'.format(action, old_s, s))

            #             # If the new state is a win, stop
            #             if env.get_environment_status() != 'play':
            #                 return env, visited_states, actions_done, p_num
            #         return env, visited_states, actions_done, p_num

            #     def node_expansion(self, env):
            #         state = env.get_environment_state()
            #         possible_actions = env.get_possible_actions()
            #         # Add state `s` to the tree
            #         self.insert_state(state, possible_actions)

            #     def tree_policy(self, state, possible_actions, combine_function, arg_function, best_value):
            #         # Using UCT to find best action in the tree
            #         # inout: state, possible actions from state,arg_function is either max or min, combine_function is either sum or minus
            #         # Returns an action
            #         # If the state has not been seen before, initialize it
            #         # Find the best action from state to child state
            #         best_action = None
            #         node = self.states[state]
            #         for a in possible_actions:
            #             u = self.c*np.sqrt(np.log(node.N)/(1+node.N_edge[a]))
            #             action_value = node.Q_edge_values[a]
            #             possible_best = combine_function(action_value, u)
            #             best_value = arg_function(possible_best, best_value)
            #             if best_value == possible_best:
            #                 best_action = a
            #         return best_action

            #     def insert_state(self, state, possible_actions):
            #         # Add state to self.state, as a new Node
            #         self.states[state] = Node(possible_actions)
            #         node_state= self.states[state]
            #         #print('...inserted {} to states, values are:\n- N: {}\n- N_edge: {}\n- E: {}\n- Q: {}'.format(state, node_state.N, node_state.N_edge, node_state.E, node_state.Q_edge_values))

            #     def default_policy(self, state, possible_actions):
            #         # Using uniform distribution to get an action
            #         # inout: state, possible actions from state
            #         # Returns an action
            #         random_index = np.random.randint(len(possible_actions))
            #         return possible_actions[random_index]

            #     def evaluate_leaf(self, env, p_num):
            #         s = env.get_environment_state()
            #         #print('... 3. evaluate leaf node, leaf state:', s)
            #         while env.get_environment_status() == 'play':
            #             possible_actions = env.get_possible_actions()
            #             action = self.default_policy(s, possible_actions)
            #             #print('possible actions: {}\naction: {}'.format(possible_actions, action))
            #             # Do the action
            #             env.generate_child_state(action, p_num, verbose=False)
            #             # NOT adding state and action to lists, only get value from rollout
            #             # Action has been done, next players turn
            #             p_num += 1
            #             # Get next state
            #             s = env.get_environment_state()
            #         # Evaluate environment, use p_num - 1 since it has been incremented
            #         eval = env.get_environment_value((p_num-1)%2+1)
            #         #print('In evaluate - player {} wins, eval={}'.format((p_num-1)%2+1,eval))
            #         return eval

            #     def backpropagate(self, visited_states, actions_done, result):
            #         """
            #         For each node in visited states
            #         Update N(s)
            #         Update N(s,a)
            #         Update Q(s,a)
            #         """
            #         for s, a in zip(reversed(visited_states), reversed(actions_done)):
            #             # print('... 4. Backprop')
            #             # print(s, a, result)
            #             node = self.states[s]
            #             node.update(a, result)
            #             # print('new N, Q',self.states[s].N, self.states[s].Q_edge_values)

            #     def get_minimax_functions(self, p_num):
            #             if p_num%2+1 == 1:
            #                 return lambda x1,x2: x1+x2, lambda x1,x2: np.max((x1,x2)), float("-inf")
            #             elif p_num%2+1 == 2:
            #                 return lambda x1,x2: x1-x2, lambda x1,x2: np.min((x1,x2)), float("inf")

            #     def get_best_simulation_action(self, state):
            #         best_sim_val = float('-inf')
            #         for a, v in self.states[state].Q_edge_values.items():
            #             if v > best_sim_val:
            #                 best_sim_val = v
            #                 best_sim_act = a
            #         return best_sim_act
            #         # print(self.states[state].Q_edge_values)
            #         # print('*** best action after simulation is {}, with a value of {}'.format(best_sim_act, best_sim_val))

            # class Node:
            #     def __init__(self, possible_actions):
            #         # number of times a state has been visited. TODO: Check that init=1 is ok
            #         self.N = 1
            #         # Dict to hold number of times a specific action from state s has been taken. default is 0
            #         self.N_edge = {}
            #         # Dict to hold eval for a specific action from state s. default is 0
            #         self.E = {}
            #         # Dict to hold Q(s,a) values for this state and all actions, defualt is 0
            #         self.Q_edge_values = {}
            #         for a in possible_actions:
            #             self.N_edge[a] = 0
            #             self.E[a] = 0
            #             self.Q_edge_values[a] = 0

            #     def update(self, action, eval):
            #         # Update values for a node
            #         self.increment_N()
            #         self.increment_N_edge(action)
            #         self.update_E(action, eval)
            #         self.update_Q_edge_values(action)

            #     def increment_N(self):
            #         self.N += 1

            #     def increment_N_edge(self, action):
            #         self.N_edge[action] += 1

            #     def update_E(self, action, eval):
            #         self.E[action] += eval

            #     def update_Q_edge_values(self, action):
            #         self.Q_edge_values[action] = self.E[action]/self.N_edge[action]
