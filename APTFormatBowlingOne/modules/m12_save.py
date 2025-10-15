import json
import os
from datetime import datetime


def _parse_llama_data_to_players(llama_data: str):
    """Parse simple llama text lines like 'Name: 175' into player dicts."""
    players = []
    if not llama_data:
        return players
    for line in str(llama_data).splitlines():
        parts = line.split(":")
        if len(parts) >= 2:
            name = parts[0].strip()
            try:
                score = int(parts[1].strip())
            except Exception:
                # try to extract numbers
                nums = [int(s) for s in parts[1].split() if s.isdigit()]
                score = nums[0] if nums else 0
            players.append({"name": name, "score": score})
    return players


def m12_save_bowling_records(results, records_file="bowling_records.json"):
    """
    Save a list of result dicts into a JSON records file.

    Each result is expected to have keys: filename, llama_data (text), exif
    This function will parse llama_data into a players array and append
    to records['games'].
    """
    records = {"games": [], "metadata": {"version": "1.0", "total_games": 0}}
    # Load existing
    if os.path.exists(records_file):
        try:
            with open(records_file, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            # start fresh if corrupted
            records = {"games": [], "metadata": {"version": "1.0", "total_games": 0}}

    for res in results:
        filename = res.get("filename")
        llama_data = res.get("llama_data") or res.get("llama_data", "")
        exif = res.get("exif", "")

        players = _parse_llama_data_to_players(llama_data)

        game = {
            "filename": filename,
            "players": players,
            "llama_raw": llama_data,
            "exif": exif,
            "saved_at": datetime.utcnow().isoformat() + "Z",
        }
        records.setdefault("games", []).append(game)

    # Update metadata
    records.setdefault("metadata", {})["total_games"] = len(records.get("games", []))
    records.setdefault("metadata", {}).setdefault("version", "1.0")

    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(records_file)), exist_ok=True)
    with open(records_file, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    return records
