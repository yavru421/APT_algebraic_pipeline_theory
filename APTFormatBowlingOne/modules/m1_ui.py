# m1: UI module (APT-compliant)
# Input: x2 (schedule_events), file_picker, cleanup_callback -> Output: y1 (UI components)
# Equation: y1 = m1(x2, file_picker, cleanup_callback)

import flet as ft

def m1_schedule_ui(schedule_events, file_picker, cleanup_callback=None):
    """
    APT Module: m1
    Input: schedule_events (List), file_picker (FilePicker), cleanup_callback (Callable)
    Output: UI (Column) - Rendered UI components
    Equation: y1 = m1(x2, file_picker, cleanup_callback)

    Description: Creates main UI interface with file upload and cleanup functionality
    """

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
        ft.Text(f"Weekly Event: Tuesdays at 7:00 PM"),
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