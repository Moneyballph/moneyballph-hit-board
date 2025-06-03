
import streamlit as st
import pandas as pd
from scipy.stats import binom

st.set_page_config(page_title="Moneyball Phil - Hit Board", layout="wide")

st.title("⚾️ Moneyball Phil - Automated Hit Board Prototype")
st.markdown("### Enter Player Name to Simulate True Hit % and Value")

player_name = st.text_input("Enter Player Name (e.g. José Ramírez):")

if player_name:
    st.markdown(f"🔍 Simulating data for **{player_name}**...")

    data = {
        "Player": [player_name],
        "Team": ["CLE"],
        "Odds (American)": [-210],
        "Last 7 Days AVG": [0.364],
        "Vs Pitcher AVG": [0.444],
        "Home/Away AVG": [0.283],
        "Vs Handedness AVG": [0.278],
        "Season AVG": [0.277],
    }

    df = pd.DataFrame(data)

    weights = {
        "Last 7 Days AVG": 0.3,
        "Vs Pitcher AVG": 0.3,
        "Home/Away AVG": 0.1,
        "Vs Handedness AVG": 0.2,
        "Season AVG": 0.1,
    }

    df["Weighted AVG"] = (
        df["Last 7 Days AVG"] * weights["Last 7 Days AVG"] +
        df["Vs Pitcher AVG"] * weights["Vs Pitcher AVG"] +
        df["Home/Away AVG"] * weights["Home/Away AVG"] +
        df["Vs Handedness AVG"] * weights["Vs Handedness AVG"] +
        df["Season AVG"] * weights["Season AVG"]
    ).round(3)

    df["True Hit %"] = (1 - binom.pmf(0, 4, df["Weighted AVG"])).round(4) * 100

    def implied_prob(odds):
        return abs(odds) / (abs(odds) + 100) if odds < 0 else 100 / (odds + 100)

    df["Implied %"] = df["Odds (American)"].apply(implied_prob).round(3) * 100
    df["EV %"] = (df["True Hit %"] - df["Implied %"]).round(1)

    def zone(p):
        if p >= 80:
            return "Elite"
        elif p >= 70:
            return "Strong"
        elif p >= 60:
            return "Moderate"
        else:
            return "Bad"

    df["Hit Zone"] = df["True Hit %"].apply(zone)

    def tag(ev):
        if ev >= 15:
            return "🔥 High Value"
        elif ev >= 5:
            return "✅ Fair"
        else:
            return "❌ Avoid"

    df["Value Tag"] = df["EV %"].apply(tag)

    st.markdown("### 🧠 Simulation Result")
    st.dataframe(df)
