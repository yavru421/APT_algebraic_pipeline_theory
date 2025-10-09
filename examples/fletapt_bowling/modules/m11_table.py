import flet as ft
from typing import List, Tuple

def m11_leaderboard_table(leaderboard_data: List[Tuple[str, dict]]):
    if not leaderboard_data:
        return ft.Column([
            ft.Text("No bowling data yet.", size=20),
            ft.Text("Using offline sample data in data/sample_records.json"),
        ])
    columns = [
        ft.DataColumn(ft.Text("Rank", weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Player", weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Games", weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Average", weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("High", weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Low", weight=ft.FontWeight.BOLD)),
    ]
    rows = []
    for rank, (name, stats) in enumerate(leaderboard_data, 1):
        rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(str(rank))),
            ft.DataCell(ft.Text(name)),
            ft.DataCell(ft.Text(str(stats["game_count"]))),
            ft.DataCell(ft.Text(f"{stats['avg']:.1f}")),
            ft.DataCell(ft.Text(str(stats["total_score"]))),
            ft.DataCell(ft.Text(str(stats["high_game"]))),
            ft.DataCell(ft.Text(str(stats["low_game"]))),
        ]))
    return ft.DataTable(columns=columns, rows=rows)
