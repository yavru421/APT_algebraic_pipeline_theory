# m9: Calendar widget module (APT-compliant)
import calendar
import datetime
# m9: Calendar widget module (APT-compliant, with popups)
def m9_calendar_widget(events, results, page):
    today = datetime.date.today()
    cal = calendar.monthcalendar(today.year, today.month)
    # Map event days to results by date
    event_map = {e['date']: e['desc'] for e in events if '-' in e['date']}
    result_map = {}
    for r in results:
        # Try to extract date from EXIF or filename (fallback: unknown)
        date_str = None

        # Handle both old format (with 'exif' key) and new format (with 'exif_summary' key)
        exif_data = r.get('exif_summary', r.get('exif', ''))

        for line in exif_data.splitlines():
            if 'File Modification Date/Time' in line:
                date_str = line.split(':',1)[-1].strip().split(' ')[0]
                break
        if not date_str:
            # Try filename: IMG_YYYYMMDD
            import re
            filename = r.get('filename', '')
            m = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
            if m:
                date_str = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        if date_str:
            # Handle both old format (llama_data) and new format (raw_llama_data)
            llama_data = r.get('raw_llama_data', r.get('llama_data', ''))
            result_map[date_str] = llama_data

    # Dialog for popups
    dlg = ft.AlertDialog(modal=True, title=ft.Text("Bowling Scores"), content=ft.Text("Select a date to view scores."))
    from functools import partial
    def show_scores(e, date):  # Fix: Add e parameter for event
        scores = result_map.get(date, 'No scores found.')
        dlg.title = ft.Text(f"Scores for {date}")
        dlg.content = ft.Text(str(scores))
        page.dialog = dlg
        dlg.open = True
        page.update()

    rows = []
    for week in cal:
        row = []
        for day in week:
            if day == 0:
                row.append(ft.Text(" ", width=32))
            else:
                # Build date string for this day
                date_str = f"{today.year}-{today.month:02d}-{day:02d}"
                if date_str in event_map:
                    row.append(ft.Container(
                        content=ft.TextButton(
                            text=f"{day}*",
                            style=ft.ButtonStyle(color="red"),
                            on_click=lambda e, d=date_str: show_scores(e, d)  # Fix: Pass both e and date
                        ),
                        bgcolor="#ffe0e0",
                        width=32,
                        border_radius=6
                    ))
                else:
                    row.append(ft.Text(str(day), width=32))
        rows.append(ft.Row(row))
    return ft.Column([
        ft.Text(f"{today.strftime('%B %Y')} Calendar", style="titleLarge"),
        *rows,
        dlg
    ])
