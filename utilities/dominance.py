import numpy as np
from itertools import product
from Models.NormalForm import compute_expected_payoff
from utilities.best_responses import compute_best_responses

def get_strict_dominance(strategies, payoff_matrix, players=["Player 1", "Player 2"]):
    dominated_strategies = {players[0]: set(), players[1]: set()}
    player1_strategies = []
    player2_strategies = []
    for (strat, payoff) in zip(strategies, payoff_matrix):
        a1 = list(strat[0].values())[0]
        a2 = list(strat[1].values())[0]
        if a1 not in player1_strategies:
            player1_strategies.append(a1)
        if a2 not in player2_strategies:
            player2_strategies.append(a2)
    
    # payoff lookup -> helpful for comparisons
    payoff_lookup = {}
    for strat, payoff in zip(strategies, payoff_matrix):
        a1 = list(strat[0].values())[0]
        a2 = list(strat[1].values())[0]
        payoff_lookup[(a1, a2)] = payoff
    #player 1
    for i in range(len(player1_strategies)):
        for j in range(len(player1_strategies)):
            #to ensure no strategy is compared to itself
            if i != j:
                payoffs_i = []
                payoffs_j = []
                for p2_strat in player2_strategies:
                    #to compare each 2 strategies together, index zero to get player 1's payoff
                    payoffs_i.append(payoff_lookup[(player1_strategies[i], p2_strat)][0])
                    payoffs_j.append(payoff_lookup[(player1_strategies[j], p2_strat)][0])
                if all(payoffs_i[k] > payoffs_j[k] for k in range(len(payoffs_i))):
                    dominated_strategies[players[0]].add(player1_strategies[j])
    #player 2
    for  i in range(len(player2_strategies)):
        for j in range(len(player2_strategies)):
            if i != j:
                payoffs_i = []
                payoffs_j = []
                for p1_strat in player1_strategies:
                    payoffs_i.append(payoff_lookup[(p1_strat, player2_strategies[i])][1])
                    payoffs_j.append(payoff_lookup[(p1_strat, player2_strategies[j])][1])
                
                if all(payoffs_i[k] > payoffs_j[k] for k in range(len(payoffs_i))):
                    dominated_strategies[players[1]].add(player2_strategies[j])
    
    return dominated_strategies


def get_weak_dominance(strategies, payoff_matrix, players=["Player 1", "Player 2"]):
    dominated_strategies = {players[0]: set(), players[1]: set()}
    player1_strategies = []
    player2_strategies = []
    for (strat, payoff) in zip(strategies, payoff_matrix):
        a1 = list(strat[0].values())[0]
        a2 = list(strat[1].values())[0]
        if a1 not in player1_strategies:
            player1_strategies.append(a1)
        if a2 not in player2_strategies:
            player2_strategies.append(a2)
    
    payoff_lookup = {}
    for strat, payoff in zip(strategies, payoff_matrix):
        a1 = list(strat[0].values())[0]
        a2 = list(strat[1].values())[0]
        payoff_lookup[(a1, a2)] = payoff
    #player 1
    for i in range(len(player1_strategies)):
        for j in range(len(player1_strategies)):
            if i != j:
                payoffs_i = []
                payoffs_j = []
                for p2_strat in player2_strategies:
                    payoffs_i.append(payoff_lookup[(player1_strategies[i], p2_strat)][0])
                    payoffs_j.append(payoff_lookup[(player1_strategies[j], p2_strat)][0])
                #only change is how we now accept equal payoffs as dominance    
                if all(payoffs_i[k] >= payoffs_j[k] for k in range(len(payoffs_i))):
                    dominated_strategies[players[0]].add(player1_strategies[j])
    #player 2
    for  i in range(len(player2_strategies)):
        for j in range(len(player2_strategies)):
            if i != j:
                payoffs_i = []
                payoffs_j = []
                for p1_strat in player1_strategies:
                    payoffs_i.append(payoff_lookup[(p1_strat, player2_strategies[i])][1])
                    payoffs_j.append(payoff_lookup[(p1_strat, player2_strategies[j])][1])
                
                if all(payoffs_i[k] >= payoffs_j[k] for k in range(len(payoffs_i))):
                    dominated_strategies[players[1]].add(player2_strategies[j])
    
    return dominated_strategies


