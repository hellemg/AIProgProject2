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