import numpy as np


class MCTS:
    def __init__(self):
        self.c = 1
        # Dict to keep different values for nodes
        self.states = {}

    def tree_policy(self, state, possible_actions, combine_function, arg_function):
        print(state)
        print(possible_actions)
        # Using UCT to find best action in the tree
        # inout: state, possible actions from state,arg_function is either max or min, combine_function is either sum or minus
        # Returns an action
        # If the state has not been seen before, initialize it
        # Find the best action from state to child state
        best_action = None
        best_value = float("-inf")
        node = self.states[state]
        for a in possible_actions:
            u = self.c*np.sqrt(np.log(node.N)/(1+node.N_edge[a]))
            action_value = node.Q_edge_values[a]
            possible_best = combine_function((action_value, u))
            best_value = arg_function((possible_best, best_value))
            if best_value == possible_best:
                best_action = a
        return best_action

    def insert_state(self, state, possible_actions):
        # Add state to self.state, as a new Node
        self.states[state] = Node(possible_actions)

    def default_policy(self, state, possible_actions):
        # Using uniform distribution to get an action
        # inout: state, possible actions from state
        # Returns an action
        random_index = np.random.randint(len(possible_actions))
        return possible_actions[random_index]

    def backpropagate(self, visited_states, actions_done, result):
        """
        For each node in visited states
        Update N(s)
        Update N(s,a)
        Update Q(s,a)
        """
        for s, a in zip(reversed(visited_states), reversed(actions_done)):
            print('-------')
            print(s, a)
            print(self.states[s].N)
            node = self.states[s]
            node.update(a, result)
            print(self.states[s].N)
            input()


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
