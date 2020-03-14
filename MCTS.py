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
        #print('...updating values for {}'.format(self.name))
        # Update values for a node
        self.N_s += 1
        self.E_t[self.action_done] += eval_value
        self.N_sa[self.action_done] += 1
        self.Q_sa[self.action_done] = self.E_t[self.action_done] / \
            self.N_sa[self.action_done]
        # self.print_node_values()

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
        # TODO: Add self.evaluate_leaf (=rollout) and self.evaluate_ciritc (NN), so it is generalized and both can be used

    def simulate(self, player_number: int, M: int, init_state):
        # Create a node from begin-state
        node = Node(init_state, parent=None, is_final=False, is_root=True)
        for i in range(M):
            self.p_num = player_number
            #print('--- Simulation {} ---'.format(i+1))

            # 1. Follow tree policy to leaf node
            # Note: leaf-node may be a final state, but not necessary
            leaf_node = self.traverse_tree(node)

            # 2. When leaf-node is found, expand the leaf to get all children and return one of them (or `node` if it is a final state)
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
            # print('-u: {}\n-Q: {}\n-poss: {}\n-best: {}'.format(u,
            #                                                    action_value, possible_best, best_value))
            if best_value == possible_best:
                #print('...best value updated')
                best_action_index = i
        return best_action_index

    def traverse_tree(self, root_node):
        # Returns leafnode
        # print('1. Traverse tree with initial state {}, player p_num: {}'.format(
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
        # TODO: Use nodes in rollout

        # Do rollout on `node` to get value
        #print('3. Evaluate leaf node', node.name)
        env = Environment(self.game_type)
        init = env.get_init(node.name)
        env.set_game(init)
        # print(node.is_final_state)
        if node.is_final_state:
            final_player = (self.p_num-1) % 2+1
            eval_value = env.get_environment_value(final_player)
            #print('leaf was final - Player {} wins, eval_value={}'.format(final_player, eval_value))
            #input('\n\n\n\n\n IN FINAL PRESS KEY')
            return eval_value
        else:
            # print(env.get_environment_status())
            while env.get_environment_status() == 'play':
                possible_actions = env.get_possible_actions()
                # print(possible_actions)
                action = self.default_policy(possible_actions)
                env.move_to_child_state(action, self.p_num, verbose=False)
                self.p_num += 1
            final_player = (self.p_num-1) % 2+1
            eval_value = env.get_environment_value(final_player)
            #print('leaf not final - Player {} wins, eval_value={}'.format(final_player, eval_value))
            return eval_value

    def backpropagate(self, node, eval_value):
        # print('4. Backpropagate from state {}, result is {}'.format(
        #    node.name, eval_value))
        # BP until node has no parent
        while not node.is_root:
            # Skip leaf node, as it has no N(s,a) values
            node = node.parent
            node.update(eval_value)

    def get_minimax_functions(self, p_num):
        if p_num % 2+1 == 1:
            return lambda x1, x2: x1+x2, lambda x1, x2: np.max((x1, x2)), float("-inf")
        elif p_num % 2+1 == 2:
            return lambda x1, x2: x1-x2, lambda x1, x2: np.min((x1, x2)), float("inf")
