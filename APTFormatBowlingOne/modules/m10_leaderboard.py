# m10: Leaderboard module (APT-compliant)
# Input: y14 (smart_results) -> Output: y10 (leaderboard_data)
# Equation: y10 = m10(y14)

import re

def m10_create_leaderboard(results):
    """
    APT Module: m10
    Input: results (List[Dict]) - Processed image results with player data
    Output: leaderboard_data (List[Tuple]) - Sorted player statistics
    Equation: y10 = m10(y14)

    Description: Aggregates scores and creates player rankings from structured data
    """
    player_stats = {}

    for r in results:
        # Check if we're dealing with structured JSON data from records
        if isinstance(r, dict) and 'players' in r:
            # This is from the JSON records format - use structured data
            for player in r['players']:
                name = player['name'].strip()
                score = player['score']

                if name not in player_stats:
                    player_stats[name] = {
                        'total_score': 0,
                        'game_count': 0,
                        'scores': [],
                        'avg': 0.0,
                        'high_game': 0,
                        'low_game': 300
                    }

                player_stats[name]['total_score'] += score
                player_stats[name]['game_count'] += 1
                player_stats[name]['scores'].append(score)
                player_stats[name]['high_game'] = max(player_stats[name]['high_game'], score)
                player_stats[name]['low_game'] = min(player_stats[name]['low_game'], score)
                player_stats[name]['avg'] = player_stats[name]['total_score'] / player_stats[name]['game_count']
        else:
            # Old format: parse llama_data text (fallback)
            llama_text = r.get('llama_data', '')
            if 'API Error' in llama_text or 'Error:' in llama_text:
                continue

            # Extract player names and scores using regex patterns
            name_score_pattern = r'([A-Za-z\s]+):\s*(\d+)'
            matches = re.findall(name_score_pattern, llama_text)

            for name, score in matches:
                name = name.strip()
                if len(name) < 2 or len(name) > 20:  # Filter out invalid names
                    continue

                score = int(score)
                if score < 50 or score > 300:  # Reasonable bowling score range
                    continue

                if name not in player_stats:
                    player_stats[name] = {
                        'total_score': 0,
                        'game_count': 0,
                        'scores': [],
                        'avg': 0.0,
                        'high_game': 0,
                        'low_game': 300
                    }

                player_stats[name]['total_score'] += score
                player_stats[name]['game_count'] += 1
                player_stats[name]['scores'].append(score)
                player_stats[name]['high_game'] = max(player_stats[name]['high_game'], score)
                player_stats[name]['low_game'] = min(player_stats[name]['low_game'], score)
                player_stats[name]['avg'] = player_stats[name]['total_score'] / player_stats[name]['game_count']

    # Sort by average score (descending)
    sorted_players = sorted(player_stats.items(), key=lambda x: x[1]['avg'], reverse=True)

    return sorted_players