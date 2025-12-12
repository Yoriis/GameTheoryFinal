from .best_responses import compute_best_responses

def pure_nash(players, strategies, payoff_matrix):
    equilibria = []
    best_resps = compute_best_responses(strategies, payoff_matrix, players)

    for strat, payoffs in zip(strategies, payoff_matrix):
        a1 = strat[0][list(strat[0].keys())[0]] # player 1's actions
        a2 = strat[1][list(strat[1].keys())[0]] # player 2's actions

        if a1 in best_resps[players[0]][a2] and a2 in best_resps[players[1]][a1]:
            equilibria.append((strat, payoffs))

    print("Pure Strategy Nash Equilibria:" )
    for eq in equilibria:
        print(f"  {eq[0]} -> {eq[1]}")

    return equilibria