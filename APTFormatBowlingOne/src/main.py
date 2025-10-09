# Bowling Team Scheduler (APT Flet Version)
# Implements: y1 = m1(x2), y2 = m2(x1), y3 = m3(y2), y4 = m4(y3), y5 = m5(x2, y4)

import flet as ft
import os
import requests
import base64
import llamaapi
import calendar
import datetime

# Import all modules
from modules.m0_dng_convert import m0_convert_dng, m0a_bulk_convert_dng
from modules.m1_ui import m1_schedule_ui
from modules.m2_upload import m2_upload_image
from modules.m3_api import m3_send_image_to_api
from modules.m4_parse import m4_parse_api_response
from modules.m5_display import m5_display_schedule_and_scores
from modules.m6_exif import m6_extract_exif_metadata
from modules.m7_metadata import m7_metadata_outliner
from modules.m8_batch import m8_auto_process_all_images
from modules.m9_calendar import m9_calendar_widget
from modules.m10_leaderboard import m10_create_leaderboard
from modules.m11_table import m11_leaderboard_table
from modules.m12_save import m12_save_bowling_records
from modules.m13_load import m13_load_bowling_records
from modules.m14_smart import m14_smart_process_images
from modules.m15_cleanup import m15_cleanup_processed_images

# Constants
SCORE_FOLDER = "score"
API_URL = "https://llama-universal-netlify-project.netlify.app/.netlify/functions/llama-proxy"
BOWLING_DAY = "Tuesday"
BOWLING_TIME = "7:00 PM"

# Main Flet app
def main(page: ft.Page):
    page.title = "Bowling Team Scheduler - APT Pipeline"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 1200
    page.window_height = 800

    # x2: calendar event data
    schedule_events = [
        {"date": "Every Tuesday", "desc": f"Bowling at {BOWLING_TIME}"}
    ]

    extracted_text = ""

    def on_upload(e: ft.FilePickerResultEvent):
        nonlocal extracted_text
        if e.files:
            file_path = e.files[0].path
            x1a = m0_convert_dng(file_path)
            y2 = m2_upload_image(x1a)
            y3 = m3_send_image_to_api(y2)
            y4 = m4_parse_api_response(y3)
            y6 = m6_extract_exif_metadata(y2)
            extracted_text = y4

            # Refresh the leaderboard tab
            refresh_tabs()

    def refresh_tabs():
        # Use smart processing - only process new images
        auto_results = m14_smart_process_images(SCORE_FOLDER, "bowling_records.json")

        # Create leaderboard data
        y10 = m10_create_leaderboard(auto_results)
        y11 = m11_leaderboard_table(y10)

        # Create cleanup callback
        def cleanup_files():
            return m15_cleanup_processed_images(SCORE_FOLDER, "bowling_records.json")

        # Update tabs content
        calendar_tab.content = ft.Column([
            m1_schedule_ui(schedule_events, file_picker, cleanup_files),
            m9_calendar_widget(tuesdays, auto_results, page),
            processed_outliner(auto_results)
        ])

        leaderboard_tab.content = ft.Column([
            y11
        ])

        page.update()

    # APT Pipeline: Initialize FilePicker first
    file_picker = ft.FilePicker(on_result=on_upload)
    page.overlay.append(file_picker)

    # APT Pipeline: First convert all DNG files, then smart-process (only new images)
    # y_converted = m0a(x_folder)
    converted_files = m0a_bulk_convert_dng(SCORE_FOLDER)

    # Use smart processing instead of reprocessing everything
    auto_results = m14_smart_process_images(SCORE_FOLDER, "bowling_records.json")

    # Create leaderboard data (APT: y10 = m10(auto_results), y11 = m11(y10))
    y10 = m10_create_leaderboard(auto_results)
    y11 = m11_leaderboard_table(y10)

    # Outliner for all processed images
    def processed_outliner(results):
        items = []
        for r in results:
            # Handle both old and new format
            filename = r.get('filename', 'Unknown')
            llama_data = r.get('raw_llama_data', r.get('llama_data', 'No data'))
            exif_data = r.get('exif_summary', r.get('exif', 'No EXIF'))
            items.append(ft.Text(f"{filename}\nLlama Data: {llama_data[:100]}...\nEXIF: {exif_data[:50]}...\n---"))
        return ft.Column([
            ft.Text("All Processed Images (Llama + EXIF):"),
            ft.ListView(items, height=400)
        ])

    # Example event: every Tuesday this month
    today = datetime.date.today()
    tuesdays = []
    for week in calendar.monthcalendar(today.year, today.month):
        if week[calendar.TUESDAY]:
            tuesdays.append({"date": f"{today.year}-{today.month:02d}-{week[calendar.TUESDAY]:02d}", "desc": "Bowling Night"})

    # Create cleanup callback
    def cleanup_files():
        return m15_cleanup_processed_images(SCORE_FOLDER, "bowling_records.json")

    # Create tabs
    calendar_tab = ft.Tab(
        text="📅 Calendar & Scores",
        content=ft.Column([
            m1_schedule_ui(schedule_events, file_picker, cleanup_files),
            m9_calendar_widget(tuesdays, auto_results, page),
            processed_outliner(auto_results)
        ])
    )

    leaderboard_tab = ft.Tab(
        text="🏆 Leaderboard",
        content=ft.Column([
            y11
        ])
    )

    # Create tab container
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            calendar_tab,
            leaderboard_tab
        ]
    )

    page.add(tabs)

    # APT: Final page update to render all components
    page.update()

if __name__ == "__main__":
    ft.app(target=main)