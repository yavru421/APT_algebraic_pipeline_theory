from typing import Dict, List, Tuple

def m10_create_leaderboard(results: List[Dict]) -> List[Tuple[str, dict]]:
    """Aggregate player stats and return sorted leaderboard.
    Results expected as list of game dicts: {'players': [{'name','score'}, ...], ...}
    """
    player_stats: Dict[str, dict] = {}
    for game in results:
        players = game.get("players", [])
        for p in players:
            name = str(p.get("name", "")).strip()
            try:
                score = int(p.get("score", 0))
            except Exception:
                continue
            if not name:
                continue
            s = player_stats.setdefault(name, {
                "total_score": 0,
                "game_count": 0,
                "scores": [],
                "avg": 0.0,
                "high_game": 0,
                "low_game": 300,
            })
            s["total_score"] += score
            s["game_count"] += 1
            s["scores"].append(score)
            s["high_game"] = max(s["high_game"], score)
            s["low_game"] = min(s["low_game"], score)
            s["avg"] = s["total_score"] / s["game_count"]
    return sorted(player_stats.items(), key=lambda x: x[1]["avg"], reverse=True)