# m8: Auto-process all images in score folder and send to Llama
def m8_auto_process_all_images(score_folder):
    results = []
    print(f"APT m8: Processing files in {score_folder}")

    if not os.path.exists(score_folder):
        print(f"APT m8: Score folder {score_folder} does not exist")
        return results

    files_found = os.listdir(score_folder)
    print(f"APT m8: Found {len(files_found)} files: {files_found}")

    for fname in files_found:
        print(f"APT m8: Processing file: {fname}")
        try:
            fpath = os.path.join(score_folder, fname)
            if os.path.isfile(fpath):
                # Convert DNG if needed
                x1a = m0_convert_dng(fpath)
                print(f"APT m8: Converted file: {x1a}")

                # Skip if conversion failed
                if x1a is None:
                    print(f"APT m8: Skipping file due to conversion failure: {fname}")
                    continue

                # Upload (redundant for local, but keep for pipeline)
                y2 = m2_upload_image(x1a)
                print(f"APT m8: Upload result: {y2}")

                # Send to Llama with prompt using LlamaAPIClient
                print(f"APT m8: Sending to API using LlamaAPIClient")

                # Read image and encode as base64 - resize if too large
                import base64
                from PIL import Image
                if not os.path.exists(y2):
                    print(f"APT m8: Warning - file does not exist: {y2}")
                    continue

                file_size = os.path.getsize(y2)
                print(f"APT m8: File size: {file_size} bytes")

                if file_size == 0:
                    print(f"APT m8: Warning - file is empty: {y2}")
                    continue

                # Resize image if too large (over 5MB)
                if file_size > 5 * 1024 * 1024:  # 5MB
                    print(f"APT m8: Resizing large image: {file_size} bytes")
                    try:
                        img = Image.open(y2)
                        # Resize to max 1920x1080 while maintaining aspect ratio
                        img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                        # Save resized image to temp file
                        temp_path = y2.replace('.png', '_resized.png').replace('.jpg', '_resized.jpg')
                        img.save(temp_path, optimize=True, quality=85)
                        y2 = temp_path
                        print(f"APT m8: Resized to: {os.path.getsize(y2)} bytes")
                    except Exception as resize_error:
                        print(f"APT m8: Resize failed: {resize_error}")

                with open(y2, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')

                print(f"APT m8: Base64 data length: {len(image_data)} characters")

                # Use the correct LlamaAPIClient format
                from llama_api_client import LlamaAPIClient

                print(f"APT m8: Making API request with correct client...")
                try:
                    client = LlamaAPIClient()

                    response = client.chat.completions.create(
                        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Extract all bowling scores, player names, dates, or game information from this image. Image filename: {fname}",
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{image_data}"
                                        },
                                    },
                                ],
                            },
                        ],
                    )

                    print(f"APT m8: API response received successfully")
                    y4 = response.completion_message.content.text
                    print(f"APT m8: Extracted text: {y4}")

                except Exception as api_error:
                    print(f"APT m8: API call failed: {api_error}")
                    print(f"APT m8: Error type: {type(api_error)}")
                    import traceback
                    print(f"APT m8: Full traceback: {traceback.format_exc()}")
                    y4 = f"API Error: {api_error}"

                y6 = m6_extract_exif_metadata(y2)

                results.append({
                    "filename": fname,
                    "llama_data": y4,
                    "exif": y6
                })
        except Exception as err:
            print(f"APT m8: Error processing {fname}: {err}")
            results.append({
                "filename": fname,
                "llama_data": f"Error: {err}",
                "exif": ""
            })

    print(f"APT m8: Completed processing {len(results)} files")
    return results
# m0: DNG conversion module (simplified - skip DNG, process PNG/JPG directly)
def m0_convert_dng(file_path):
    import subprocess
    import os
    # For PNG/JPG files, return as-is
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        return file_path

    # For DNG files, skip conversion and return None
    if file_path.lower().endswith('.dng'):
        print(f"APT m0: Skipping DNG file (convert to PNG first): {file_path}")
        return None

    return file_path

# m0a: Bulk DNG conversion module (APT-compliant)
def m0a_bulk_convert_dng(score_folder):
    """
    APT Module: m0a
    Input: x_folder (score folder path)
    Output: y_converted (list of converted file paths)
    Equation: y_converted = m0a(x_folder)
    """
    import os
    converted_files = []
    if not os.path.exists(score_folder):
        os.makedirs(score_folder)
        return converted_files

    for fname in os.listdir(score_folder):
        fpath = os.path.join(score_folder, fname)
        if os.path.isfile(fpath):
            converted_path = m0_convert_dng(fpath)
            converted_files.append(converted_path)

    return converted_files
# Bowling Team Scheduler (APT Flet Version)
# Implements: y1 = m1(x2), y2 = m2(x1), y3 = m3(y2), y4 = m4(y3), y5 = m5(x2, y4)

import flet as ft
import os
import requests
import base64
import llamaapi

# Constants
SCORE_FOLDER = "score"
API_URL = "https://llama-universal-netlify-project.netlify.app/.netlify/functions/llama-proxy"
BOWLING_DAY = "Tuesday"
BOWLING_TIME = "7:00 PM"

