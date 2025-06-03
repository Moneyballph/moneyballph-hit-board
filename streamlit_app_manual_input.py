
import streamlit as st
import pandas as pd
from scipy.stats import binom

st.set_page_config(page_title="Moneyball Phil - Custom Hit Board", layout="wide")
st.title("⚾️ Moneyball Phil - Manual Hit Probability Simulator")

st.markdown("### 🔢 Enter Player Info and Stats")

player_name = st.text_input("Player Name", "José Ramírez")
odds = st.number_input("American Odds", value=-210)

last7 = st.number_input("Last 7 Days AVG", value=0.364, format="%.3f")
vs_pitcher = st.number_input("Vs Pitcher AVG", value=0.444, format="%.3f")
home_away = st.number_input("Home/Away AVG", value=0.283, format="%.3f")
vs_hand = st.number_input("Vs Handedness AVG", value=0.278, format="%.3f")
season_avg = st.number_input("Season AVG", value=0.277, format="%.3f")

if player_name:
    weights = {
        "Last 7 Days AVG": 0.3,
        "Vs Pitcher AVG": 0.3,
        "Home/Away AVG": 0.1,
        "Vs Handedness AVG": 0.2,
        "Season AVG": 0.1,
    }

    weighted_avg = round(
        last7 * weights["Last 7 Days AVG"] +
        vs_pitcher * weights["Vs Pitcher AVG"] +
        home_away * weights["Home/Away AVG"] +
        vs_hand * weights["Vs Handedness AVG"] +
        season_avg * weights["Season AVG"], 3
    )

    true_hit_prob = round((1 - binom.pmf(0, 4, weighted_avg)) * 100, 2)

    def implied_prob(odds):
        return round(abs(odds) / (abs(odds) + 100) * 100, 2) if odds < 0 else round(100 / (odds + 100) * 100, 2)

    implied = implied_prob(odds)
    ev = round(true_hit_prob - implied, 2)

    def hit_zone(p):
        if p >= 80:
            return "Elite"
        elif p >= 70:
            return "Strong"
        elif p >= 60:
            return "Moderate"
        else:
            return "Bad"

    def tag(ev):
        if ev >= 15:
            return "🔥 High Value"
        elif ev >= 5:
            return "✅ Fair"
        else:
            return "❌ Avoid"

    row = {
        "Player": player_name,
        "Odds": odds,
        "Weighted AVG": weighted_avg,
        "True Hit %": true_hit_prob,
        "Implied %": implied,
        "EV %": ev,
        "Hit Zone": hit_zone(true_hit_prob),
        "Value Tag": tag(ev)
    }

    st.markdown("### ✅ Simulation Result")
    st.dataframe(pd.DataFrame([row]))
