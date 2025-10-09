import flet as ft
import calendar
import datetime
from typing import List, Dict

def m9_calendar_widget(events: List[Dict], results: List[Dict], page: ft.Page):
    today = datetime.date.today()
    cal = calendar.monthcalendar(today.year, today.month)

    # Map event days for simple highlighting (offline)
    event_days = set()
    for e in events:
        try:
            parts = e.get("date", "").split("-")
            if len(parts) == 3 and int(parts[0]) == today.year and int(parts[1]) == today.month:
                event_days.add(int(parts[2]))
        except Exception:
            continue

    rows = []
    for week in cal:
        row = []
        for day in week:
            if day == 0:
                row.append(ft.Container(width=32))
            else:
                label = f"{day}*" if day in event_days else str(day)
                color = "#D32F2F" if day in event_days else None
                row.append(ft.Text(label, width=32, color=color))
        rows.append(ft.Row(row))

    return ft.Column([
        ft.Text(today.strftime("%B %Y"), size=20, weight=ft.FontWeight.BOLD),
        *rows
    ])
