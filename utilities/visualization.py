import csv
import os
import math
from textwrap import shorten


def print_tree(node, indent=0):
    if node.is_terminal():
        print(" " * indent +f"Terminal: Payoffs {node.payoffs}")
        return
    print(" " * indent + f"{node.player}'s turn | Actions: {node.actions}")
    for action, child in node.children.items():
        print(" " * (indent + 2) + f"Action: {action}")
        print_tree(child, indent + 4)


# Display Normal form
def print_normal_form(strategies, payoff_matrix, players=["Player 1", "Player 2"]):
    """
    Display the Normal Form payoff matrix in a clean tabular format.

    Args:
        strategies: A list of tuples where each tuple contains a strategy dict for each player
        payoff_matrix: A list of payoff tuples corresponding to each strategy profile
        players: List of player names (default: P1 and P2)
    """

    print("\n=== Normal Form Representation ===")

    # Extract player strategies as simple action names
    p1_actions = sorted(set(s[0][list(s[0].keys())[0]] for s in strategies))
    p2_actions = sorted(set(s[1][list(s[1].keys())[0]] for s in strategies))

    # Create a mapping to fill the matrix
    # Creates an empty table (will later store the payoff values)
    table = {a1: {a2: None for a2 in p2_actions} for a1 in p1_actions}

    # fill the payoff matrix
    for (strat, payoff) in zip(strategies, payoff_matrix):
        a1 = strat[0][list(strat[0].keys())[0]]  # Player 1 action
        a2 = strat[1][list(strat[1].keys())[0]]  # Player 2 action
        table[a1][a2] = payoff

    # Print Player 2 header
    print(f"\n             {players[1]}")
    print("         " + "   ".join(f"{a2:^10}" for a2 in p2_actions))

    # Print matrix rows for Player 1
    for a1 in p1_actions:
        row = f"{players[0][0]}: {a1:<6} "
        for a2 in p2_actions:
            payoff = table[a1][a2]
            cell = f"{payoff}"
            row += f"{cell:^12}"
        print(row)

    print("\n")

