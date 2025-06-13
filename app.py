import streamlit as st
import requests

st.title("Test API Football Fixtures - Fără dată")

API_KEY = st.secrets["API_FOOTBALL_KEY"]
HEADERS = {"x-apisports-key": API_KEY}
API_BASE = "https://v3.football.api-sports.io"

league_id = 39  # Premier League
seasons_to_try = [2024, 2025]

fixtures = None
used_season = None

for season in seasons_to_try:
    params = {
        "league": league_id,
        "season": season,
        # fără 'date' ca să aducem toate meciurile din sezon
    }
    response = requests.get(f"{API_BASE}/fixtures", headers=HEADERS, params=params)
    data = response.json()
    if data.get("response") and len(data["response"]) > 0:
        fixtures = data["response"]
        used_season = season
        break

if fixtures:
    st.write(f"Am găsit meciuri pentru sezonul {used_season}:")
    st.json(fixtures)
else:
    st.write("Nu s-au găsit meciuri pentru niciunul din sezoanele încercate.")