# m1: UI module (Flet-based)
def m1_schedule_ui(schedule_events, file_picker, cleanup_callback=None):

    def on_cleanup_click(e):
        if cleanup_callback:
            result = cleanup_callback()
            # Show result in a dialog
            dialog = ft.AlertDialog(
                title=ft.Text("Cleanup Complete"),
                content=ft.Text(f"Removed {result.get('removed', 0)} processed files\nKept {result.get('kept', 0)} unprocessed files"),
                actions=[ft.TextButton("OK", on_click=lambda e: setattr(dialog, 'open', False) or e.page.update())]
            )
            e.page.dialog = dialog
            dialog.open = True
            e.page.update()

    return ft.Column([
        ft.Text("Bowling Team Scheduler", style="headlineMedium"),
        ft.Text(f"Weekly Event: {BOWLING_DAY}s at {BOWLING_TIME}"),
        ft.ListView([
            ft.Text(f"{event['date']}: {event['desc']}") for event in schedule_events
        ], height=100),
        ft.Text("Upload Score Image:"),
        ft.ElevatedButton(
            "Pick Image File",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["png", "jpg", "jpeg", "dng"]
            )
        ),
        ft.Divider(),
        ft.Text("File Management:", style="titleMedium"),
        ft.ElevatedButton(
            "🗑️ Clean Up Processed Images",
            icon=ft.Icons.DELETE_SWEEP,
            on_click=on_cleanup_click,
            color="#FF5722"
        ),
        ft.Text("(Removes images that have been saved to records)",
                style="bodySmall", color="#666666"),
    ])

# m2: Image upload module
def m2_upload_image(file_path):
    if not os.path.exists(SCORE_FOLDER):
        os.makedirs(SCORE_FOLDER)
    dest = os.path.join(SCORE_FOLDER, os.path.basename(file_path))

    # If the file is already in the score folder, don't copy it to itself
    if os.path.abspath(file_path) == os.path.abspath(dest):
        print(f"APT m2: File already in score folder, returning as-is: {dest}")
        return dest

    # Copy file to score folder
    with open(file_path, "rb") as src, open(dest, "wb") as dst:
        dst.write(src.read())
    return dest

# m3: API request module
def m3_send_image_to_api(image_path):
    with open(image_path, "rb") as f:
        files = {"file": (os.path.basename(image_path), f, "image/png")}
        response = requests.post(API_URL, files=files)
    return response.json()

# m4: Response parsing module
def m4_parse_api_response(api_response):
    # Parse chat completions response format
    try:
        if "choices" in api_response and len(api_response["choices"]) > 0:
            return api_response["choices"][0]["message"]["content"]
        else:
            return api_response.get("text", str(api_response))
    except Exception as e:
        return f"Parse error: {e} - Response: {str(api_response)[:100]}..."

# m5: Calendar logic module (APT: explicit exif_metadata)
def m5_display_schedule_and_scores(schedule_events, extracted_text, exif_metadata):
    return ft.Column([
        ft.Text("Extracted Score Data:"),
        ft.Text(extracted_text or "No score uploaded yet."),
        ft.Text("Image Metadata (EXIF):"),
        ft.Text(exif_metadata or "No metadata found."),
        ft.Text("Upcoming Events:"),
        ft.ListView([
            ft.Text(f"{event['date']}: {event['desc']}" ) for event in schedule_events
        ], height=100),
    ])

