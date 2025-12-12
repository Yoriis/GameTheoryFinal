import streamlit as st
import numpy as np
from graphviz import Digraph

from games import GAMES, PLAYERS
from Models.NormalForm import extensive_to_normal_form, get_mixed_probs, compute_expected_payoff
from utilities.visualization import print_tree, print_normal_form
from utilities.nash_equilibrium import pure_nash
from utilities.dominance import get_strict_dominance, get_weak_dominance, mixed_strategy_dominance_3x3, mixed_strategy_dominance_3x2
from utilities.best_responses import compute_best_responses

st.markdown("""
<style>
/* Darker header for the normal form table */
thead tr th {
    background-color: #2b2b2b !important;
    color: white !important;
    font-weight: 700 !important;
}
tbody tr td {
    color: #000 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
div.stButton > button {
    cursor: pointer !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Force pointer cursor on selectbox dropdowns */
div.stSelectbox > div[role="combobox"] {
    cursor: pointer !important;
}
</style>
""", unsafe_allow_html=True)



st.set_page_config(page_title="Game Theory Analyzer", layout="wide")

# Initialize session state
if 'game_selected' not in st.session_state:
    st.session_state.game_selected = None
if 'game_tree' not in st.session_state:
    st.session_state.game_tree = None
if 'normal_form' not in st.session_state:
    st.session_state.normal_form = None
if 'custom_game_ready' not in st.session_state:
    st.session_state.custom_game_ready = False

def display_payoff_table(strategies, payoff_matrix, p1_actions, p2_actions):
    """Display payoff matrix as a styled HTML table"""
    table_data = {}
    for (strat, payoff) in zip(strategies, payoff_matrix):
        a1 = list(strat[0].values())[0]
        a2 = list(strat[1].values())[0]
        if a1 not in table_data:
            table_data[a1] = {}
        table_data[a1][a2] = f"({payoff[0]}, {payoff[1]})"
    
    # Build HTML table
    html = """
    <table style="width:100%; border-collapse: collapse; text-align: center; font-family: Arial, sans-serif;">
        <thead>
            <tr style="background-color:#2c3e50; color:white; font-weight:bold;">
                <th style="border: 1px solid #34495e; padding: 10px;">Player 1 \\ Player 2</th>
    """
    # Column headers for Player 2
    for a2 in p2_actions:
        html += f'<th style="border: 1px solid #34495e; padding: 10px;">{a2}</th>'
    html += "</tr></thead><tbody>"

    # Data rows
    for idx, a1 in enumerate(p1_actions):
        row_color = "#ecf0f1" if idx % 2 == 0 else "#ffffff"  # alternating row colors
        html += f'<tr style="background-color:{row_color};">'
        html += f'<td style="border: 1px solid #bdc3c7; padding: 10px; font-weight:bold;">{a1}</td>'
        for a2 in p2_actions:
            html += f'<td style="border: 1px solid #bdc3c7; padding: 10px;">{table_data[a1][a2]}</td>'
        html += "</tr>"

    html += "</tbody></table>"
    return html

def draw_extensive_form(node, dot=None, parent_id=None):
    """Recursive function to create Graphviz diagram for extensive form"""
    if dot is None:
        dot = Digraph(format="png")
        dot.attr('node', shape='circle', fontsize='12', fontname='Arial')

    node_id = str(id(node))
    if node.is_terminal():
        label = f"{node.payoffs}"
        dot.node(node_id, label=label, shape='box', style='filled', fillcolor='#d5f4e6')
    else:
        label = f"{node.player}"
        dot.node(node_id, label=label, shape='circle', style='filled', fillcolor='#f9d5e5')

    if parent_id is not None:
        dot.edge(parent_id, node_id, label=getattr(node, 'action_from_parent', ''))

    for action, child in node.children.items():
        child.action_from_parent = str(action)
        draw_extensive_form(child, dot, node_id)

    return dot



st.title("Game Theory Analyzer")
st.markdown("Analyze game theory: extensive and normal forms, dominance, best responses, mixed strategies, and Nash equilibria.")

# Sidebar for game selection
with st.sidebar:
    st.header("Game Selection")
    game_choice = st.selectbox(
        "Choose a game:",
        ["Select a game...", "Prisoner's Dilemma", "Battle of the Sexes", 
         "Matching Pennies", "Hawk-Dove Game", "Custom Game"]
    )
    
    if game_choice != "Select a game...":
        if st.button("Load Game", type="primary"):
            if game_choice == "Custom Game":
                st.session_state.game_selected = game_choice
                st.session_state.custom_game_ready = False
            else:
                st.session_state.game_selected = game_choice
                st.session_state.game_tree = GAMES[game_choice]()
                st.session_state.normal_form = None
                st.success(f"✓ {game_choice} loaded!")