def mixed_strategy_dominance_3x3(strategies, payoff_matrix, players=["Player 1", "Player 2"]):
    dominated_strategies = {players[0]: set(), players[1]: set()}
    epsilon = 1e-6

    player1_strategies = []
    player2_strategies = []
    for (strat, payoff) in zip(strategies, payoff_matrix):
        a1 = list(strat[0].values())[0]
        a2 = list(strat[1].values())[0]
        if a1 not in player1_strategies:
            player1_strategies.append(a1)
        if a2 not in player2_strategies:
            player2_strategies.append(a2)

    # PLAYER 1
    if len(player1_strategies) >= 3:
        # first we test if C is dominated by both A and B
        #we test multiple values of p to get the correct mixed strategy
        for p_val in np.arange(0.01, 1, 0.01):
            m1 = [p_val, 1-p_val, 0]

            c1, _ = compute_expected_payoff(payoff_matrix, [0,0,1], [1,0,0])
            c2, _ = compute_expected_payoff(payoff_matrix, [0,0,1], [0,1,0])
            c3, _ = compute_expected_payoff(payoff_matrix, [0,0,1], [0,0,1])
            u1, _ = compute_expected_payoff(payoff_matrix, m1, [1,0,0])
            u2, _ = compute_expected_payoff(payoff_matrix, m1, [0,1,0])
            u3, _ = compute_expected_payoff(payoff_matrix, m1, [0,0,1])
            #the epsilon to ensure that no equal values enter the condition
            if (u1 > c1 + epsilon and u2 > c2 + epsilon and u3 > c3 + epsilon):
                print(f"{player1_strategies[2]} is dominated by the mixed strategy: {m1} (p={p_val:.4f})")
                dominated_strategies[players[0]].add(player1_strategies[2])
                break

        # to test if B is dominated by both A and C
        for p_val in np.arange(0.01, 1, 0.01):
            m1 = [p_val, 0, 1-p_val]

            c1, _ = compute_expected_payoff(payoff_matrix, [0,1,0], [1,0,0])
            c2, _ = compute_expected_payoff(payoff_matrix, [0,1,0], [0,1,0])
            c3, _ = compute_expected_payoff(payoff_matrix, [0,1,0], [0,0,1])
            u1, _ = compute_expected_payoff(payoff_matrix, m1, [1,0,0])
            u2, _ = compute_expected_payoff(payoff_matrix, m1, [0,1,0])
            u3, _ = compute_expected_payoff(payoff_matrix, m1, [0,0,1])

            if (u1 > c1 + epsilon and u2 > c2 + epsilon and u3 > c3 + epsilon):
                print(f"{player1_strategies[1]} is dominated by the mixed strategy: {m1} (p={p_val:.4f})")
                dominated_strategies[players[0]].add(player1_strategies[1])
                break

        # to test if A is dominated by mixing B and C
        for p_val in np.arange(0.01, 1, 0.01):
            m1 = [0, p_val, 1-p_val]

            c1, _ = compute_expected_payoff(payoff_matrix, [1,0,0], [1,0,0])
            c2, _ = compute_expected_payoff(payoff_matrix, [1,0,0], [0,1,0])
            c3, _ = compute_expected_payoff(payoff_matrix, [1,0,0], [0,0,1])
            u1, _ = compute_expected_payoff(payoff_matrix, m1, [1,0,0])
            u2, _ = compute_expected_payoff(payoff_matrix, m1, [0,1,0])
            u3, _ = compute_expected_payoff(payoff_matrix, m1, [0,0,1])

            if (u1 > c1 + epsilon and u2 > c2 + epsilon and u3 > c3 + epsilon):
                print(f"{player1_strategies[0]} is dominated by the mixed strategy: {m1} (p={p_val:.4f})")
                dominated_strategies[players[0]].add(player1_strategies[0])
                break

    # PLAYER 2
    if len(player2_strategies) >= 3:
        for p_val in np.arange(0.01, 1, 0.01):
            m1 = [p_val, 1-p_val, 0]

            _, c1 = compute_expected_payoff(payoff_matrix, [1,0,0], [0,0,1])
            _, c2 = compute_expected_payoff(payoff_matrix, [0,1,0], [0,0,1])
            _, c3 = compute_expected_payoff(payoff_matrix, [0,0,1], [0,0,1])
            _, u1 = compute_expected_payoff(payoff_matrix, [1,0,0], m1)
            _, u2 = compute_expected_payoff(payoff_matrix, [0,1,0], m1)
            _, u3 = compute_expected_payoff(payoff_matrix, [0,0,1], m1)

            if (u1 > c1 + epsilon and u2 > c2 + epsilon and u3 > c3 + epsilon):
                print(f"{player2_strategies[2]} is dominated by the mixed strategy: {m1} (p={p_val:.4f})")
                dominated_strategies[players[1]].add(player2_strategies[2])
                break

    return dominated_strategies

