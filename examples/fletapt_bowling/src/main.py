import flet as ft
import os
from modules.m13_load import m13_load_bowling_records
from modules.m10_leaderboard import m10_create_leaderboard
from modules.m11_table import m11_leaderboard_table
from modules.m9_calendar import m9_calendar_widget

data_file = os.path.join(os.path.dirname(__file__), "..", "data", "sample_records.json")

def main(page: ft.Page):
    page.title = "FletAPT Bowling (Offline Example)"
    page.window_width = 1100
    page.window_height = 800

    # Offline schedule: every Thursday of current month
    import datetime, calendar
    today = datetime.date.today()
    thursdays = []
    for week in calendar.monthcalendar(today.year, today.month):
        if week[calendar.THURSDAY]:
            thursdays.append({"date": f"{today.year}-{today.month:02d}-{week[calendar.THURSDAY]:02d}", "desc": "League Night"})

    # Load and compute UI
    records = m13_load_bowling_records(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "sample_records.json")))
    games = records.get("games", [])
    leaderboard_data = m10_create_leaderboard(games)

    calendar_tab = ft.Tab(
        text="📅 Calendar",
        content=m9_calendar_widget(thursdays, games, page)
    )
    leaderboard_tab = ft.Tab(
        text="🏆 Leaderboard",
        content=ft.Container(content=m11_leaderboard_table(leaderboard_data), padding=16)
    )

    tabs = ft.Tabs(tabs=[calendar_tab, leaderboard_tab])
    page.add(tabs)

if __name__ == "__main__":
    ft.app(target=main)
