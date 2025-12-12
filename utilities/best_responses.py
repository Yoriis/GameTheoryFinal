def compute_best_responses(strategies, payoff_matrix, players=["Player 1", "Player 2"]):
    """
    Returns a dictionary of best responses for each player.
    
    Example result:
    {
      "Player 1": {"Cooperate": ["Cooperate", "Defect"]},
      "Player 2": {"Defect": ["Cooperate"]},
    }
    """
    best_responses = {players[0]: {}, players[1]: {}}
    
    # Separate players payoffs
    # For Player 1: all payoffs against each P2 action
    # For Player 2: all payoffs against each P1 action
    p1_payoffs = {}
    p2_payoffs = {}
    
    for (strat, payoff) in zip(strategies, payoff_matrix):
        a1 = strat[0][list(strat[0].keys())[0]] # player 1's actions
        a2 = strat[1][list(strat[1].keys())[0]] # player 2's actions
        
        if a2 not in p1_payoffs:
            p1_payoffs[a2] = []
        if a1 not in p2_payoffs:
            p2_payoffs[a1] = []
        
        # This groups payoffs based on opponent action
        p1_payoffs[a2].append((payoff[0], a1))  # (P1 payoff, P1 action)
        p2_payoffs[a1].append((payoff[1], a2))  # (P2 payoff, P2 action)
    
    # Calculate best responses
    # Finds the maximum payoff
    # Returns all actions that achieve that maximum (in case of ties)
    for opp_action, vals in p1_payoffs.items():
        max_p1 = max(vals)[0]
        best_responses[players[0]][opp_action] = [a for p,a in vals if p == max_p1]
    
    for opp_action, vals in p2_payoffs.items():
        max_p2 = max(vals)[0]
        best_responses[players[1]][opp_action] = [a for p,a in vals if p == max_p2]
    
    return best_responses