#In this case, we could only get a mixed strategy for the player with 3 strategies, as there is no such thing as as mixed strategy for 2 strategies
def mixed_strategy_dominance_3x2(strategies, payoff_matrix, players=["Player 1", "Player 2"]):
    dominated_strategies = {players[0]: set(), players[1]: set()}
    epsilon = 1e-6

    player1_strategies = []
    player2_strategies = []
    for (strat, payoff) in zip(strategies, payoff_matrix):
        a1 = list(strat[0].values())[0]
        a2 = list(strat[1].values())[0]
        if a1 not in player1_strategies:
            player1_strategies.append(a1)
        if a2 not in player2_strategies:
            player2_strategies.append(a2)

    # PLAYER 1
    if len(player1_strategies) >= 3:
        for p_val in np.arange(0.01, 1, 0.01):
            m1 = [p_val, 1-p_val, 0]
            c1, _ = compute_expected_payoff(payoff_matrix, [0,0,1], [1,0])
            c2, _ = compute_expected_payoff(payoff_matrix, [0,0,1], [0,1])

            u1, _ = compute_expected_payoff(payoff_matrix, m1, [1,0])
            u2, _ = compute_expected_payoff(payoff_matrix, m1, [0,1])

            if (u1 > c1 + epsilon and u2 > c2 + epsilon):
                print(f"{player1_strategies[2]} is dominated by the mixed strategy: {m1} (p={p_val:.4f})")
                dominated_strategies[players[0]].add(player1_strategies[2])
                break

        for p_val in np.arange(0.01, 1, 0.01):
            m2 = [p_val, 0, 1-p_val]
            b1, _ = compute_expected_payoff(payoff_matrix, [0,1,0], [1,0])
            b2, _ = compute_expected_payoff(payoff_matrix, [0,1,0], [0,1])

            u1, _ = compute_expected_payoff(payoff_matrix, m2, [1,0])
            u2, _ = compute_expected_payoff(payoff_matrix, m2, [0,1])

            if (u1 > b1 + epsilon and u2 > b2 + epsilon):
                print(f"{player1_strategies[1]} is dominated by the mixed strategy: {m2} (p={p_val:.4f})")
                dominated_strategies[players[0]].add(player1_strategies[1])
                break

        for p_val in np.arange(0.01, 1, 0.01):
            m3 = [0, p_val, 1-p_val]
            a1, _ = compute_expected_payoff(payoff_matrix, [1,0,0], [1,0])
            a2, _ = compute_expected_payoff(payoff_matrix, [1,0,0], [0,1])

            u1, _ = compute_expected_payoff(payoff_matrix, m3, [1,0])
            u2, _ = compute_expected_payoff(payoff_matrix, m3, [0,1])

            if (u1 > a1 + epsilon and u2 > a2 + epsilon):
                print(f"{player1_strategies[0]} is dominated by the mixed strategy: {m3} (p={p_val:.4f})")
                dominated_strategies[players[0]].add(player1_strategies[0])
                break

    # PLAYER 2
    if len(player2_strategies) >= 3:
        for p_val in np.arange(0.01, 1, 0.01):
            m1 = [p_val, 1-p_val, 0]
            _, c1 = compute_expected_payoff(payoff_matrix, [1,0], [0,0,1])
            _, c2 = compute_expected_payoff(payoff_matrix, [0,1], [0,0,1])

            _, u1 = compute_expected_payoff(payoff_matrix, [1,0], m1)
            _, u2 = compute_expected_payoff(payoff_matrix, [0,1], m1)

            if (u1 > c1 + epsilon and u2 > c2 + epsilon):
                print(f"{player2_strategies[2]} is dominated by the mixed strategy: {m1} (p={p_val:.4f})")
                dominated_strategies[players[1]].add(player2_strategies[2])
                break

        for p_val in np.arange(0.01, 1, 0.01):
            m2 = [p_val, 0, 1-p_val]
            _, b1 = compute_expected_payoff(payoff_matrix, [1,0], [0,1,0])
            _, b2 = compute_expected_payoff(payoff_matrix, [0,1], [0,1,0])

            _, u1 = compute_expected_payoff(payoff_matrix, [1,0], m2)
            _, u2 = compute_expected_payoff(payoff_matrix, [0,1], m2)

            if (u1 > b1 + epsilon and u2 > b2 + epsilon):
                print(f"{player2_strategies[1]} is dominated by the mixed strategy: {m2} (p={p_val:.4f})")
                dominated_strategies[players[1]].add(player2_strategies[1])
                break

        for p_val in np.arange(0.01, 1, 0.01):
            m3 = [0, p_val, 1-p_val]
            _, a1 = compute_expected_payoff(payoff_matrix, [1,0], [1,0,0])
            _, a2 = compute_expected_payoff(payoff_matrix, [0,1], [1,0,0])

            _, u1 = compute_expected_payoff(payoff_matrix, [1,0], m3)
            _, u2 = compute_expected_payoff(payoff_matrix, [0,1], m3)

            if (u1 > a1 + epsilon and u2 > a2 + epsilon):
                print(f"{player2_strategies[0]} is dominated by the mixed strategy: {m3} (p={p_val:.4f})")
                dominated_strategies[players[1]].add(player2_strategies[0])
                break

    return dominated_strategies



