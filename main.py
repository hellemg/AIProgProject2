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

        def get_player_number(p_num):
            # Return randomly P1 or P2
            if p_num == 3:
                return np.random.randint(2)
            # Defined p_num to be 0 for P1 and 1 for P2
            else:
                return p_num-1

        def get_init(game_type):
            if game_type == 'nim':
                return (N, K)
            elif game_type == 'ledge':
                return B_init

        p1_wins = 0
        p1_start = 0
        for j in range(G):
            env = Environment(game_type)
            init = get_init(game_type)
            env.set_game(init)
            mcts = MCTS(game_type)
            state = env.get_environment_state()
            player_number = get_player_number(P)
            # Player number is 0 for P1 and 1 for P2
            p1_start += ((player_number+1)%2)
            while env.get_environment_status() == 'play':
                possible_actions = env.get_possible_actions()
                # Do M simulations
                best_action = mcts.simulate(player_number, M, state)
                #best_action = mcts.get_best_action_by_simulating(
                #    player_number, M=M, state=state)
                
                # Do the action
                env.move_to_child_state(
                    best_action, player_number, verbose)
                # Get next state
                state = env.get_environment_state()
                # Next players turn
                player_number += 1
            winner = (player_number-1) % 2+1
            if verbose:
                print('Player {} wins'.format(winner))
            if winner == 1:
                p1_wins += 1
            print('*** Game {} done ***'.format(j+1))
        
        print('Player 1 wins {} of {} games ({}%.\nPlayer 1 started {}% of the time)'.format(p1_wins, G, p1_wins/G*100, p1_start/G*100))

        """
        TODO: 
        - Add methods to ledge that does not exist
        - Test for ledge
        - Go through oppgavetekst and ensure everything is ok
        - Comment code
        - Decide what to clean
        - Clean
        """