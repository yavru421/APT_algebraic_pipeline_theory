"""
APT Flet Dashboard - Clean, Functional Implementation

Pipeline Equation:
    y_results = m3(m2(m1(x_input)))

m1: Process user input (instruction parsing)
m2: Execute APT pipeline (load, extract, rewrite, trace, persist)
m3: Display results (update UI with pipeline output)

Contract:
  Inputs: x_input (user instruction)
  Outputs: y_results (pipeline execution results)
  Modules: m1 (parse), m2 (execute), m3 (display)
"""

import flet as ft
import os
import datetime
import json
from apt_pipeline_pkg.apt_modules import m1_load_state, m2_extract_eq, m3_llm_rewrite, m4_sim_trace, m5_persist

class APTDashboard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.results = []
        self.setup_ui()

    def setup_ui(self):
        self.page.title = "APT Pipeline Dashboard"
        self.page.bgcolor = "#1e1e1e"
        self.page.scroll = ft.ScrollMode.AUTO

        # Input section
        self.instruction_input = ft.TextField(
            label="Pipeline Instruction",
            hint_text="Enter your APT instruction here...",
            bgcolor="#2d2d2d",
            color="#ffffff",
            expand=True,
            on_submit=self.execute_pipeline
        )

        # Execute button
        self.execute_btn = ft.ElevatedButton(
            "Execute Pipeline",
            on_click=self.execute_pipeline,
            bgcolor="#0d7377",
            color="#ffffff"
        )

        # Results display
        self.results_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=ft.padding.all(10)
        )

        # Status bar
        self.status_bar = ft.Container(
            content=ft.Text("Ready", color="#ffffff"),
            bgcolor="#0d7377",
            padding=10,
            height=40
        )

        # Layout
        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("APT Pipeline Dashboard", size=24, weight=ft.FontWeight.BOLD, color="#ffffff"),
                    ft.Row([self.instruction_input, self.execute_btn]),
                    ft.Container(
                        content=self.results_list,
                        bgcolor="#2d2d2d",
                        border_radius=10,
                        padding=10,
                        expand=True
                    ),
                    self.status_bar
                ]),
                padding=20,
                expand=True
            )
        )

    def m1_parse_input(self, instruction: str) -> dict:
        """Parse user instruction into APT format"""
        return {
            "instruction": instruction,
            "timestamp": datetime.datetime.now().isoformat(),
            "pipeline_equation": f"y_result = m3(m2(m1('{instruction}')))"
        }

    def m2_execute_apt_pipeline(self, parsed_input: dict) -> dict:
        """Execute the full APT pipeline"""
        try:
            # Load state
            state_file = os.path.join(os.getcwd(), ".apt_dashboard_state.json")
            state = m1_load_state(state_file)

            # Extract and process equation
            eq0 = m2_extract_eq(state, parsed_input["pipeline_equation"])
            eq1 = m3_llm_rewrite(eq0)
            trace = m4_sim_trace(eq1)
            out_dir = m5_persist(state, eq1, trace)

            return {
                "success": True,
                "original_equation": eq0,
                "rewritten_equation": eq1,
                "trace": trace,
                "output_directory": out_dir,
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            }

    def m3_display_results(self, result: dict):
        """Display pipeline results in UI"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        if result["success"]:
            result_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"✅ Pipeline Executed - {timestamp}", weight=ft.FontWeight.BOLD, color="#4CAF50"),
                        ft.Text(f"Original: {result['original_equation']}", color="#ffffff"),
                        ft.Text(f"Rewritten: {result['rewritten_equation']}", color="#ffffff"),
                        ft.Text(f"Output: {result['output_directory']}", color="#ffffff"),
                        ft.Text(f"Trace Steps: {len(result['trace'])}", color="#ffffff"),
                    ]),
                    padding=15
                ),
                color="#2d2d2d"
            )
        else:
            result_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"❌ Pipeline Failed - {timestamp}", weight=ft.FontWeight.BOLD, color="#f44336"),
                        ft.Text(f"Error: {result['error']}", color="#ffffff"),
                    ]),
                    padding=15
                ),
                color="#2d2d2d"
            )

        self.results_list.controls.insert(0, result_card)
        if len(self.results_list.controls) > 10:  # Keep only last 10 results
            self.results_list.controls.pop()

        self.results_list.update()

    def execute_pipeline(self, e):
        """Main pipeline execution: y_results = m3(m2(m1(x_input)))"""
        instruction = self.instruction_input.value.strip()
        if not instruction:
            return

        # Update status
        self.status_bar.content.value = "Executing pipeline..."
        self.status_bar.update()

        try:
            # APT Pipeline: y_results = m3(m2(m1(x_input)))
            parsed = self.m1_parse_input(instruction)  # m1
            result = self.m2_execute_apt_pipeline(parsed)  # m2
            self.m3_display_results(result)  # m3

            # Clear input
            self.instruction_input.value = ""
            self.instruction_input.update()

            # Update status
            status = "✅ Success" if result["success"] else "❌ Failed"
            self.status_bar.content.value = status

        except Exception as e:
            self.status_bar.content.value = f"❌ Error: {str(e)}"

        self.status_bar.update()

def main(page: ft.Page):
    dashboard = APTDashboard(page)

if __name__ == "__main__":
    ft.app(target=main)