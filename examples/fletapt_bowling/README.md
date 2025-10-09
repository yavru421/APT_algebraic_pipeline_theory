# FletAPT Bowling (Sanitized Example)

An offline, sanitized example of a Flet application formatted with Algebraic Pipeline Theory (APT).

- No secrets, API keys, or tokens.
- No external API calls (offline by default).
- Uses only fabricated sample data in `data/sample_records.json`.
- Minimal dependencies: Flet only for UI.

## APT Pipeline (Example)

We demonstrate a simplified, offline pipeline:

```
y13 = m13(x4)            # Load records from JSON file
(y10) = m10(y13)         # Compute leaderboard data
(y11) = m11(y10)         # Render leaderboard table (Flet)
(y9)  = m9(x2, y13, x5)  # Render calendar from league schedule and records
UI = (y9, y11)           # App shows Calendar + Leaderboard tabs
```

- x2: schedule_events (example league days)
- x4: records_file (path to bundled JSON)
- y13: loaded_records (games: [{date, players[]}])
- y10: leaderboard_data (sorted player stats)
- y11: leaderboard_table (Flet DataTable)
- y9: calendar_widget (Flet Column)

## Run locally

```bash
# From repository root
cd examples/fletapt_bowling
pip install -r requirements.txt
python -m src.main
```

If you prefer to run as a Flet app:

```bash
python -m src.main
```

## Project layout

```
examples/fletapt_bowling/
├─ README.md
├─ requirements.txt
├─ APT_EQUATION.md
├─ data/
│  └─ sample_records.json
├─ modules/
│  ├─ __init__.py
│  ├─ m9_calendar.py
│  ├─ m10_leaderboard.py
│  ├─ m11_table.py
│  └─ m13_load.py
└─ src/
   └─ main.py
```

## Notes
- This example intentionally excludes network calls and secret config for safety.
- To integrate a real vision pipeline, create new modules (m2, m3, m4, m6, m12, m14) and gate them behind environment variables.
