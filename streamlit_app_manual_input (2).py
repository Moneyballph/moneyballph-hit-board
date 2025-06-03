
import streamlit as st
import pandas as pd
from scipy.stats import binom

st.set_page_config(page_title="Moneyball Phil: Daily Hit Simulator", layout="wide")

st.title("⚾ Moneyball Phil: Daily Hit Probability Simulator")

# Step 1: Create a session-based results list to store each player
if "results_table" not in st.session_state:
    st.session_state["results_table"] = []

# Input fields
st.header("🔍 Enter Player Stats")

player_name = st.text_input("Player Name")
last7_avg = st.number_input("Last 7 Days AVG", min_value=0.0, max_value=1.0, format="%.4f")
vs_pitcher_avg = st.number_input("AVG vs Pitcher (enter 0 if none)", min_value=0.0, max_value=1.0, format="%.4f")
home_away_avg = st.number_input("Home/Away AVG", min_value=0.0, max_value=1.0, format="%.4f")
handedness_avg = st.number_input("AVG vs Handedness", min_value=0.0, max_value=1.0, format="%.4f")
season_avg = st.number_input("Season AVG", min_value=0.0, max_value=1.0, format="%.4f")
odds = st.text_input("Sportsbook Odds (e.g. -250 or +120)")

# Hit Zone Logic
def classify_hit_zone(p):
    if p >= 80:
        return "🔥 Elite"
    elif p >= 70:
        return "✅ Strong"
    elif p >= 60:
        return "⚠️ Moderate"
    else:
        return "❌ Low"

# Run simulation
if st.button("Analyze Player"):
    # Step 2: Weighted average
    weight_avg = (
        last7_avg * 0.3 +
        vs_pitcher_avg * 0.3 +
        home_away_avg * 0.1 +
        handedness_avg * 0.2 +
        season_avg * 0.1
    )

    # Step 3: Binomial true hit probability over 4 ABs
    true_prob = 1 - binom.pmf(0, 4, weight_avg)

    # Step 4: Calculate implied probability
    try:
        odds_val = int(odds)
        if odds_val < 0:
            implied_prob = abs(odds_val) / (abs(odds_val) + 100)
        else:
            implied_prob = 100 / (odds_val + 100)
    except:
        implied_prob = 0.0

    ev = (true_prob - implied_prob) * 100
    hit_zone = classify_hit_zone(true_prob * 100)
    value_tag = "🔥 High Value" if ev >= 15 else "—"

    # Step 5: Append to session state table
    result = {
        "Player": player_name,
        "True Hit %": f"{true_prob*100:.1f}%",
        "Implied %": f"{implied_prob*100:.1f}%",
        "EV %": f"{ev:.1f}%",
        "Hit Zone": hit_zone,
        "Value": value_tag
    }
    st.session_state["results_table"].append(result)

# Step 6: Show the live hit board
if st.session_state["results_table"]:
    st.markdown("### 📊 Live Hit Board")
    st.dataframe(pd.DataFrame(st.session_state["results_table"]))