# m6: EXIF metadata extraction module
def m6_extract_exif_metadata(image_path):
    import subprocess
    try:
        result = subprocess.run([
            "exiftool", image_path
        ], capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"EXIF extraction error: {e}"

# m10: Leaderboard module (APT-compliant) - Aggregates scores and creates rankings
def m10_create_leaderboard(results):
    """
    APT Module: m10
    Input: results (list of processed image results with llama_data)
    Output: leaderboard_data (dict with player stats and rankings)
    Equation: y10 = m10(results)
    """
    import re

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
            # Pattern for "Player Name: Score"
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

# m11: Leaderboard display module (APT-compliant) - Creates Flet table widget
def m11_leaderboard_table(leaderboard_data):
    """
    APT Module: m11
    Input: leaderboard_data (sorted list of player stats)
    Output: flet_table (Flet DataTable widget)
    Equation: y11 = m11(y10)
    """

    if not leaderboard_data:
        return ft.Column([
            ft.Text("No bowling data found yet.", style=ft.TextThemeStyle.HEADLINE_MEDIUM, color="#000000"),
            ft.Text("Upload some bowling score images to see the leaderboard!", color="#666666")
        ])

    # Create table headers with proper Material Design colors
    columns = [
        ft.DataColumn(ft.Text("Rank", weight=ft.FontWeight.BOLD, color="#FFFFFF")),
        ft.DataColumn(ft.Text("Player Name", weight=ft.FontWeight.BOLD, color="#FFFFFF")),
        ft.DataColumn(ft.Text("Games", weight=ft.FontWeight.BOLD, color="#FFFFFF")),
        ft.DataColumn(ft.Text("Average", weight=ft.FontWeight.BOLD, color="#FFFFFF")),
        ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.BOLD, color="#FFFFFF")),
        ft.DataColumn(ft.Text("High Game", weight=ft.FontWeight.BOLD, color="#FFFFFF")),
        ft.DataColumn(ft.Text("Low Game", weight=ft.FontWeight.BOLD, color="#FFFFFF")),
    ]

    # Create table rows with proper Material Design color scheme
    rows = []
    for rank, (player_name, stats) in enumerate(leaderboard_data, 1):
        # Determine row color based on rank - using Material Design surface colors
        if rank == 1:
            row_color = "#FFF3E0"  # Gold winner (Amber 50)
            text_color = "#E65100"  # Amber 900
        elif rank == 2:
            row_color = "#ECEFF1"  # Silver (Blue Grey 50)
            text_color = "#263238"  # Blue Grey 900
        elif rank == 3:
            row_color = "#FFF3E0"  # Bronze (Orange 50)
            text_color = "#E65100"  # Orange 900
        else:
            row_color = "#F5F5F5" if rank % 2 == 0 else "#FFFFFF"  # Alternating rows
            text_color = "#212121"  # Dark text

        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(rank), color=text_color, weight=ft.FontWeight.BOLD if rank <= 3 else ft.FontWeight.NORMAL)),
                ft.DataCell(ft.Text(player_name, color=text_color, weight=ft.FontWeight.BOLD if rank <= 3 else ft.FontWeight.NORMAL)),
                ft.DataCell(ft.Text(str(stats['game_count']), color=text_color)),
                ft.DataCell(ft.Text(f"{stats['avg']:.1f}", color=text_color, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(str(stats['total_score']), color=text_color)),
                ft.DataCell(ft.Text(str(stats['high_game']), color=text_color, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(str(stats['low_game']), color=text_color)),
            ],
            color=row_color
        )
        rows.append(row)

    # Create the data table with improved Material Design styling
    data_table = ft.DataTable(
        columns=columns,
        rows=rows,
        border=ft.border.all(1, "#E0E0E0"),
        border_radius=12,
        vertical_lines=ft.border.BorderSide(0.5, "#E0E0E0"),
        horizontal_lines=ft.border.BorderSide(0.5, "#E0E0E0"),
        heading_row_color="#1976D2",  # Blue primary
        show_checkbox_column=False,
    )

    # Create summary stats with proper colors
    total_games = sum(stats['game_count'] for _, stats in leaderboard_data)
    avg_of_averages = sum(stats['avg'] for _, stats in leaderboard_data) / len(leaderboard_data)
    highest_score = max(stats['high_game'] for _, stats in leaderboard_data)

    summary = ft.Column([
        ft.Text("🏆 Bowling Leaderboard",
                style=ft.TextThemeStyle.HEADLINE_LARGE,
                weight=ft.FontWeight.BOLD,
                color="#212121"),
        ft.Text(f"📊 Total Games: {total_games} | League Average: {avg_of_averages:.1f} | Highest Score: {highest_score}",
                style=ft.TextThemeStyle.BODY_LARGE,
                color="#757575"),
        ft.Divider(color="#E0E0E0"),
    ])

    # Create scrollable container with proper Material Design styling
    scrollable_table = ft.Container(
        content=ft.Column([
            data_table
        ], scroll=ft.ScrollMode.AUTO),
        height=500,  # Fixed height to enable scrolling
        padding=ft.padding.all(16),
        margin=ft.margin.all(8),
        border_radius=12,
        bgcolor="#FFFFFF",
        border=ft.border.all(1, "#E0E0E0"),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=3,
            color="#00000020",
            offset=ft.Offset(0, 1),
        )
    )

    return ft.Column([
        summary,
        scrollable_table
    ])# m12: Data persistence module (APT-compliant) - Manages JSON record storage