# Custom game input
if st.session_state.game_selected == "Custom Game" and not st.session_state.custom_game_ready:
    st.header("Create Custom Game")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Player 1 Actions")
        p1_actions_input = st.text_input("Enter actions (comma-separated):", "Action1, Action2", key="p1_actions")
        p1_actions = [a.strip() for a in p1_actions_input.split(",") if a.strip()]

    with col2:
        st.subheader("Player 2 Actions")
        p2_actions_input = st.text_input("Enter actions (comma-separated):", "Action1, Action2", key="p2_actions")
        p2_actions = [a.strip() for a in p2_actions_input.split(",") if a.strip()]

    if len(p1_actions) > 0 and len(p2_actions) > 0:
        st.subheader("Payoff Matrix")
        st.markdown("Enter payoffs for each strategy profile (Player 1, Player 2):")
        payoffs_dict = {}

        for i, a1 in enumerate(p1_actions):
            cols = st.columns(len(p2_actions))
            for j, a2 in enumerate(p2_actions):
                with cols[j]:
                    st.caption(f"({a1}, {a2})")
                    p1_pay = st.number_input(f"P1 payoff", key=f"p1_{i}_{j}", value=0)
                    p2_pay = st.number_input(f"P2 payoff", key=f"p2_{i}_{j}", value=0)
                    payoffs_dict[(a1, a2)] = (p1_pay, p2_pay)
        
        if st.button("Create Game", type="primary"):
            from Models.ExtensiveForm import ExtensiveFormNode
            root = ExtensiveFormNode(player="Player 1", actions=p1_actions, info_set="P1_custom")
            for a1 in p1_actions:
                p2_node = ExtensiveFormNode(player="Player 2", actions=p2_actions, info_set="P2_custom")
                root.children[a1] = p2_node
                for a2 in p2_actions:
                    payoff = payoffs_dict[(a1, a2)]
                    p2_node.children[a2] = ExtensiveFormNode(payoffs=payoff)
            st.session_state.game_tree = root
            st.session_state.custom_game_ready = True
            st.session_state.normal_form = None
            st.success("Custom game created!")
            st.rerun()


