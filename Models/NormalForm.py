from itertools import product
import numpy as np

def collect_info_sets(root):
    '''
    Traverse the tree as an extensive form and collect the info sets of all players
    return :
        info_sets[player] = { info_set_id: actions}
    '''
    info_sets = {}
    stack = [root]

    while stack:
        node = stack.pop()
        if node is None or node.is_terminal():
            continue

        player = node.player
        if player is None:
            continue

        if player not in info_sets:
            info_sets[player] = {}

        info_id = node.info_set
        if info_id is None:
            info_id = f"auto_{player}_{id(node)}"
            node.info_set = info_id

        if info_id in info_sets[player]:
            if info_sets[player][info_id] != node.actions:
                raise ValueError(f"Inconsistent actions in info set {info_id} for {player}")
        else:
            info_sets[player][info_id] = list(node.actions)

        #push children to complete iteration over stack
        for child in node.children.values():
            stack.append(child)

    return info_sets
    
def enumerate_player_strategies(info_set_for_player):
    info_ids = list(info_set_for_player.keys())
    action_lists = [info_set_for_player[iid] for iid in info_ids]
    strategies = []
    for str in product(*action_lists):
        strategies.append({iid: act for iid, act in zip(info_ids, str)})
    return strategies, info_ids

def evaluate_profile(root, profile):
    node = root
    while not node.is_terminal():
        p = node.player
        info_id = node.info_set if node.info_set is not None else f"node {id(node)}"
        action = profile[p][info_id]
        node = node.children[action]
    return node.payoffs

def extensive_to_normal_form(root, players):
    info_sets = collect_info_sets(root)

    strategies = {}
    for player in players:
        strategies[player], _ = enumerate_player_strategies(info_sets[player])

    player_strategies = [strategies[p] for p in players]
    strategy_profiles = list(product(*player_strategies))

    #Evaluate payoffs
    payoff_matrix = []
    for profile_tuple in strategy_profiles:
        profile = {player: strat for player, strat in zip(players, profile_tuple)}
        payoff_matrix.append(evaluate_profile(root, profile))

    return { 
        # The function returns a dictionary like the following: 
        # {'strategies': [({'P1_main': 'Cooperate'}, {'P2_main': 'Cooperate'}), 
        # ({'P1_main': 'Cooperate'}, {'P2_main': 'Defect'}),
        #  ({'P1_main': 'Defect'}, {'P2_main': 'Cooperate'}), 
        #  ({'P1_main': 'Defect'}, {'P2_main': 'Defect'})], 
        #  'payoff_matrix': [(3, 3), (0, 5), (5, 0), (1, 1)]}
        # the 'strategies' list contains tuples of dictionaries representing each player’s actions at their respective info sets (P1_main and P2_main),
        #  and 'payoff_matrix' contains the corresponding payoff tuples.
        
    "strategies": strategy_profiles,   
    "payoff_matrix": payoff_matrix  # matrix of payoffs for all strategy profiles
}


def compute_expected_payoff(payoff_matrix, mixed_p1, mixed_p2):
    """
    Function to calculate the payoff given probabilities of P1 & P2

    :param payoff_matrix: list of payoff tuples [(p1_payoff, p2_payoff), ...]
    :param mixed_p1:  list of probabilities over Player 1’s strategies
    :param mixed_p2: list of probabilities over Player 2’s strategies

    Returns: (expected_p1, expected_p2)
    """
    # Convert to numpy
    mixed_p1 = np.array(mixed_p1)
    mixed_p2 = np.array(mixed_p2)

    # Expected payoff is a double sum:
    # sum_i sum_j [ p1[i] * p2[j] * payoff(i,j) ]

    expected_p1 = 0.0
    expected_p2 = 0.0

    index = 0
    for i in range(len(mixed_p1)):
        for j in range(len(mixed_p2)):
            p = mixed_p1[i] * mixed_p2[j]
            p1_pay, p2_pay = payoff_matrix[index]

            expected_p1 += p * p1_pay
            expected_p2 += p * p2_pay

            index += 1

    return expected_p1, expected_p2    

def get_mixed_probs(root, result):
    # get set of unique actions for each player
    info_sets = collect_info_sets(root)
    # define dict to store probabilities for each player
    # {"Player 1: [prob1, prob2],..."}
    probs = {}

    # loop through each player's info set
    for player, actions in info_sets.items():
        print(f"Enter Probabilities for {player}")
        probs[player] = []

        action_key = f"P{player[-1]}_main"

        a=0  # while loop iterator
        while a < len(actions[action_key]):
            prob = float(input(f"Prob of Strategy {a+1}: "))

            if prob<0 or prob>1:
                print("Error! Enter a probability between 1 and 0")
                continue  # no increment, we'll retry the same idx a

            probs[player].append(prob)

            # validate sum = 1
            if len(probs[player]) == len(actions[action_key]):
                if sum(probs[player]) != 1:
                    print("Try again and Make sure your probabilities for each player sum up to 1")
                    a=0  # restart from the beginning
                    probs[player] = []  # reset probabilities for that player
                    continue

            a+=1  # increment iter
    
    if len(probs)==2:
        # extract P1 and P2 probabilities
        p1 = probs["Player 1"]
        p2 = probs["Player 2"]

        exp1, exp2 = compute_expected_payoff(
            result['payoff_matrix'],
            p1, p2
        )
        print("Mixed strategy for P1:\n", p1)
        print("Mixed strategy for P2:\n", p2)
        print("Expected Payoffs under mixed strategies:", (exp1, exp2))