def m12_save_bowling_records(results, records_file="bowling_records.json"):
    """
    APT Module: m12
    Input: results (list of processed image results), records_file (path)
    Output: y12 (updated records dict)
    Equation: y12 = m12(results, records_file)
    """
    import json
    import os
    from datetime import datetime

    # Load existing records if file exists
    if os.path.exists(records_file):
        try:
            with open(records_file, 'r') as f:
                records = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            records = {"games": [], "metadata": {"created": datetime.now().isoformat(), "version": "1.0"}}
    else:
        records = {"games": [], "metadata": {"created": datetime.now().isoformat(), "version": "1.0"}}

    # Process each result and add to records if not already exists
    for r in results:
        filename = r.get('filename', '')
        llama_data = r.get('llama_data', '')
        exif_data = r.get('exif', '')

        # Skip if already processed or error
        if any(game.get('filename') == filename for game in records['games']):
            print(f"APT m12: Skipping already recorded file: {filename}")
            continue

        if 'API Error' in llama_data or 'Error:' in llama_data:
            print(f"APT m12: Skipping error file: {filename}")
            continue

        # Extract date from EXIF or filename
        date_str = None
        for line in exif_data.splitlines():
            if 'File Modification Date/Time' in line:
                date_str = line.split(':', 1)[-1].strip().split(' ')[0]
                break

        if not date_str:
            # Try filename: IMG_YYYYMMDD
            import re
            m = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
            if m:
                date_str = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
            else:
                date_str = datetime.now().strftime('%Y-%m-%d')

        # Extract player scores using regex
        import re
        players = []
        name_score_pattern = r'([A-Za-z\s]+):\s*(\d+)'
        matches = re.findall(name_score_pattern, llama_data)

        for name, score in matches:
            name = name.strip()
            if len(name) >= 2 and len(name) <= 20 and name not in ['Game', 'Total', 'Scratch', 'Hdcp']:
                try:
                    score_int = int(score)
                    if 50 <= score_int <= 300:  # Valid bowling score range
                        players.append({"name": name, "score": score_int})
                except ValueError:
                    continue

        # Create game record
        game_record = {
            "filename": filename,
            "date": date_str,
            "timestamp": datetime.now().isoformat(),
            "players": players,
            "raw_llama_data": llama_data[:500],  # Truncate for storage
            "exif_summary": exif_data[:200] if exif_data else ""
        }

        records['games'].append(game_record)
        print(f"APT m12: Recorded game data for {filename} with {len(players)} players on {date_str}")

    # Update metadata
    records['metadata']['last_updated'] = datetime.now().isoformat()
    records['metadata']['total_games'] = len(records['games'])

    # Save updated records
    try:
        with open(records_file, 'w') as f:
            json.dump(records, f, indent=2)
        print(f"APT m12: Saved {len(records['games'])} total games to {records_file}")
    except Exception as e:
        print(f"APT m12: Error saving records: {e}")

    return records

# m13: Data loading module (APT-compliant) - Loads existing bowling records
def m13_load_bowling_records(records_file="bowling_records.json"):
    """
    APT Module: m13
    Input: records_file (path)
    Output: y13 (records dict)
    Equation: y13 = m13(records_file)
    """
    import json
    import os

    if not os.path.exists(records_file):
        print(f"APT m13: No existing records file found: {records_file}")
        return {"games": [], "metadata": {"created": "", "version": "1.0"}}

    try:
        with open(records_file, 'r') as f:
            records = json.load(f)
        print(f"APT m13: Loaded {len(records.get('games', []))} games from {records_file}")
        return records
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"APT m13: Error loading records: {e}")
        return {"games": [], "metadata": {"created": "", "version": "1.0"}}

