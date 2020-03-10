import numpy as np


class MCTS:
    def __init__(self):
        self.c = 1
        # Dict to keep different values for nodes
        self.states = {}

    def tree_policy(self, state, possible_actions, combine_function, arg_function, best_value):
        print(state)
        print(possible_actions)
        # Using UCT to find best action in the tree
        # inout: state, possible actions from state,arg_function is either max or min, combine_function is either sum or minus
        # Returns an action
        # If the state has not been seen before, initialize it
        # Find the best action from state to child state
        best_action = None
        node = self.states[state]
        for a in possible_actions:
            u = self.c*np.sqrt(np.log(node.N)/(1+node.N_edge[a]))
            action_value = node.Q_edge_values[a]
            possible_best = combine_function(action_value, u)
            best_value = arg_function(possible_best, best_value)
            if best_value == possible_best:
                best_action = a
        print('___ best value', best_value)
        return best_action

    def insert_state(self, state, possible_actions):
        # Add state to self.state, as a new Node
        self.states[state] = Node(possible_actions)
        node_state= self.states[state]
        #print('...inserted {} to states, values are:\n- N: {}\n- N_edge: {}\n- E: {}\n- Q: {}'.format(state, node_state.N, node_state.N_edge, node_state.E, node_state.Q_edge_values))

    def default_policy(self, state, possible_actions):
        # Using uniform distribution to get an action
        # inout: state, possible actions from state
        # Returns an action
        random_index = np.random.randint(len(possible_actions))
        return possible_actions[random_index]

    def traverse_tree(self, s, env):
        p_num = 0
        visited_states = []
        actions_done = []
        # Traverse the tree until a leaf node is found or a final state is reached
        while s in self.states:
            print('...in tree search, there are {} states in the tree'.format(len(self.states.keys())))
            combine_func, arg_func, best_value = self.get_minimax_functions(p_num)
            possible_actions = env.get_possible_actions()
            action = self.tree_policy(s, possible_actions, combine_func, arg_func, best_value)
            # Do the action
            env.generate_child_state(action)
            # Add state and action to lists
            visited_states.append(s)
            actions_done.append(action)
            print('action done: {}'.format(action))
            # Action has been done, next players turn
            p_num += 1
            # Get next state and possible actions
            s = env.get_environment_state()
            possible_actions = env.get_possible_actions()
            # If the new state is a win, stop
            if env.get_environment_status() != 'play':
                return s, visited_states, actions_done, p_num
        return s, visited_states, actions_done, p_num
        

    def evaluate_leaf(self, s, env, p_num):
        print('... 3. evaluate leaf node, leaf state:', s)
        while env.get_environment_status() == 'play':
            possible_actions = env.get_possible_actions()
            action = self.default_policy(s, possible_actions)
            #print('possible actions: {}\naction: {}'.format(possible_actions, action))
            # Do the action
            env.generate_child_state(action)
            # NOT adding state and action to lists, only get value from rollout
            # Action has been done, next players turn
            p_num += 1
            # Get next state
            s = env.get_environment_state()
        eval = env.get_environment_value(p_num%2+1)
        print('In evaluate - player {} wins, eval={}'.format(p_num%2+1,eval))
        return eval

    def backpropagate(self, visited_states, actions_done, result):
        """
        For each node in visited states
        Update N(s)
        Update N(s,a)
        Update Q(s,a)
        """
        for s, a in zip(reversed(visited_states), reversed(actions_done)):
            print('... 4. Backprop')
            print(s, a, result)
            node = self.states[s]
            node.update(a, result)
            print('new N, Q',self.states[s].N, self.states[s].Q_edge_values)

    def get_minimax_functions(self, p_num):
            if p_num%2+1 == 1:
                return lambda x1,x2: x1+x2, lambda x1,x2: np.max((x1,x2)), float("-inf")
            elif p_num%2+1 == 2:
                return lambda x1,x2: x1-x2, lambda x1,x2: np.min((x1,x2)), float("inf")

class Node:
    def __init__(self, possible_actions):
        # number of times a state has been visited. TODO: Check that init=1 is ok
        self.N = 1
        # Dict to hold number of times a specific action from state s has been taken. default is 0
        self.N_edge = {}
        # Dict to hold eval for a specific action from state s. default is 0
        self.E = {}
        # Dict to hold Q(s,a) values for this state and all actions, defualt is 0
        self.Q_edge_values = {}
        for a in possible_actions:
            self.N_edge[a] = 0
            self.E[a] = 0
            self.Q_edge_values[a] = 0

    def update(self, action, eval):
        # Update values for a node
        self.increment_N()
        self.increment_N_edge(action)
        self.update_E(action, eval)
        self.update_Q_edge_values(action)

    def increment_N(self):
        self.N += 1

    def increment_N_edge(self, action):
        self.N_edge[action] += 1

    def update_E(self, action, eval):
        self.E[action] += eval

    def update_Q_edge_values(self, action):
        self.Q_edge_values[action] = self.E[action]/self.N_edge[action]
