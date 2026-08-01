"""
国勢調査2020年の総人口データを検索
"""

import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
APP_ID = os.environ["ESTAT_APP_ID"]

url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList"

params = {
    "appId": APP_ID,
    "searchWord": "国勢調査 2020 人口",
    "surveyYears": "2020",
    "limit": 20
}

response = requests.get(url, params=params, timeout=60)
data = response.json()

if "GET_STATS_LIST" in data and "DATALIST_INF" in data["GET_STATS_LIST"]:
    tables = data["GET_STATS_LIST"]["DATALIST_INF"].get("TABLE_INF", [])
    
    if not isinstance(tables, list):
        tables = [tables]
    
    print(f"検索結果: {len(tables)} 件\n")
    
    for i, table in enumerate(tables[:10], 1):
        table_id = table.get("@id", "N/A")
        title = table.get("TITLE", {}).get("$", "N/A")
        
        print(f"[{i}] {table_id}")
        print(f"    {title[:100]}...")
        print()
else:
    print("検索結果なし")
