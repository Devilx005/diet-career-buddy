import streamlit as st
import requests
from datetime import datetime

@st.cache_data(ttl=1800)
def get_live_job_data():
    try:
        response = requests.get(
            "https://api.github.com/search/repositories",
            params={"q": "job+hiring+india+software", "sort": "updated", "per_page": 10},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "total": data.get("total_count", 0),
                "updated": datetime.now().strftime("%H:%M:%S")
            }
    except:
        pass
    return {"success": False, "total": 8500, "updated": datetime.now().strftime("%H:%M:%S")}

@st.cache_data(ttl=1800)
def get_market_sentiment():
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "bitcoin", "vs_currencies": "usd", "include_24hr_change": "true"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            change = data.get("bitcoin", {}).get("usd_24h_change", 0)
            return {
                "success": True,
                "change": change,
                "trend": "📈 Bullish" if change > 0 else "📉 Bearish" if change < -2 else "📊 Stable",
                "multiplier": 1.05 if change > 2 else 0.98 if change < -2 else 1.0
            }
    except:
        pass
    return {"success": False, "change": 2.5, "trend": "📊 Stable", "multiplier": 1.02}
