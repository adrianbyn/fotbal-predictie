import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Predicții Fotbal", layout="wide")
st.title("📊 Aplicație Predicții Fotbal")

API_KEY = st.secrets["API_FOOTBALL_KEY"]
HEADERS = {"x-apisports-key": API_KEY}
API_BASE = "https://v3.football.api-sports.io"

# Selectează țara
countries_res = requests.get(f"{API_BASE}/countries", headers=HEADERS).json()
countries = [c["name"] for c in countries_res["response"]]
country = st.sidebar.selectbox("Selectează țară", sorted(countries))

# Selectează liga
leagues_res = requests.get(f"{API_BASE}/leagues", headers=HEADERS, params={"country": country}).json()
leagues = {l["league"]["id"]: l["league"]["name"] for l in leagues_res["response"]}
league_id = st.sidebar.selectbox("Selectează ligă", list(leagues.keys()), format_func=lambda x: leagues[x])

# Selectează data
date = st.sidebar.date_input("Selectează data")

# Obține meciurile
fixtures_res = requests.get(f"{API_BASE}/fixtures", headers=HEADERS,
                            params={"league": league_id, "season": 2025, "date": date.strftime("%Y-%m-%d")}).json()
matches = fixtures_res.get("response", [])

if not matches:
    st.warning("Nu s-au găsit meciuri pentru criteriile alese.")
else:
    data = []
    for m in matches:
        fixture_id = m["fixture"]["id"]
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        pred_res = requests.get(f"{API_BASE}/predictions", headers=HEADERS, params={"fixture": fixture_id}).json()
        if pred_res["response"]:
            pred = pred_res["response"][0]["predictions"]
            data.append({
                "Meci": f"{home} vs {away}",
                "Victorie gazdă": pred["win"]["home"],
                "Egal": pred["win"]["draw"],
                "Victorie oaspeți": pred["win"]["away"],
                "Ambele marchează?": "DA" if pred["goals"]["both"] == "Yes" else "NU",
                "Pauză/Final": f"{pred['win']['halfTime']}/{pred['win']['fullTime']}"
            })
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