# m14: Smart processing module (APT-compliant) - Only processes new images
def m14_smart_process_images(score_folder, records_file="bowling_records.json"):
    """
    APT Module: m14
    Input: score_folder (path), records_file (path)
    Output: y14 (combined results from cache and new processing)
    Equation: y14 = m14(score_folder, records_file)
    """
    # Load existing records
    records = m13_load_bowling_records(records_file)
    processed_files = {game['filename'] for game in records['games']}

    # Get all files in score folder
    if not os.path.exists(score_folder):
        print(f"APT m14: Score folder {score_folder} does not exist")
        return []

    files_found = os.listdir(score_folder)
    new_files = [f for f in files_found if f not in processed_files and os.path.isfile(os.path.join(score_folder, f))]

    print(f"APT m14: Found {len(files_found)} total files, {len(new_files)} new files to process")

    # Process only new files
    if new_files:
        print(f"APT m14: Processing new files: {new_files}")
        # Create a mini score folder with just new files for processing
        new_results = []
        for fname in new_files:
            fpath = os.path.join(score_folder, fname)
            # Process single file (reuse m8 logic but for single file)
            try:
                x1a = m0_convert_dng(fpath)
                if x1a is None:
                    continue

                y2 = m2_upload_image(x1a)

                # Skip API call if file is too large or already processed
                import base64
                from PIL import Image
                if not os.path.exists(y2) or os.path.getsize(y2) == 0:
                    continue

                file_size = os.path.getsize(y2)
                if file_size > 5 * 1024 * 1024:  # 5MB
                    try:
                        img = Image.open(y2)
                        img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                        temp_path = y2.replace('.png', '_resized.png').replace('.jpg', '_resized.jpg')
                        img.save(temp_path, optimize=True, quality=85)
                        y2 = temp_path
                    except Exception as resize_error:
                        print(f"APT m14: Resize failed for {fname}: {resize_error}")
                        continue

                with open(y2, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')

                # API call
                from llama_api_client import LlamaAPIClient
                try:
                    client = LlamaAPIClient()
                    response = client.chat.completions.create(
                        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                        messages=[{
                            "role": "user",
                            "content": [{
                                "type": "text",
                                "text": f"Extract all bowling scores, player names, dates, or game information from this image. Image filename: {fname}",
                            }, {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{image_data}"}
                            }]
                        }]
                    )
                    y4 = response.completion_message.content.text
                except Exception as api_error:
                    y4 = f"API Error: {api_error}"

                y6 = m6_extract_exif_metadata(y2)

                new_results.append({
                    "filename": fname,
                    "llama_data": y4,
                    "exif": y6
                })

            except Exception as err:
                print(f"APT m14: Error processing {fname}: {err}")
                new_results.append({
                    "filename": fname,
                    "llama_data": f"Error: {err}",
                    "exif": ""
                })

        # Save new results to records
        if new_results:
            updated_records = m12_save_bowling_records(new_results, records_file)

    # Convert all records back to structured format for the leaderboard
    all_results = []
    for game in records['games']:
        # Pass the structured game data directly (includes 'players' array)
        all_results.append(game)

    return all_results

# m15: Image cleanup module (APT-compliant) - Safely removes processed images
def m15_cleanup_processed_images(score_folder, records_file="bowling_records.json"):
    """
    APT Module: m15
    Input: score_folder (path), records_file (path)
    Output: y15 (cleanup summary)
    Equation: y15 = m15(score_folder, records_file)
    """
    import os

    # Load records to see what's been processed
    records = m13_load_bowling_records(records_file)
    processed_files = {game['filename'] for game in records['games']}

    if not os.path.exists(score_folder):
        return {"removed": 0, "kept": 0, "error": "Score folder not found"}

    files_found = os.listdir(score_folder)
    removed_count = 0
    kept_count = 0

    for fname in files_found:
        fpath = os.path.join(score_folder, fname)
        if os.path.isfile(fpath):
            if fname in processed_files:
                try:
                    os.remove(fpath)
                    removed_count += 1
                    print(f"APT m15: Removed processed file: {fname}")
                except Exception as e:
                    print(f"APT m15: Error removing {fname}: {e}")
                    kept_count += 1
            else:
                kept_count += 1
                print(f"APT m15: Keeping unprocessed file: {fname}")

    summary = {"removed": removed_count, "kept": kept_count}
    print(f"APT m15: Cleanup complete - removed {removed_count}, kept {kept_count} files")
    return summary

def m7_metadata_outliner(score_folder):
    items = []
    for fname in os.listdir(score_folder):
        fpath = os.path.join(score_folder, fname)
        if os.path.isfile(fpath):
            meta = m6_extract_exif_metadata(fpath)
            items.append(ft.Text(f"{fname}:\n{meta}"))
    return ft.Column([
        ft.Text("All Uploaded Images Metadata Outliner:"),
        ft.ListView(items, height=200)
    ])

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

ft.app(target=main)
