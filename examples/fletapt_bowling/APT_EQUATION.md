# APT Equation for FletAPT Bowling (Offline Example)

Variables:
- x2: schedule_events (list)
- x4: records_file (str)
- x5: ui_page (Flet page)

Outputs:
- y9: calendar_widget
- y10: leaderboard_data
- y11: leaderboard_table
- y13: loaded_records

Equations:
```
y13 = m13(x4)
y10 = m10(y13)
y11 = m11(y10)
y9  = m9(x2, y13, x5)
UI  = (y9, y11)
```

Signatures:
- m9(events: List, results: List[Dict], page: Page) -> UI
- m10(results: List[Dict]) -> List[Tuple]
- m11(leaderboard: List[Tuple]) -> UI
- m13(file: str) -> Dict

This example is offline-only and does not invoke any external services.