# Main content area
if st.session_state.game_tree is not None:
    st.header(f"Analysis: {st.session_state.game_selected}")
    
    # Show Extensive Form Tree
    st.subheader("Extensive Form Tree")
    dot = draw_extensive_form(st.session_state.game_tree)
    st.graphviz_chart(dot)


    # Convert to Normal Form button
    if st.session_state.normal_form is None:
        if st.button("Convert to Normal Form", type="primary"):
            st.session_state.normal_form = extensive_to_normal_form(
                st.session_state.game_tree, 
                PLAYERS
            )
            st.rerun()
    
    # Display Normal Form
    if st.session_state.normal_form:
        strategies = st.session_state.normal_form['strategies']
        payoff_matrix = st.session_state.normal_form['payoff_matrix']
        
        # Extract actions
        p1_actions = sorted(set(s[0][list(s[0].keys())[0]] for s in strategies))
        p2_actions = sorted(set(s[1][list(s[1].keys())[0]] for s in strategies))
        
        st.subheader("Normal Form Representation")
        st.markdown(display_payoff_table(strategies, payoff_matrix, p1_actions, p2_actions), unsafe_allow_html=True)
        
        # Analysis tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Dominance", 
            "Best Responses", 
            "Rationalizability",
            "Nash Equilibrium",
            "Mixed Strategies"
        ])
        
        with tab1:
            st.subheader("Dominance Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Strict Dominance**")
                strict_dom = get_strict_dominance(strategies, payoff_matrix, PLAYERS)
                if any(strict_dom.values()):
                    for player, dominated in strict_dom.items():
                        if dominated:
                            st.warning(f"{player}: {', '.join(dominated)}")
                else:
                    st.success("No strictly dominated strategies")
            
            with col2:
                st.markdown("**Weak Dominance**")
                weak_dom = get_weak_dominance(strategies, payoff_matrix, PLAYERS)
                if any(weak_dom.values()):
                    for player, dominated in weak_dom.items():
                        if dominated:
                            st.info(f"{player}: {', '.join(dominated)}")
                else:
                    st.success("No weakly dominated strategies")
            
            st.markdown("**Mixed Strategy Dominance**")
            
            # Capture print output from mixed strategy functions
            import io
            import sys
            
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            if len(p1_actions) == 3 and len(p2_actions) == 3:
                mixed_dom = mixed_strategy_dominance_3x3(strategies, payoff_matrix, PLAYERS)
            elif (len(p1_actions) == 3 and len(p2_actions) == 2) or (len(p1_actions) == 2 and len(p2_actions) == 3):
                mixed_dom = mixed_strategy_dominance_3x2(strategies, payoff_matrix, PLAYERS)
            else:
                mixed_dom = {PLAYERS[0]: set(), PLAYERS[1]: set()}
            
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            if output:
                st.code(output)
            
            if any(mixed_dom.values()):
                for player, dominated in mixed_dom.items():
                    if dominated:
                        st.info(f"{player}: {', '.join(dominated)}")
            else:
                st.success("No mixed strategy dominated strategies detected")
        
        with tab2:
            st.subheader("Best Response Analysis")
            best_resp = compute_best_responses(strategies, payoff_matrix, PLAYERS)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Player 1 Best Responses**")
                for opp_action, responses in best_resp[PLAYERS[0]].items():
                    st.write(f"Against {opp_action}: **{', '.join(responses)}**")
            
            with col2:
                st.markdown("**Player 2 Best Responses**")
                for opp_action, responses in best_resp[PLAYERS[1]].items():
                    st.write(f"Against {opp_action}: **{', '.join(responses)}**")
        
        with tab3:
            st.subheader("Rationalizability")
            st.info("Rationalizable strategies are those that survive iterated elimination of strictly dominated strategies.")
            
            # Show which strategies are rationalizable (not strictly dominated)
            strict_dom = get_strict_dominance(strategies, payoff_matrix, PLAYERS)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Player 1 Rationalizable Strategies**")
                p1_rational = [a for a in p1_actions if a not in strict_dom[PLAYERS[0]]]
                for strat in p1_rational:
                    st.success(f"✓ {strat}")
            
            with col2:
                st.markdown("**Player 2 Rationalizable Strategies**")
                p2_rational = [a for a in p2_actions if a not in strict_dom[PLAYERS[1]]]
                for strat in p2_rational:
                    st.success(f"✓ {strat}")
        
        with tab4:
            st.subheader("Nash Equilibrium (Pure Strategies)")
            
            equilibria = []
            best_resp = compute_best_responses(strategies, payoff_matrix, PLAYERS)
            
            for strat, payoffs in zip(strategies, payoff_matrix):
                a1 = strat[0][list(strat[0].keys())[0]]
                a2 = strat[1][list(strat[1].keys())[0]]
                
                if a1 in best_resp[PLAYERS[0]][a2] and a2 in best_resp[PLAYERS[1]][a1]:
                    equilibria.append((a1, a2, payoffs))
            
            if equilibria:
                st.success(f"Found {len(equilibria)} Pure Strategy Nash Equilibrium/Equilibria:")
                for a1, a2, payoffs in equilibria:
                    st.markdown(f"- **({a1}, {a2})** → Payoffs: ({payoffs[0]}, {payoffs[1]})")
            else:
                st.warning("No pure strategy Nash equilibria found. Try mixed strategies!")
        
        with tab5:
            st.subheader("Mixed Strategy Calculator")
            st.markdown("Enter probability distributions for each player's strategies:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Player 1 Probabilities**")
                p1_probs = []
                for i, action in enumerate(p1_actions):
                    prob = st.number_input(
                        f"{action}", 
                        min_value=0.0, 
                        max_value=1.0, 
                        value=1.0/len(p1_actions),
                        step=0.01,
                        key=f"p1_prob_{i}"
                    )
                    p1_probs.append(prob)
                
                p1_sum = sum(p1_probs)
                if abs(p1_sum - 1.0) > 0.001:
                    st.error(f"Probabilities must sum to 1.0 (current: {p1_sum:.3f})")
            
            with col2:
                st.markdown("**Player 2 Probabilities**")
                p2_probs = []
                for i, action in enumerate(p2_actions):
                    prob = st.number_input(
                        f"{action}", 
                        min_value=0.0, 
                        max_value=1.0, 
                        value=1.0/len(p2_actions),
                        step=0.01,
                        key=f"p2_prob_{i}"
                    )
                    p2_probs.append(prob)
                
                p2_sum = sum(p2_probs)
                if abs(p2_sum - 1.0) > 0.001:
                    st.error(f"Probabilities must sum to 1.0 (current: {p2_sum:.3f})")
            
            if abs(p1_sum - 1.0) <= 0.001 and abs(p2_sum - 1.0) <= 0.001:
                if st.button("Calculate Expected Payoffs", type="primary"):
                    exp1, exp2 = compute_expected_payoff(payoff_matrix, p1_probs, p2_probs)
                    
                    st.success("Expected Payoffs:")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Player 1", f"{exp1:.3f}")
                    with col2:
                        st.metric("Player 2", f"{exp2:.3f}")

else:
    st.info("Select a game from the sidebar to begin the analysis")
    
    st.markdown("""
    ### Available Games:
    - **Prisoner's Dilemma**: Two criminals get arrested, must choose to cooperate or defect.
    - **Battle of the Sexes**: Two players want to go out together, but prefer different activities.
    - **Matching Pennies**: Two players simultaneously place a penny, one wins if they match, the other if they differ.
    - **Hawk-Dove Game**: Two animals fight over a resource, can choose to be agressive or retreat.
    - **Custom Game**: Create your own payoff matrix!
    """)