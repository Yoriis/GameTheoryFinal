from Models.ExtensiveForm import ExtensiveFormNode

PLAYERS = ["Player 1", "Player 2"]

# Prisoner's Dilemma
def build_pd_tree():
    #Actions
    C, D = "Cooperate" , "Defect"
    root = ExtensiveFormNode(player="Player 1", actions=[C, D], info_set="P1_main")

    for a1 in [C, D]:
        p2 = ExtensiveFormNode(player="Player 2", actions=[C, D], info_set="P2_main")
        root.children[a1] = p2

        for a2 in [C, D]:
            if (a1, a2) == (C, C):
                payoff = (3, 3)
            elif (a1, a2) == (C, D):
                payoff = (0, 5)
            elif (a1, a2) == (D, C):
                payoff = (5, 0)
            else:
                payoff = (1, 1)
            p2.children[a2] = ExtensiveFormNode(payoffs=payoff)
    
    return root

# BATTLE OF SEXES
def build_bos_tree():
    O, F = "Opera", "Football"
    root = ExtensiveFormNode(player="Player 1", actions=[O, F], info_set="P1_main")

    for a1 in [O, F]:
        p2 = ExtensiveFormNode(player="Player 2", actions=[O, F], info_set="P2_main")
        root.children[a1] = p2

        for a2 in [O, F]:
            if (a1, a2) == (O, O):
                payoff = (2, 1)
            elif (a1, a2) == (O, F):
                payoff = (0, 0)
            elif (a1, a2) == (F, O):
                payoff = (0, 0)
            else:
                payoff = (1, 2)
            p2.children[a2] = ExtensiveFormNode(payoffs=payoff)
    
    return root

# matching pennies
def build_mp_tree():
    H, T = "Heads", "Tails"
    root = ExtensiveFormNode(player="Player 1", actions=[H, T], info_set="P1_main")

    for a1 in [H, T]:
        p2 = ExtensiveFormNode(player="Player 2", actions=[H, T], info_set="P2_main")
        root.children[a1] = p2

        for a2 in [H, T]:
            if a1 == a2:
                payoff = (1, -1)
            else:
                payoff = (-1, 1)
            p2.children[a2] = ExtensiveFormNode(payoffs=payoff)
    
    return root

# hawk-dove
def build_hawk_dove_tree():
    H, D = "Hawk", "Dove"
    root = ExtensiveFormNode(player="Player 1", actions=[H, D], info_set="P1_main")

    for a1 in [H, D]:
        p2 = ExtensiveFormNode(player="Player 2", actions=[H, D], info_set="P2_main")
        root.children[a1] = p2

        for a2 in [H, D]:
            if (a1, a2) == (H, H):
                payoff = (-1, -1)
            elif (a1, a2) == (H, D):
                payoff = (3, 0)
            elif (a1, a2) == (D, H):
                payoff = (0, 3)
            else:
                payoff = (2, 2)
            p2.children[a2] = ExtensiveFormNode(payoffs=payoff)
    
    return root


# User-defined game
def build_custom_game():
    print("\n--- Create Your Own 2-Player Game ---")
    print("Enter actions for each player (comma separated):")
    
    p1_actions = input("Player 1 actions: ").strip().split(",")
    p2_actions = input("Player 2 actions: ").strip().split(",")
    
    p1_actions = [a.strip() for a in p1_actions]
    p2_actions = [a.strip() for a in p2_actions]
    
    # This sets up Player 1's decision node.
    root = ExtensiveFormNode(player="Player 1", actions=p1_actions, info_set="P1_custom")
    
    # Ask payoff for each strategy profile
    for a1 in p1_actions:
        p2 = ExtensiveFormNode(player="Player 2", actions=p2_actions, info_set="P2_custom")
        root.children[a1] = p2
        
        for a2 in p2_actions:
            print(f"\nEnter payoffs for profile: ({a1}, {a2})")
            
            p1 = int(input("  Payoff Player 1: "))
            p2p = int(input("  Payoff Player 2: "))
            
            payoff = (p1, p2p)
            p2.children[a2] = ExtensiveFormNode(payoffs=payoff)
    
    print("\nCustom game created successfully!")
    return root


GAMES = {
    "Prisoner's Dilemma": build_pd_tree,
    "Battle of the Sexes": build_bos_tree,
    "Matching Pennies": build_mp_tree,
    "Hawk-Dove Game": build_hawk_dove_tree,
    "Custom Game": build_custom_game
}

