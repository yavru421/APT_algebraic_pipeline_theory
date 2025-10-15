import json
import os


def m13_load_bowling_records(records_file="bowling_records.json"):
    """
    Load bowling records from a JSON file. If the file doesn't exist,
    return an empty structure matching test expectations.
    """
    default = {"games": [], "metadata": {"version": "1.0", "total_games": 0}}
    if not os.path.exists(records_file):
        return default

    try:
        with open(records_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure required keys exist
            if "games" not in data:
                data["games"] = []
            if "metadata" not in data:
                data["metadata"] = {"version": "1.0", "total_games": len(data.get("games", []))}
            return data
    except Exception:
        return default
