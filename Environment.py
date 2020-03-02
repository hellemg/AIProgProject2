class Environment:
    def __init__(self, verbose):
        self.verbose = verbose
    
    def generate_initial_state(self):
        raise NotImplementedError

    def generate_child_states(self):
        raise NotImplementedError

    def get_environment_status(self):
        # win, loose, play
        raise NotImplementedError

    