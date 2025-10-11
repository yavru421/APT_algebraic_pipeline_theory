#!/usr/bin/env python3
"""
APT GUI Application using Flet
===============================
Algebraic Pipeline Theory GUI with interactive RAPT expression rendering

Pipeline Equation: GUI_State = m5(m4(m3(m2(m1(x1)), x2)))

Modules:
- m1: RAPT file parsing and tokenization
- m2: Interactive expression rendering with clickable elements
- m3: Workspace tab management
- m4: File/directory navigation
- m5: Terminal/notepad toggle interface
"""

import flet as ft
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Any

class APTGUIApp:
    def __init__(self):
        self.page = None
        self.current_rapt_content = ""
        self.expression_container = None
        self.tabs_container = None
        self.selected_file_text = None

    def main(self, page: ft.Page):
        """Main entry point - initializes the APT GUI"""
        self.page = page
        page.title = "APT GUI - Algebraic Pipeline Theory Interface"
        page.theme_mode = ft.ThemeMode.DARK

        # Module implementations
        file_selector = self.m1_file_selector()
        expression_renderer = self.m2_expression_renderer()
        tab_manager = self.m3_tab_manager()

        # Main layout
        page.add(
            ft.Column([
                ft.Text("APT GUI - Algebraic Pipeline Theory",
                        size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                file_selector,
                ft.Divider(),
                expression_renderer,
                ft.Divider(),
                tab_manager
            ])
        )

    def m1_file_selector(self) -> ft.Column:
        """Module m1: RAPT file selection and parsing"""

        def on_file_picked(e):
            if e.files:
                file_path = e.files[0].path
                self.load_rapt_file(file_path)

        def on_select_current(_):
            current_file = Path("RAPT_PIPELINE.RAPT")
            if current_file.exists():
                self.load_rapt_file(str(current_file.absolute()))

        file_picker = ft.FilePicker(on_result=on_file_picked)
        self.page.overlay.append(file_picker)

        self.selected_file_text = ft.Text("No RAPT file selected", size=14)

        return ft.Column([
            ft.Text("m1: RAPT File Selection", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton(
                    "Select RAPT File",
                    icon=ft.Icons.FOLDER_OPEN,
                    on_click=lambda _: file_picker.pick_files(
                        dialog_title="Select RAPT Pipeline File",
                        file_type=ft.FilePickerFileType.CUSTOM,
                        allowed_extensions=["rapt", "txt"]
                    )
                ),
                ft.ElevatedButton(
                    "Use Current RAPT_PIPELINE.RAPT",
                    icon=ft.Icons.PLAY_ARROW,
                    on_click=on_select_current
                )
            ]),
            self.selected_file_text
        ])

    def m2_expression_renderer(self) -> ft.Column:
        """Module m2: Interactive expression rendering"""
        self.expression_container = ft.Column([
            ft.Text("No expression loaded", size=16)
        ])

        return ft.Column([
            ft.Text("m2: Algebraic Expression Renderer", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=self.expression_container,
                bgcolor=ft.Colors.GREY_900,
                border_radius=8,
                padding=20,
                border=ft.border.all(1, ft.Colors.GREY_700)
            )
        ])

    def m3_tab_manager(self) -> ft.Column:
        """Module m3: Workspace tab management"""
        self.tabs_container = ft.Tabs(
            tabs=[],
            animation_duration=300
        )

        return ft.Column([
            ft.Text("m3: Workspace Tabs", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=self.tabs_container,
                height=400,
                border=ft.border.all(1, ft.Colors.GREY_700),
                border_radius=8
            )
        ])

    def load_rapt_file(self, file_path: str):
        """Load and parse RAPT file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.current_rapt_content = f.read()

            self.selected_file_text.value = f"Loaded: {Path(file_path).name}"
            self.parse_and_render_expression()
            self.page.update()

        except Exception as e:
            self.selected_file_text.value = f"Error loading file: {e}"
            self.page.update()

    def parse_and_render_expression(self):
        """Parse RAPT content and render interactive expression"""
        # Extract the main equation (Y = ...)
        equation_match = re.search(r'Y\s*=\s*(.+)', self.current_rapt_content)
        if not equation_match:
            self.expression_container.controls = [
                ft.Text("No Y = equation found in RAPT file", color=ft.Colors.RED)
            ]
            return

        equation = equation_match.group(1).strip()

        # Parse the equation into clickable components
        components = self.parse_equation_components(equation)

        # Create interactive expression display
        expression_row = ft.Row([], wrap=True, spacing=5)

        for component in components:
            if component['type'] == 'module':
                btn = ft.ElevatedButton(
                    text=component['text'],
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE
                    ),
                    on_click=lambda e, comp=component: self.on_component_click(comp)
                )
                expression_row.controls.append(btn)
            elif component['type'] == 'variable':
                btn = ft.ElevatedButton(
                    text=component['text'],
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE
                    ),
                    on_click=lambda e, comp=component: self.on_component_click(comp)
                )
                expression_row.controls.append(btn)
            else:
                # Operators and syntax
                expression_row.controls.append(
                    ft.Text(component['text'], size=16, color=ft.Colors.WHITE)
                )

        self.expression_container.controls = [
            ft.Text("Y = ", size=20, weight=ft.FontWeight.BOLD),
            expression_row
        ]

    def parse_equation_components(self, equation: str) -> List[Dict[str, str]]:
        """Parse equation into clickable components"""
        components = []

        # Simple tokenization - enhanced for RAPT syntax
        tokens = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*|\(|\)|=|,|@|"[^"]*"|\S)', equation)

        for token in tokens:
            if re.match(r'^m\d+$', token):  # Module like m0, m1, etc.
                components.append({'type': 'module', 'text': token})
            elif re.match(r'^x\d+$', token):  # Variable like x1, x2, etc.
                components.append({'type': 'variable', 'text': token})
            elif token.startswith('"') and token.endswith('"'):  # String literal
                components.append({'type': 'string', 'text': token})
            else:  # Operators, parentheses, etc.
                components.append({'type': 'syntax', 'text': token})

        return components

    def on_component_click(self, component: Dict[str, str]):
        """Handle clicks on expression components"""
        comp_name = component['text']

        if component['type'] == 'module':
            # Open module file in workspace tab
            module_file = f"APT_MODULES/{comp_name}.py"
            self.create_workspace_tab(comp_name, module_file, "APT_MODULES")

        elif component['type'] == 'variable':
            # Try to resolve variable from RAPT file
            var_match = re.search(f'{comp_name}\\s*=\\s*"([^"]*)"', self.current_rapt_content)
            if var_match:
                file_path = var_match.group(1)
                self.create_workspace_tab(comp_name, file_path, ".")

    def create_workspace_tab(self, tab_name: str, file_path: str, root_dir: str):
        """Module m4 & m5: Create workspace tab with file/terminal interface"""

        # File content display
        file_content = ft.Text("", selectable=True, size=12)

        # Load file if it exists
        full_path = Path(root_dir) / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                file_content.value = content[:2000] + "..." if len(content) > 2000 else content
            except:
                file_content.value = f"Could not read file: {full_path}"
        else:
            file_content.value = f"File not found: {full_path}\\nExpected path: {full_path.absolute()}"

        # Directory listing
        dir_list = ft.ListView(height=150, spacing=2)
        try:
            root_path = Path(root_dir).absolute()
            for item in sorted(root_path.iterdir())[:10]:  # Limit to first 10 items
                dir_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(item.name, size=12),
                        leading=ft.Icon(ft.Icons.FOLDER if item.is_dir() else ft.Icons.DESCRIPTION),
                        dense=True
                    )
                )
        except Exception as e:
            dir_list.controls.append(ft.Text(f"Could not list directory: {e}"))

        # Terminal output and input
        terminal_output = ft.Text("Terminal ready...", size=12, color=ft.Colors.GREEN_400)
        terminal_input = ft.TextField(
            hint_text="Enter command...",
            size=12,
            on_submit=lambda e: self.run_terminal_command(e.control.value, terminal_output, root_dir, e.control)
        )

        # File view
        file_view = ft.Column([
            ft.Text(f"File: {file_path}", weight=ft.FontWeight.BOLD, size=14),
            ft.Container(
                content=ft.Column([file_content], scroll=ft.ScrollMode.AUTO),
                height=250,
                border=ft.border.all(1, ft.Colors.GREY_600),
                padding=10
            )
        ])

        # Terminal view
        terminal_view = ft.Column([
            ft.Text("Terminal", weight=ft.FontWeight.BOLD, size=14),
            ft.Container(
                content=terminal_output,
                height=200,
                border=ft.border.all(1, ft.Colors.GREY_600),
                padding=10,
                bgcolor=ft.Colors.BLACK
            ),
            terminal_input
        ])

        # Current view container
        current_view = ft.Container(content=file_view)

        def toggle_view(view_type):
            if view_type == "file":
                current_view.content = file_view
            else:
                current_view.content = terminal_view
            self.page.update()

        # Tab content
        tab_content = ft.Column([
            ft.Row([
                ft.ElevatedButton("File View", on_click=lambda _: toggle_view("file"), height=30),
                ft.ElevatedButton("Terminal View", on_click=lambda _: toggle_view("terminal"), height=30)
            ]),
            ft.Text(f"Directory: {root_dir}", size=12, color=ft.Colors.GREY_400),
            ft.Container(
                content=dir_list,
                border=ft.border.all(1, ft.Colors.GREY_600),
                border_radius=4
            ),
            current_view
        ])

        # Create and add tab
        new_tab = ft.Tab(
            text=tab_name,
            content=tab_content
        )

        self.tabs_container.tabs.append(new_tab)
        self.page.update()

    def run_terminal_command(self, command: str, output_widget: ft.Text, working_dir: str, input_widget: ft.TextField):
        """Execute terminal command and display output"""
        if not command.strip():
            return

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            output_text = f"$ {command}\\n{result.stdout}"
            if result.stderr:
                output_text += f"\\nERROR: {result.stderr}"

            output_widget.value = output_text
            output_widget.color = ft.Colors.GREEN_400 if result.returncode == 0 else ft.Colors.RED_400

        except subprocess.TimeoutExpired:
            output_widget.value = f"$ {command}\\nCommand timed out"
            output_widget.color = ft.Colors.ORANGE_400
        except Exception as e:
            output_widget.value = f"$ {command}\\nError: {e}"
            output_widget.color = ft.Colors.RED_400

        # Clear input and update
        input_widget.value = ""
        self.page.update()

def main():
    """Pipeline Entry Point"""
    app = APTGUIApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()