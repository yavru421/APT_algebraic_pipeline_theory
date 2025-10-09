import json
import os

def m13_load_bowling_records(records_file: str) -> dict:
    """Load bowling records from a JSON file.
    Offline-only. Returns {games: [...], metadata: {...}}.
    """
    if not os.path.exists(records_file):
        return {"games": [], "metadata": {"version": "1.0", "total_games": 0}}
    with open(records_file, "r", encoding="utf-8") as f:
        return json.load(f)