def rationalizability_2x2(strategies, payoff_matrix):
    """
    Iterated elimination of never-best responses for a 2x2 game.
    Uses the existing:
        - compute_best_responses()
    """

    remaining = strategies.copy()
    remaining_payoffs = payoff_matrix.copy()

    changed = True
    iteration = 1

    while changed:
        changed = False
        print(f"\n=== ITERATION {iteration} ===")

        # 1. Compute best responses on the CURRENT strategy set
        best_res = compute_best_responses(remaining, remaining_payoffs)

        # Collect current actions
        p1_actions = set([s[0]['P1_main'] for s in remaining])
        p2_actions = set([s[1]['P2_main'] for s in remaining])

        # 2. Find which actions are not best responses (dominated) and validate it's not empty
        never_br_p1 = {a for a in p1_actions if a not in sum(best_res["Player 1"].values(), [])}
        never_br_p2 = {a for a in p2_actions if a not in sum(best_res["Player 2"].values(), [])}

        # If none removed → stable
        if not never_br_p1 and not never_br_p2:
            print("No more deletions → rationalizable set reached.")
            break

        # 3. Filter out deleted strategies
        new_remaining = []
        new_payoffs = []
        for strat, payoff in zip(remaining, remaining_payoffs):
            a1 = strat[0]['P1_main']
            a2 = strat[1]['P2_main']
            if a1 not in never_br_p1 and a2 not in never_br_p2:
                new_remaining.append(strat)
                new_payoffs.append(payoff)

        print("Removed P1:", never_br_p1)
        print("Removed P2:", never_br_p2)

        changed = True
        remaining = new_remaining
        remaining_payoffs = new_payoffs
        iteration += 1

    return {
        "rationalizable_strategies": remaining,
        "rationalizable_payoffs": remaining_payoffs
    }

