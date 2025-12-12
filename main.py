from games import GAMES, PLAYERS
from Models.NormalForm import extensive_to_normal_form, get_mixed_probs
from utilities.visualization import print_tree, print_normal_form
from utilities.nash_equilibrium import pure_nash
from utilities.dominance import get_strict_dominance, get_weak_dominance, rationalizability_2x2
from utilities.best_responses import compute_best_responses
import os
from gui import run

def menu():
    names = list(GAMES.keys())
    os.makedirs("output", exist_ok=True)

    while True:
        print("\n=== Game Theory Simulator (Extensive -> Normal) ===")
        for i, name in enumerate(names, 1):
            print(f"{i}. {name}")
        print("Q. Quit")

        choice = input("Choose a game: ").strip()
        if choice.lower() == "q":
            print("GoodBye")
            break
    

        game_name = names[int(choice) - 1]
        root = GAMES[game_name]()
        print(f"\n-- {game_name} (Extensive Form) ---")
        print_tree(root)
        print(extensive_to_normal_form(root, PLAYERS))


        # Normal form
        result = extensive_to_normal_form(root, PLAYERS)
        print_normal_form(result["strategies"], result["payoff_matrix"], PLAYERS)
        
        # Best responses
        best = compute_best_responses(result["strategies"], result["payoff_matrix"], PLAYERS)
        print("Best Responses:", best)

        # Dominance
        print("\n=== Dominance Analysis ===")
        strict_dom = get_strict_dominance(result["strategies"], result["payoff_matrix"], PLAYERS)
        print("Strictly Dominated Strategies:", strict_dom)
        weak_dom = get_weak_dominance(result["strategies"], result["payoff_matrix"], PLAYERS)
        print("Weakly Dominated Strategies:", weak_dom)

        # rationalizability
        print("\n=== Rationalizability (2x2) ===")
        rat = rationalizability_2x2(result["strategies"], result["payoff_matrix"])
        print("Rationalizable strategies:")
        print_normal_form(rat["rationalizable_strategies"], rat["rationalizable_payoffs"], PLAYERS)


        # calculate payoff of mixed strtegies
        while True:
            print("==Analyze Mixed Strategies==")
            choice = input("Analyze a new strategy or press Q to quit: ").strip()
            if choice.lower() == "q":
                print("Exiting...")
                break
            get_mixed_probs(root, result)
        

if __name__ == "__main__":
    run()