"""
APT Flet Dashboard - TRUE APT METHODOLOGY
========================================

🚀 PURE APT ALGEBRAIC PIPELINE IMPLEMENTATION:
- Single unified pipeline equation: Y = m6(m5(m4(m3(m2(m1(X))))))
- Explicit variable definitions (x1, x2, y1, y2, etc.)
- Algebraic error handling (no scattered try-catch)
- Deterministic module contracts
- Unified state management

Pipeline Equation: Y_dashboard = m6_status(m5_persist(m4_execute(m3_connect(m2_ui(m1_init(X_startup))))))

Contract:
  X_startup = {context_dirs: List[str], server_url: str, ui_config: Dict}
  Y_dashboard = {ui_state: Dict, server_connection: bool, execution_results: List}

Module Contracts:
  m1_init: X_startup → y1_system_state
  m2_ui: y1_system_state → y2_ui_components
  m3_connect: y2_ui_components → y3_connected_system
  m4_execute: y3_connected_system + x_instruction → y4_results
  m5_persist: y4_results → y5_persisted_state
  m6_status: y5_persisted_state → Y_dashboard

Usage: python apt_flet_dashboard.py
"""

import asyncio
import json
import datetime
import time
import os
import logging
import threading
from typing import Dict, Any, List, Optional, Tuple
import flet as ft
import requests

# ============================================================================
# APT MODULE DEFINITIONS - PURE ALGEBRAIC IMPLEMENTATION
# ============================================================================

class APTModule:
    """Base class for all APT modules with algebraic contracts"""

    def __init__(self, module_name: str):
        self.module_name = module_name
        self.execution_log = []

    def log_execution(self, inputs: Dict[str, Any], outputs: Dict[str, Any], success: bool):
        """Log module execution for traceability"""
        self.execution_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "module": self.module_name,
            "inputs": inputs,
            "outputs": outputs,
            "success": success
        })

class APTError:
    """Algebraic error representation instead of exceptions"""

    def __init__(self, module: str, error_type: str, message: str, recovery_action: str = None):
        self.module = module
        self.error_type = error_type
        self.message = message
        self.recovery_action = recovery_action
        self.timestamp = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module": self.module,
            "error_type": self.error_type,
            "message": self.message,
            "recovery_action": self.recovery_action,
            "timestamp": self.timestamp
        }

# ============================================================================
# APT MODULE m1: SYSTEM INITIALIZATION
# ============================================================================

class M1_SystemInit(APTModule):
    """
    APT Module m1: System Initialization

    Contract:
      Inputs: x_startup = {context_dirs, server_url, ui_config}
      Outputs: y1_system_state = {platform_info, context_files, init_success}
      Errors: APTError with recovery actions
      Success: Complete system state ready for UI construction

    Algebraic: y1 = m1(x_startup)
    """

    def __init__(self):
        super().__init__("m1_system_init")

    def execute(self, x_startup: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[APTError]]:
        """Execute m1 with algebraic error handling"""
        inputs = {"x_startup": x_startup}

        # Extract startup parameters
        context_dirs = x_startup.get("context_dirs", ["context_files", "context", "docs"])
        server_url = x_startup.get("server_url", "http://localhost:8000")
        ui_config = x_startup.get("ui_config", {})

        # Scan context directories
        context_files = {}
        for dirname in context_dirs:
            if os.path.exists(dirname) and os.path.isdir(dirname):
                files = [f for f in os.listdir(dirname) if f.endswith(('.txt', '.md', '.json'))]
                if files:
                    context_files[dirname] = files

        # Build system state
        y1_system_state = {
            "platform_info": {
                "os": os.name,
                "cwd": os.getcwd(),
                "python_version": "3.12+"
            },
            "context_files": context_files,
            "server_url": server_url,
            "ui_config": ui_config,
            "init_timestamp": time.time(),
            "init_success": True
        }

        self.log_execution(inputs, {"y1_system_state": y1_system_state}, True)
        return y1_system_state, None

# ============================================================================
# APT MODULE m2: UI COMPONENT CONSTRUCTION
# ============================================================================

class M2_UIConstruction(APTModule):
    """
    APT Module m2: UI Component Construction

    Contract:
      Inputs: y1_system_state
      Outputs: y2_ui_components = {page, status_bar, input_field, output_field, etc.}
      Errors: APTError for UI construction failures
      Success: Complete UI component tree ready for display

    Algebraic: y2 = m2(y1)
    """

    def __init__(self):
        super().__init__("m2_ui_construction")
        self.ui_components = {}

    def execute(self, y1_system_state: Dict[str, Any], page: ft.Page) -> Tuple[Dict[str, Any], Optional[APTError]]:
        """Execute m2 with UI component construction"""
        inputs = {"y1_system_state": y1_system_state}

        # Configure page
        page.title = "APT Dashboard - Pure Algebraic"
        page.bgcolor = "#181C24"
        page.scroll = ft.ScrollMode.AUTO

        # Status components (for m6)
        status_icon = ft.Icon(ft.Icons.CIRCLE, color="#FF5555", size=16)
        status_text = ft.Text("m1: Initializing...", color="#F8F8F2", size=14, weight=ft.FontWeight.BOLD)

        # Input components (for m4)
        instruction_input = ft.TextField(
            label="APT Instruction Pipeline",
            hint_text="Enter algebraic instruction: e.g., 'Y = analyze(X_context)'",
            expand=True,
            bgcolor="#232936",
            color="#F8F8F2",
            border_color="#444857"
        )

        # Output components (for m5)
        pipeline_display = ft.TextField(
            label="Current Pipeline Equation",
            value="Y = m6(m5(m4(m3(m2(m1(X))))))",
            read_only=True,
            bgcolor="#232936",
            color="#8BE9FD",
            border_color="#444857"
        )

        result_output = ft.TextField(
            label="Pipeline Execution Results",
            multiline=True,
            min_lines=8,
            read_only=True,
            bgcolor="#232936",
            color="#F8F8F2",
            border_color="#444857"
        )

        execution_log = ft.TextField(
            label="APT Module Execution Log",
            multiline=True,
            min_lines=6,
            read_only=True,
            bgcolor="#232936",
            color="#50FA7B",
            border_color="#444857"
        )

        # Build UI tree
        y2_ui_components = {
            "page": page,
            "status_icon": status_icon,
            "status_text": status_text,
            "instruction_input": instruction_input,
            "pipeline_display": pipeline_display,
            "result_output": result_output,
            "execution_log": execution_log,
            "context_info": f"Context files: {len(y1_system_state['context_files'])} directories",
            "construction_success": True
        }

        self.ui_components = y2_ui_components
        self.log_execution(inputs, {"y2_ui_components": "constructed"}, True)
        return y2_ui_components, None

# ============================================================================
# APT MODULE m3: SERVER CONNECTION
# ============================================================================

class M3_ServerConnection(APTModule):
    """
    APT Module m3: Server Connection Management

    Contract:
      Inputs: y2_ui_components
      Outputs: y3_connected_system = {ui_components, server_status, connection_time}
      Errors: APTError for connection failures with recovery actions
      Success: Established server connection ready for pipeline execution

    Algebraic: y3 = m3(y2)
    """

    def __init__(self):
        super().__init__("m3_server_connection")

    def execute(self, y2_ui_components: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[APTError]]:
        """Execute m3 with algebraic server connection"""
        inputs = {"y2_ui_components": "ui_components_ready"}

        # Extract server URL from UI components or use default
        server_url = "http://localhost:8000"

        # Algebraic connection attempt
        connection_start = time.time()
        server_status = self._attempt_connection(server_url)
        connection_time = time.time() - connection_start

        if server_status["connected"]:
            y3_connected_system = {
                **y2_ui_components,
                "server_status": server_status,
                "server_url": server_url,
                "connection_time": connection_time,
                "connection_success": True
            }

            # Update status in UI
            y2_ui_components["status_icon"].color = "#50FA7B"  # Green
            y2_ui_components["status_text"].value = f"m3: Connected to server ({connection_time:.2f}s)"

            self.log_execution(inputs, {"y3_connected_system": "connected"}, True)
            return y3_connected_system, None
        else:
            # Algebraic error representation
            error = APTError(
                module="m3_server_connection",
                error_type="connection_failed",
                message=f"Cannot connect to {server_url}: {server_status.get('error', 'Unknown error')}",
                recovery_action="Start MCP server with: uvicorn apt_mcp_server_simple:app --port 8000"
            )

            # Still return partial system for graceful degradation
            y3_connected_system = {
                **y2_ui_components,
                "server_status": server_status,
                "server_url": server_url,
                "connection_time": connection_time,
                "connection_success": False
            }

            # Update status in UI
            y2_ui_components["status_icon"].color = "#FF5555"  # Red
            y2_ui_components["status_text"].value = f"m3: Server disconnected ({connection_time:.2f}s)"

            self.log_execution(inputs, {"y3_connected_system": "disconnected"}, False)
            return y3_connected_system, error

    def _attempt_connection(self, server_url: str) -> Dict[str, Any]:
        """Attempt server connection with proper timeout"""
        try:
            response = requests.get(f"{server_url}/health", timeout=30)  # Increased timeout
            if response.status_code == 200:
                return {
                    "connected": True,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "server_info": response.json()
                }
            else:
                return {
                    "connected": False,
                    "status_code": response.status_code,
                    "error": f"Server returned {response.status_code}"
                }
        except requests.exceptions.Timeout:
            return {
                "connected": False,
                "error": "Connection timeout (30s) - Server may be busy",
                "timeout": True
            }
        except requests.exceptions.ConnectionError as e:
            return {
                "connected": False,
                "error": f"Connection error: {str(e)}",
                "connection_error": True
            }
        except Exception as e:
            return {
                "connected": False,
                "error": f"Unexpected error: {str(e)}"
            }

# ============================================================================
# APT MODULE m4: PIPELINE EXECUTION ENGINE
# ============================================================================

class M4_PipelineExecution(APTModule):
    """
    APT Module m4: Pipeline Execution Engine

    Contract:
      Inputs: y3_connected_system + x_instruction
      Outputs: y4_results = {instruction, execution_trace, server_response, success}
      Errors: APTError for execution failures
      Success: Complete pipeline execution with full trace

    Algebraic: y4 = m4(y3, x_instruction)
    """

    def __init__(self):
        super().__init__("m4_pipeline_execution")

    def execute(self, y3_connected_system: Dict[str, Any], x_instruction: str) -> Tuple[Dict[str, Any], Optional[APTError]]:
        """Execute m4 with full pipeline execution"""
        inputs = {"y3_connected_system": "system_ready", "x_instruction": x_instruction}

        if not y3_connected_system["connection_success"]:
            error = APTError(
                module="m4_pipeline_execution",
                error_type="no_server_connection",
                message="Cannot execute pipeline without server connection",
                recovery_action="Fix server connection in m3 first"
            )

            y4_results = {
                "instruction": x_instruction,
                "execution_trace": [],
                "server_response": None,
                "success": False,
                "error": error.to_dict()
            }

            self.log_execution(inputs, {"y4_results": "failed_no_connection"}, False)
            return y4_results, error

        # Execute pipeline on server
        server_url = y3_connected_system["server_url"]
        execution_trace = []

        try:
            # Parse instruction
            execution_trace.append({"step": "parse", "status": "starting", "timestamp": time.time()})
            parse_response = requests.post(
                f"{server_url}/v1/parse_instruction",
                json={"prompt": x_instruction},
                timeout=30  # Increased timeout
            )
            execution_trace.append({"step": "parse", "status": "completed", "response_code": parse_response.status_code})

            # Execute via chat completions
            execution_trace.append({"step": "execute", "status": "starting", "timestamp": time.time()})
            chat_response = requests.post(
                f"{server_url}/v1/chat/completions",
                json={"prompt": x_instruction},
                timeout=45  # Increased timeout for complex operations
            )
            execution_trace.append({"step": "execute", "status": "completed", "response_code": chat_response.status_code})

            if parse_response.status_code == 200 and chat_response.status_code == 200:
                parse_data = parse_response.json()
                chat_data = chat_response.json()

                y4_results = {
                    "instruction": x_instruction,
                    "execution_trace": execution_trace,
                    "server_response": {
                        "equation": parse_data.get("apt_equation", ""),
                        "result": chat_data.get("result", ""),
                        "processing_time": chat_data.get("processing_time", 0)
                    },
                    "success": True
                }

                self.log_execution(inputs, {"y4_results": "success"}, True)
                return y4_results, None
            else:
                error = APTError(
                    module="m4_pipeline_execution",
                    error_type="server_error",
                    message=f"Server error: parse={parse_response.status_code}, chat={chat_response.status_code}",
                    recovery_action="Check server logs and API endpoints"
                )

                y4_results = {
                    "instruction": x_instruction,
                    "execution_trace": execution_trace,
                    "server_response": None,
                    "success": False,
                    "error": error.to_dict()
                }

                self.log_execution(inputs, {"y4_results": "server_error"}, False)
                return y4_results, error

        except Exception as e:
            error = APTError(
                module="m4_pipeline_execution",
                error_type="execution_exception",
                message=f"Pipeline execution failed: {str(e)}",
                recovery_action="Check network connection and server availability"
            )

            y4_results = {
                "instruction": x_instruction,
                "execution_trace": execution_trace,
                "server_response": None,
                "success": False,
                "error": error.to_dict()
            }

            self.log_execution(inputs, {"y4_results": "exception"}, False)
            return y4_results, error

# ============================================================================
# APT MODULE m5: STATE PERSISTENCE
# ============================================================================

class M5_StatePersistence(APTModule):
    """
    APT Module m5: State Persistence Management

    Contract:
      Inputs: y4_results
      Outputs: y5_persisted_state = {results, saved_state, persistence_success}
      Errors: APTError for persistence failures
      Success: State successfully persisted with backup

    Algebraic: y5 = m5(y4)
    """

    def __init__(self):
        super().__init__("m5_state_persistence")
        self.state_file = ".apt_dashboard_state.json"

    def execute(self, y4_results: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[APTError]]:
        """Execute m5 with state persistence"""
        inputs = {"y4_results": "execution_completed"}

        try:
            # Load existing state
            existing_state = self._load_existing_state()

            # Add new execution to history
            execution_history = existing_state.get("execution_history", [])
            execution_history.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "instruction": y4_results["instruction"],
                "success": y4_results["success"],
                "result": y4_results.get("server_response", {}).get("result", ""),
                "execution_trace": y4_results["execution_trace"]
            })

            # Keep only last 50 executions
            execution_history = execution_history[-50:]

            # Build new state
            new_state = {
                "execution_history": execution_history,
                "last_instruction": y4_results["instruction"],
                "last_success": y4_results["success"],
                "save_timestamp": datetime.datetime.now().isoformat()
            }

            # Save state
            with open(self.state_file, 'w') as f:
                json.dump(new_state, f, indent=2)

            y5_persisted_state = {
                "results": y4_results,
                "saved_state": new_state,
                "persistence_success": True,
                "state_file": self.state_file
            }

            self.log_execution(inputs, {"y5_persisted_state": "saved"}, True)
            return y5_persisted_state, None

        except Exception as e:
            error = APTError(
                module="m5_state_persistence",
                error_type="persistence_failed",
                message=f"Failed to save state: {str(e)}",
                recovery_action="Check file permissions and disk space"
            )

            y5_persisted_state = {
                "results": y4_results,
                "saved_state": None,
                "persistence_success": False,
                "error": error.to_dict()
            }

            self.log_execution(inputs, {"y5_persisted_state": "failed"}, False)
            return y5_persisted_state, error

    def _load_existing_state(self) -> Dict[str, Any]:
        """Load existing state file"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

# ============================================================================
# APT MODULE m6: STATUS AND UI UPDATE
# ============================================================================

class M6_StatusUpdate(APTModule):
    """
    APT Module m6: Status and UI Update

    Contract:
      Inputs: y5_persisted_state
      Outputs: Y_dashboard = {final_ui_state, status_updated, dashboard_ready}
      Errors: APTError for UI update failures
      Success: Complete dashboard with updated status and results

    Algebraic: Y = m6(y5)
    """

    def __init__(self):
        super().__init__("m6_status_update")

    def execute(self, y5_persisted_state: Dict[str, Any], ui_components: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[APTError]]:
        """Execute m6 with UI status updates"""
        inputs = {"y5_persisted_state": "state_persisted"}

        try:
            results = y5_persisted_state["results"]

            # Update pipeline display
            if results["success"] and results["server_response"]:
                equation = results["server_response"].get("equation", "Y = m6(m5(m4(m3(m2(m1(X))))))")
                ui_components["pipeline_display"].value = equation
                ui_components["pipeline_display"].update()

            # Update result output
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            if results["success"]:
                result_text = results["server_response"]["result"]
                processing_time = results["server_response"]["processing_time"]
                new_result = f"[{timestamp}] ✅ SUCCESS: {result_text}\n⏱️ Processing: {processing_time:.2f}s\n\n"
            else:
                error_info = results.get("error", {})
                new_result = f"[{timestamp}] ❌ ERROR: {error_info.get('message', 'Unknown error')}\n💡 Recovery: {error_info.get('recovery_action', 'No action specified')}\n\n"

            current_results = ui_components["result_output"].value or ""
            ui_components["result_output"].value = current_results + new_result
            ui_components["result_output"].update()

            # Update execution log
            trace_text = f"[{timestamp}] Module execution trace:\n"
            for step in results["execution_trace"]:
                trace_text += f"  • {step}\n"
            trace_text += "\n"

            current_log = ui_components["execution_log"].value or ""
            ui_components["execution_log"].value = current_log + trace_text
            ui_components["execution_log"].update()

            # Update status
            if results["success"]:
                ui_components["status_text"].value = "m6: ✅ Pipeline execution complete"
                ui_components["status_icon"].color = "#50FA7B"
            else:
                ui_components["status_text"].value = "m6: ❌ Pipeline execution failed"
                ui_components["status_icon"].color = "#FF5555"

            ui_components["status_text"].update()
            ui_components["status_icon"].update()

            Y_dashboard = {
                "final_ui_state": ui_components,
                "status_updated": True,
                "dashboard_ready": True,
                "execution_summary": {
                    "instruction": results["instruction"],
                    "success": results["success"],
                    "timestamp": timestamp
                }
            }

            self.log_execution(inputs, {"Y_dashboard": "complete"}, True)
            return Y_dashboard, None

        except Exception as e:
            error = APTError(
                module="m6_status_update",
                error_type="ui_update_failed",
                message=f"Failed to update UI: {str(e)}",
                recovery_action="Check UI component references"
            )

            Y_dashboard = {
                "final_ui_state": ui_components,
                "status_updated": False,
                "dashboard_ready": False,
                "error": error.to_dict()
            }

            self.log_execution(inputs, {"Y_dashboard": "failed"}, False)
            return Y_dashboard, error

# ============================================================================
# APT PIPELINE ORCHESTRATOR
# ============================================================================

class APTPipelineOrchestrator:
    """
    APT Pipeline Orchestrator - Executes the complete algebraic pipeline

    Pipeline Equation: Y = m6(m5(m4(m3(m2(m1(X))))))
    """

    def __init__(self):
        self.m1 = M1_SystemInit()
        self.m2 = M2_UIConstruction()
        self.m3 = M3_ServerConnection()
        self.m4 = M4_PipelineExecution()
        self.m5 = M5_StatePersistence()
        self.m6 = M6_StatusUpdate()

        self.execution_errors = []
        self.current_state = None

    async def execute_full_pipeline(self, page: ft.Page) -> Dict[str, Any]:
        """Execute the complete APT pipeline"""

        # X_startup: Initial input
        X_startup = {
            "context_dirs": ["context_files", "context", "docs"],
            "server_url": "http://localhost:8000",
            "ui_config": {"theme": "dark", "debug": False}
        }

        # m1: System initialization
        y1, error1 = self.m1.execute(X_startup)
        if error1:
            self.execution_errors.append(error1)

        # m2: UI construction
        y2, error2 = self.m2.execute(y1, page)
        if error2:
            self.execution_errors.append(error2)

        # Build and display UI
        self._build_ui_layout(page, y2)

        # m3: Server connection
        y3, error3 = self.m3.execute(y2)
        if error3:
            self.execution_errors.append(error3)

        # Store current state for instruction execution
        self.current_state = y3

        return {
            "pipeline_state": y3,
            "errors": [e.to_dict() for e in self.execution_errors],
            "success": len(self.execution_errors) == 0
        }

    async def execute_instruction(self, instruction: str) -> Dict[str, Any]:
        """Execute instruction through m4→m5→m6"""
        if not self.current_state:
            return {"error": "Pipeline not initialized"}

        # m4: Pipeline execution
        y4, error4 = self.m4.execute(self.current_state, instruction)
        if error4:
            self.execution_errors.append(error4)

        # m5: State persistence
        y5, error5 = self.m5.execute(y4)
        if error5:
            self.execution_errors.append(error5)

        # m6: Status update
        Y_final, error6 = self.m6.execute(y5, self.current_state)
        if error6:
            self.execution_errors.append(error6)

        return Y_final

    def _build_ui_layout(self, page: ft.Page, y2_ui_components: Dict[str, Any]):
        """Build the complete UI layout"""

        # Status bar
        status_bar = ft.Container(
            content=ft.Row([
                y2_ui_components["status_icon"],
                y2_ui_components["status_text"],
                ft.ElevatedButton(
                    "Refresh Connection",
                    on_click=lambda e: asyncio.create_task(self._refresh_connection()),
                    bgcolor="#6272A4",
                    color="#F8F8F2",
                    height=30
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor="#232936",
            padding=16,
            margin=ft.margin.only(bottom=16),
            border_radius=8
        )

        # Main content
        main_content = ft.Column([
            ft.Text("APT Dashboard - Pure Algebraic Pipeline", size=24, weight=ft.FontWeight.BOLD, color="#8BE9FD"),
            ft.Divider(color="#444857"),
            status_bar,

            # Pipeline control
            ft.Container(
                content=ft.Column([
                    ft.Text("Pipeline Control", size=18, weight=ft.FontWeight.BOLD, color="#50FA7B"),
                    y2_ui_components["pipeline_display"],
                    ft.Row([
                        y2_ui_components["instruction_input"],
                        ft.ElevatedButton(
                            "Execute Pipeline",
                            on_click=lambda e: asyncio.create_task(self._handle_instruction()),
                            bgcolor="#50FA7B",
                            color="#282A36",
                            height=50
                        )
                    ]),
                    ft.Text(y2_ui_components["context_info"], color="#6272A4")
                ], spacing=12),
                bgcolor="#232936",
                padding=16,
                border_radius=8,
                margin=ft.margin.only(bottom=16)
            ),

            # Results
            ft.Container(
                content=ft.Column([
                    ft.Text("Pipeline Results", size=18, weight=ft.FontWeight.BOLD, color="#F1FA8C"),
                    y2_ui_components["result_output"]
                ], spacing=12),
                bgcolor="#232936",
                padding=16,
                border_radius=8,
                margin=ft.margin.only(bottom=16)
            ),

            # Execution log
            ft.Container(
                content=ft.Column([
                    ft.Text("APT Module Execution Log", size=18, weight=ft.FontWeight.BOLD, color="#BD93F9"),
                    y2_ui_components["execution_log"]
                ], spacing=12),
                bgcolor="#232936",
                padding=16,
                border_radius=8
            )
        ], spacing=16, scroll=ft.ScrollMode.AUTO)

        page.add(main_content)

    async def _handle_instruction(self):
        """Handle instruction execution"""
        instruction = self.current_state["instruction_input"].value.strip()
        if not instruction:
            return

        # Clear input
        self.current_state["instruction_input"].value = ""
        self.current_state["instruction_input"].update()

        # Execute pipeline
        result = await self.execute_instruction(instruction)

    async def _refresh_connection(self):
        """Refresh server connection"""
        if self.current_state:
            y3, error = self.m3.execute(self.current_state)
            if error:
                self.execution_errors.append(error)
            self.current_state.update(y3)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

async def main(page: ft.Page):
    """Main application entry point"""
    orchestrator = APTPipelineOrchestrator()
    result = await orchestrator.execute_full_pipeline(page)

    # Log pipeline initialization
    if result["success"]:
        print("✅ APT Pipeline initialized successfully")
    else:
        print("❌ APT Pipeline initialization with errors:")
        for error in result["errors"]:
            print(f"  • {error['module']}: {error['message']}")

if __name__ == "__main__":
    ft.app(target=main)import flet as ft
import requests
import os
import platform
from apt_pipeline_pkg.apt_modules import m1_load_state, m2_extract_eq, m3_llm_rewrite, m5_persist
from apt_pipeline_pkg.apt_modules import m4_sim_trace
import datetime
import threading
import time
import logging

# --- m1: System/context scan ---
def m1_scan_context(context_folder: str | None = None):
    """Scan for context files.

    Looks in both 'context_files' and 'context' directories (relative to cwd).
    Returns a dict with discovered files keyed by folder so the UI can show where they came from.
    """
    search_dirs = []
    if context_folder:
        search_dirs.append(context_folder)
    # prefer explicit 'context_files' then 'context'
    search_dirs.extend(["context_files", "context"])
    found = {}
    for d in search_dirs:
        p = os.path.join(os.getcwd(), d)
        if os.path.isdir(p):
            matches = [f for f in os.listdir(p) if f.endswith((".txt", ".md"))]
            if matches:
                # store relative paths for UI
                found[d] = [os.path.join(d, f) for f in matches]
    sysinfo = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "cwd": os.getcwd(),
        "context_files": found
    }
    return sysinfo

# --- m2: Render algebraic pipeline equation as clickable UI ---
def m2_render_pipeline(equation, on_module_click, on_var_click):
    import re
    # Color code modules (m1, m2, ...) and variables (x1, x2, y1, y2, Y)
    tokens = re.split(r'(m\d+|x\d+|y\d+|Y)', equation)
    controls = []
    for t in tokens:
        if t.startswith('m') and t[1:].isdigit():
            controls.append(ft.TextButton(t, style=ft.ButtonStyle(color="#2196F3"), on_click=lambda e, t=t: on_module_click(t)))
        elif t.startswith('x') or t.startswith('y') or t == 'Y':
            controls.append(ft.TextButton(t, style=ft.ButtonStyle(color="#4CAF50"), on_click=lambda e, t=t: on_var_click(t)))
        else:
            controls.append(ft.Text(t))
    return ft.Row(controls, wrap=True)

# --- m3: Workspace tab simulation ---
class WorkspaceTabs(ft.Tabs):
    def __init__(self):
        super().__init__(tabs=[], selected_index=0, expand=1)
    def open_tab(self, label, content):
        # content may be a string or a Control
        for i, tab in enumerate(self.tabs):
            if tab.text == label:
                # replace content if new content is provided
                tab.content = content if not isinstance(content, str) else ft.Text(content)
                self.selected_index = i
                self.update()
                return
        ctrl = content if not isinstance(content, str) else ft.Text(content)
        self.tabs.append(ft.Tab(text=label, content=ctrl))
        self.selected_index = len(self.tabs) - 1
        self.update()



class ChatThreads(ft.Tabs):
    def __init__(self):
        super().__init__(tabs=[], selected_index=0, expand=1)

    def open_thread(self, label: str):
        for i, tab in enumerate(self.tabs):
            if tab.text == label:
                self.selected_index = i
                self.update()
                return
        col = ft.Column()
        self.tabs.append(ft.Tab(text=label, content=col))
        self.selected_index = len(self.tabs) - 1
        self.update()

    def append_message(self, label: str, message: str, author: str = "assistant"):
        # ensure thread exists
        self.open_thread(label)
        # format message with timestamp and author
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{ts}] {author}: {message}"
        for tab in self.tabs:
            if tab.text == label:
                try:
                    # tab.content is expected to be a Column
                    tab.content.controls.append(ft.Text(formatted))
                    tab.content.update()
                except Exception:
                    tab.content = ft.Column([ft.Text(formatted)])
                    self.update()
                return

class StatusBar(ft.Container):
    """
    m6_status_bar
    Contract:
      Inputs: status: str, notification: str|None
      Outputs: persistent status bar, transient toast if notification
      Errors: None
      Success: Status bar always visible, never overlaps UI, toast for events
      Algebraic: y6 = m6(y5, x3, x4)
    """
    def __init__(self, status="Idle"):
        super().__init__(
            content=ft.Text(status, color="#F8F8F2", size=14, weight=ft.FontWeight.BOLD),
            bgcolor="#232936",
            padding=10,
            alignment=ft.alignment.center,
            border_radius=0,
            height=40,
            expand=False
        )
        self.status = status
        self.toast = None
    def set_status(self, status):
        self.status = status
        try:
            self.content.value = status
            try:
                self.content.update()
            except AssertionError:
                # control not yet added to page; ignore update for now
                pass
        except Exception:
            # best-effort: if content isn't set, store status for later
            self.status = status
    def show_toast(self, page, message, duration=2):
        try:
            # Instead of using overlay/snack_bar which can interfere with scrolling
            # we'll set the status text briefly and log the message. This avoids
            # creating an overlay that may cause the UI to go black on scroll.
            self.set_status(message)
            # Keep a log entry; page may not be available in some contexts.
            try:
                logging.getLogger(__name__).info(f"toast: {message}")
            except Exception:
                pass
        except Exception:
            # best-effort no-op
            pass

    def append_message(self, label: str, message: str, author: str = "assistant"):
        # ensure thread exists
        self.open_thread(label)
        # format message with timestamp and author
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{ts}] {author}: {message}"
        for tab in self.tabs:
            if tab.text == label:
                # tab.content is a Column
                try:
                    tab.content.controls.append(ft.Text(formatted))
                    tab.content.update()
                except Exception:
                    tab.content = ft.Column([ft.Text(formatted)])
                    self.update()
                return

# --- m4: Main Flet UI ---
def main(page: ft.Page):
    # configure logger for this module
    logging.basicConfig(filename=os.path.join(os.getcwd(), "apt_flet_dashboard.log"), level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
    logger = logging.getLogger(__name__)
    # --- m6: Status Bar and Notification ---
    status_bar = StatusBar()
    def set_status(status):
        logger.debug(f"set_status called: {status}")
        status_bar.set_status(status)
    def notify(message):
        logger.debug(f"notify called: {message}")
        status_bar.show_toast(page, message)
    # --- Llama Example Outputs for User Learning ---
    llama_examples = [
        {"prompt": "Summarize a text file in context_files.", "output": "y1 = m1_load_file(x1 = 'context_files/file.txt')\ny2 = m2_summarize(y1)\ny_final = m2(y1)  # Loads and summarizes file"},
        {"prompt": "Take a screenshot and analyze it.", "output": "y1 = m1_screenshot()\ny2 = m2_analyze_image(y1)\ny_final = m2(y1)  # Screenshot then analyze"},
        {"prompt": "Research the latest discoveries in the context folder.", "output": "y1 = m1_scan_context(x1 = 'context')\ny2 = m2_extract_discoveries(y1)\ny_final = m2(y1)  # Research context for discoveries"},
        {"prompt": "Generate a report from all markdown files.", "output": "y1 = m1_list_files(x1 = '*.md')\ny2 = m2_aggregate(y1)\ny3 = m3_generate_report(y2)\ny_final = m3(y2)  # Aggregate and report"},
        {"prompt": "Visualize the pipeline as a diagram.", "output": "y1 = m1_parse_equation(x1 = pipeline_equation)\ny2 = m2_render_diagram(y1)\ny_final = m2(y1)  # Render pipeline diagram"},
        {"prompt": "Start a multi-chat session for brainstorming.", "output": "y1 = m1_enable_multichat()\ny2 = m2_new_thread(y1)\ny_final = m2(y1)  # Enable multi-chat and new thread"},
        {"prompt": "Export the current pipeline and chat history.", "output": "y1 = m1_export_pipeline()\ny2 = m2_export_chat()\ny3 = m3_bundle_outputs(y1, y2)\ny_final = m3(y1, y2)  # Export pipeline and chat"},
        {"prompt": "Simulate the pipeline execution.", "output": "y1 = m1_parse_equation(x1 = pipeline_equation)\ny2 = m2_simulate(y1)\ny_final = m2(y1)  # Simulate pipeline"},
    ]

    def show_llama_examples(e=None):
        rows = []
        for ex in llama_examples:
            rows.append(ft.Text(f"Prompt: {ex['prompt']}", color="#8BE9FD", weight=ft.FontWeight.BOLD))
            rows.append(ft.Text(f"APT Output:\n{ex['output']}", color="#F8F8F2"))
            rows.append(ft.Divider())
        content = ft.Column(rows, width=700)
        workspace_tabs.open_tab("Llama Examples", content)
        # APT GUI Pipeline:
        #   GUI_State = m5(m4(m3(m2(m1(x1)), x2)))
    page.title = "APT MCP Dashboard"
    # Avoid page-level scrolling; use the main_content Column's scroll to manage viewport.
    page.scroll = "none"
    page.bgcolor = "#181C24"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    set_status("Booting...")
    sysinfo = m1_scan_context()
    greeting = f"Hey user, you've started APT MCP Server.\nThis is what I see:\n{sysinfo}"
    # Context file management and multi-chat state
    context_files = sysinfo.get("context_files", {}) if isinstance(sysinfo, dict) else {}
    selected_context = {"path": None}
    chat_counter = {"n": 0}
    result_box = ft.TextField(label="Result", multiline=True, min_lines=8, max_lines=20, read_only=True, bgcolor="#232936", color="#F8F8F2", border_color="#444857")
    pipeline_equation = "y_final = m6(m5(m4(m3(m2(m1(x1,...))))))"
    pipeline_box = ft.TextField(label="Pipeline Equation", value=pipeline_equation, read_only=True, bgcolor="#232936", color="#8BE9FD", border_color="#444857")
    discoveries_box = ft.TextField(label="Discoveries", multiline=True, min_lines=2, max_lines=6, read_only=True, bgcolor="#232936", color="#50FA7B", border_color="#444857")
    instruction_box = ft.TextField(label="Instruction", autofocus=True, bgcolor="#232936", color="#F8F8F2", border_color="#444857", hint_text="Type an instruction or question and press Enter to send", on_submit=lambda e: send_instruction(e), multiline=False)
    screenshot_img = ft.Image(width=400, visible=False)
    workspace_tabs = WorkspaceTabs()
    # Chat threads layer (separate conversational layer)
    # state persistence
    state_file = os.path.join(os.getcwd(), ".apt_dashboard_state.json")
    chat_history: dict = {}

    def load_state():
        nonlocal chat_history
        try:
            if os.path.isfile(state_file):
                with open(state_file, "r", encoding="utf-8") as sf:
                    st = __import__("json").load(sf)
                    chat_history = st.get("chat_history", {}) or {}
                    sel = st.get("selected_context")
                    if sel:
                        selected_context["path"] = sel
                        status_text.value = f"Selected: {sel}"
                    multi = st.get("multi_chat", False)
                    multi_chat_switch.value = multi
        except Exception:
            chat_history = {}

    def save_state():
        try:
            st = {"chat_history": chat_history, "selected_context": selected_context.get("path"), "multi_chat": bool(multi_chat_switch.value)}
            with open(state_file, "w", encoding="utf-8") as sf:
                __import__("json").dump(st, sf, indent=2)
        except Exception as ex:
            append_to_result("system", f"Failed to save state: {ex}")

    chat_threads = ChatThreads()
    load_state()
    # populate from chat_history
    for tlabel, msgs in chat_history.items():
        for m in msgs:
            ts = m.get("ts")
            author = m.get("author", "assistant")
            text = m.get("text", "")
            chat_threads.append_message(tlabel, text, author=author)
    # UI container for context files and status
    context_container = ft.Column()
    status_text = ft.Text("Selected: none", color="#8BE9FD")
    multi_chat_switch = ft.Switch(label="Multi-chat", value=False)

    def render_context_files():
        context_container.controls.clear()
        if not context_files:
            context_container.controls.append(ft.Text("No context files found.", color="#AAAAAA"))
        else:
            for folder, files in context_files.items():
                context_container.controls.append(ft.Text(f"{folder}:", color="#8BE9FD"))
                for f in files:
                    fname = os.path.basename(f)
                    def _on_click(e, path=f, name=fname):
                        p = os.path.join(os.getcwd(), path)
                        try:
                            with open(p, "r", encoding="utf-8") as fh:
                                content = fh.read()
                        except Exception as ex:
                            content = f"Failed to load {path}: {ex}"
                        workspace_tabs.open_tab(name, content)
                        selected_context["path"] = path
                        status_text.value = f"Selected: {path}"
                        status_text.update()
                    context_container.controls.append(ft.TextButton(fname, on_click=_on_click, style=ft.ButtonStyle(color="#8BE9FD")))
        context_container.update()

    # defer rendering until the container is added to the page

    def refresh_contexts(e=None):
        nonlocal context_files
        sys = m1_scan_context()
        context_files = sys.get("context_files", {}) if isinstance(sys, dict) else {}
        render_context_files()
        status_text.value = f"Selected: {selected_context.get('path') or 'none'} (refreshed)"
        status_text.update()

    def update_discoveries():
        try:
            resp = requests.get("http://localhost:8000/v1/research/memory")
            data = resp.json()
            discoveries_box.value = "\n".join(data.get("discoveries", []))
            discoveries_box.update()
        except Exception:
            discoveries_box.value = "(No discoveries yet)"
            discoveries_box.update()

    def append_to_result(sender: str, text: str):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{ts}] {sender}: {text}\n\n"
        result_box.value = (result_box.value or "") + entry
        result_box.update()

    def update_pipeline_box(equation):
        pipeline_box.value = equation
        pipeline_box.update()
        # Also update the interactive pipeline row
        pipeline_row.controls.clear()
        pipeline_row.controls.extend(m2_render_pipeline(equation, on_module_click, on_var_click).controls)
        pipeline_row.update()

    def on_module_click(module):
        workspace_tabs.open_tab(module, f"Workspace for {module}")

    def on_var_click(var):
        workspace_tabs.open_tab(var, f"Context for {var}")

    def send_instruction(e):
        instr = (instruction_box.value or "").strip()
        if not instr:
            return
        set_status("Processing instruction...")
        # record user message first
        if multi_chat_switch.value:
            chat_counter["n"] += 1
            current_thread = f"Chat {chat_counter['n']}"
        else:
            current_thread = "General"
        chat_history.setdefault(current_thread, []).append({"ts": datetime.datetime.now().isoformat(), "author": "user", "text": instr})
        chat_threads.append_message(current_thread, instr, author="user")
        save_state()
        # Try to get APT pipeline equation for the instruction
        try:
            set_status("Parsing instruction (Llama)...")
            resp = requests.post("http://localhost:8000/v1/parse_instruction", json={"prompt": instr})
            eqn = resp.json().get("apt_equation", "")
            if eqn:
                update_pipeline_box(eqn)
        except Exception:
            notify("Failed to parse instruction.")
        if "screenshot" in instr:
            set_status("Taking screenshot...")
            resp = requests.post("http://localhost:8000/v1/chat/completions", json={"prompt": "Take a screenshot", "screenshot": True})
            data = resp.json()
            append_to_result("system", data.get("result", ""))
            if data.get("screenshot"):
                screenshot_img.src = data["screenshot"]
                screenshot_img.visible = True
            else:
                screenshot_img.visible = False
            screenshot_img.update()
            set_status("Screenshot complete.")
        elif "research" in instr:
            set_status("Starting research mode...")
            requests.post("http://localhost:8000/v1/research/start")
            append_to_result("system", "Research mode started.")
            set_status("Research mode active.")
        elif "llama" in instr or "generate" in instr:
            set_status("Calling Llama...")
            resp = requests.post("http://localhost:8000/v1/chat/completions", json={"prompt": instr})
            data = resp.json()
            message = data.get("result", "")
            # assistant reply to current thread
            chat_history.setdefault(current_thread, []).append({"ts": datetime.datetime.now().isoformat(), "author": "assistant", "text": message})
            chat_threads.append_message(current_thread, message, author="assistant")
            save_state()
            screenshot_img.visible = False
            screenshot_img.update()
            set_status("Llama response complete.")
        else:
            set_status("Calling Llama (default)...")
            resp = requests.post("http://localhost:8000/v1/chat/completions", json={"prompt": instr})
            data = resp.json()
            message = data.get("result", f"Instruction received: {instr} (no matching module)")
            chat_history.setdefault(current_thread, []).append({"ts": datetime.datetime.now().isoformat(), "author": "assistant", "text": message})
            chat_threads.append_message(current_thread, message, author="assistant")
            save_state()
            screenshot_img.visible = False
            screenshot_img.update()
            set_status("Llama response complete.")
        instruction_box.value = ""
        instruction_box.update()
        update_discoveries()
        update_discoveries()
        set_status("Idle")

    def nlp_chat(e):
        instr = (instruction_box.value or "").strip()
        if not instr:
            return
        # record user message in thread
        if multi_chat_switch.value:
            chat_counter["n"] += 1
            tlabel = f"Chat {chat_counter['n']}"
        else:
            tlabel = "General"
        chat_history.setdefault(tlabel, []).append({"ts": datetime.datetime.now().isoformat(), "author": "user", "text": instr})
        chat_threads.append_message(tlabel, instr, author="user")
        resp = requests.post("http://localhost:8000/v1/nlp_chat", json={"prompt": instr})
        data = resp.json()
        message = data.get("nlp_response", "[No response]")
        chat_history.setdefault(tlabel, []).append({"ts": datetime.datetime.now().isoformat(), "author": "assistant", "text": message})
        chat_threads.append_message(tlabel, message, author="assistant")
        save_state()
        screenshot_img.visible = False
        screenshot_img.update()
        update_discoveries()

    def evaluate_workflow(e):
        instr = (instruction_box.value or "").strip()
        if not instr:
            return
        try:
            resp = requests.post("http://localhost:8000/v1/parse_instruction", json={"prompt": instr})
            eqn = resp.json().get("apt_equation", "")
            if eqn:
                update_pipeline_box(eqn)
                result_box.value = f"Evaluated workflow:\n{eqn}"
                result_box.update()
        except Exception as ex:
            result_box.value = f"Failed to evaluate workflow: {ex}"
            result_box.update()

    # --- Export snapshot (pipeline + chat + context) ---
    def export_snapshot(e=None):
        try:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            base_dir = os.path.join(os.getcwd(), "archive", "experiments", ts)
            os.makedirs(base_dir, exist_ok=True)
            # Save pipeline equation
            with open(os.path.join(base_dir, "pipeline_equation.txt"), "w", encoding="utf-8") as fpeq:
                fpeq.write(pipeline_box.value or "")
            # Save chat history
            with open(os.path.join(base_dir, "chat_history.json"), "w", encoding="utf-8") as fch:
                __import__("json").dump(chat_history, fch, indent=2)
            # Save selected context file content if any
            if selected_context.get("path"):
                src_path = os.path.join(os.getcwd(), selected_context["path"])
                if os.path.isfile(src_path):
                    with open(src_path, "r", encoding="utf-8") as sc:
                        ctx_content = sc.read()
                    with open(os.path.join(base_dir, "selected_context.txt"), "w", encoding="utf-8") as scw:
                        scw.write(ctx_content)
            # Derive module list from equation
            eq_text = pipeline_box.value or ""
            modules = m_extract_modules(eq_text)
            trace = m_simulate_trace(modules)
            with open(os.path.join(base_dir, "trace.json"), "w", encoding="utf-8") as ftr:
                __import__("json").dump(trace, ftr, indent=2)
            manifest_core = m_build_snapshot(eq_text, modules, selected_context.get("path"), bool(multi_chat_switch.value), chat_history, trace)
            manifest_core["files"] = os.listdir(base_dir)
            manifest = manifest_core
            with open(os.path.join(base_dir, "manifest.json"), "w", encoding="utf-8") as fm:
                __import__("json").dump(manifest, fm, indent=2)
            append_to_result("system", f"Exported snapshot to {base_dir}")
        except Exception as ex:
            append_to_result("system", f"Snapshot export failed: {ex}")

    # --- Execute APT pipeline with MCP server endpoints ---
    def execute_pipeline(e=None):
        eq_text = pipeline_box.value or ""
        if not eq_text.strip():
            append_to_result("system", "No pipeline equation to execute.")
            return

        set_status("Executing APT pipeline...")
        append_to_result("pipeline", f"🚀 Starting execution of: {eq_text}")

        try:
            # Step 1: Parse the instruction to get APT equation
            append_to_result("pipeline", "📡 Calling parse_instruction endpoint...")
            resp = requests.post("http://localhost:8000/v1/parse_instruction",
                               json={"prompt": eq_text}, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                apt_eq = data.get("apt_equation", eq_text)
                append_to_result("pipeline", f"✅ Parsed equation: {apt_eq}")
            else:
                append_to_result("pipeline", f"⚠️ Parse failed (status {resp.status_code}), using original")
                apt_eq = eq_text

            # Step 2: Execute via chat completions
            append_to_result("pipeline", "🤖 Calling chat/completions endpoint...")
            resp = requests.post("http://localhost:8000/v1/chat/completions",
                               json={"prompt": f"Execute this APT pipeline: {apt_eq}"}, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                result = data.get("result", "No result returned")
                append_to_result("pipeline", f"� LLM Response: {result}")
            else:
                append_to_result("pipeline", f"❌ Chat completion failed (status {resp.status_code})")

            # Step 3: Check research memory for discoveries
            append_to_result("pipeline", "🔍 Checking research/memory endpoint...")
            resp = requests.get("http://localhost:8000/v1/research/memory", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                memory = data.get("memory", [])
                discoveries = data.get("discoveries", [])
                append_to_result("pipeline", f"� Memory entries: {len(memory)}")
                append_to_result("pipeline", f"🔬 Discoveries: {len(discoveries)}")

                # Update discoveries box
                if discoveries:
                    discoveries_box.value = "\n".join(discoveries[-5:])  # Show last 5
                    discoveries_box.update()
            else:
                append_to_result("pipeline", f"⚠️ Memory check failed (status {resp.status_code})")

            # Step 4: Try NLP chat for additional processing
            append_to_result("pipeline", "🧠 Calling nlp_chat endpoint...")
            resp = requests.post("http://localhost:8000/v1/nlp_chat",
                               json={"prompt": f"Analyze this APT pipeline result: {apt_eq}"}, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                nlp_result = data.get("nlp_response", "No NLP response")
                append_to_result("pipeline", f"🧠 NLP Analysis: {nlp_result}")
            else:
                append_to_result("pipeline", f"⚠️ NLP chat failed (status {resp.status_code})")

            append_to_result("pipeline", "✅ Pipeline execution completed successfully!")
            append_to_result("pipeline", f"🔗 Total MCP endpoint calls: 4 (parse, chat, memory, nlp)")
            set_status("Pipeline execution complete")

        except requests.exceptions.Timeout:
            append_to_result("pipeline", "⏰ Pipeline execution timed out")
            set_status("Pipeline execution timed out")
        except requests.exceptions.ConnectionError:
            append_to_result("pipeline", "🚫 Cannot connect to MCP server on localhost:8000")
            set_status("MCP server connection failed")
        except Exception as ex:
            append_to_result("pipeline", f"❌ Pipeline execution failed: {str(ex)}")
            set_status("Pipeline execution failed")


    pipeline_row = ft.Row([], wrap=True)
    # Initial rendering of pipeline equation
    pipeline_row.controls.extend(m2_render_pipeline(pipeline_equation, on_module_click, on_var_click).controls)

    # --- Main Layout: Modular, Non-overlapping Containers ---
    # Grid-based dashboard layout
    main_grid = ft.GridView(
        runs_count=2,
        max_extent=700,
        child_aspect_ratio=1.7,
        spacing=16,
        run_spacing=16,
        expand=True,
        controls=[
            ft.Container(
                ft.Column([
                    ft.Text(greeting, color="#F1FA8C", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([status_text, multi_chat_switch], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(context_container, bgcolor="#181C24", padding=8, border_radius=6, margin=4, expand=True),
                    ft.ElevatedButton("Refresh Context", on_click=refresh_contexts, bgcolor="#6272A4", color="#F8F8F2"),
                ], spacing=8),
                bgcolor="#232936", padding=16, border_radius=10, expand=True
            ),
            ft.Container(
                ft.Column([
                    ft.Text("Pipeline Equation", color="#8BE9FD", size=16, weight=ft.FontWeight.BOLD),
                    pipeline_box,
                    pipeline_row,
                    ft.Row([
                        ft.ElevatedButton("Execute Pipeline", on_click=execute_pipeline, bgcolor="#444857", color="#F8F8F2"),
                        ft.ElevatedButton("Send", on_click=send_instruction, bgcolor="#444857", color="#F8F8F2"),
                        ft.ElevatedButton("Chat (NLP)", on_click=nlp_chat, bgcolor="#6272A4", color="#F8F8F2")
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    instruction_box
                ], spacing=8),
                bgcolor="#232936", padding=16, border_radius=10, expand=True
            ),
            ft.Container(
                ft.Column([
                    ft.Text("Results", color="#50FA7B", size=16, weight=ft.FontWeight.BOLD),
                    result_box
                ], spacing=8),
                bgcolor="#232936", padding=16, border_radius=10, expand=True
            ),
            ft.Container(
                ft.Column([
                    ft.Text("Discoveries", color="#F1FA8C", size=16, weight=ft.FontWeight.BOLD),
                    discoveries_box
                ], spacing=8),
                bgcolor="#232936", padding=16, border_radius=10, expand=True
            ),
            ft.Container(
                ft.Column([
                    ft.Text("Context Screenshot", color="#8BE9FD", size=16, weight=ft.FontWeight.BOLD),
                    screenshot_img
                ], spacing=8),
                bgcolor="#232936", padding=16, border_radius=10, expand=True
            ),
            ft.Container(
                ft.Column([
                    ft.Text("Chat Threads", color="#F1FA8C", size=16, weight=ft.FontWeight.BOLD),
                    chat_threads
                ], spacing=8),
                bgcolor="#232936", padding=16, border_radius=10, expand=True
            ),
            ft.Container(
                ft.Column([
                    ft.Text("Workspace Tabs", color="#8BE9FD", size=16, weight=ft.FontWeight.BOLD),
                    workspace_tabs
                ], spacing=8),
                bgcolor="#232936", padding=16, border_radius=10, expand=True
            )
        ]
    )
    # Clear page and add a wrapper Column with the grid and a fixed status bar
    page.controls.clear()
    wrapper = ft.Column([main_grid, status_bar], expand=True)
    page.add(wrapper)
    # now that context_container is on the page, render its contents
    chat_threads.open_thread("General")
    render_context_files()
    update_discoveries()

    # --- Startup validation / bootcheck ---
    def boot_check():
        append_to_result("boot", "Starting boot validation...")
        # Check directories
        missing = []
        for d in ("context_files", "context"):
            p = os.path.join(os.getcwd(), d)
            if not os.path.isdir(p):
                missing.append(d)
                try:
                    os.makedirs(p, exist_ok=True)
                    append_to_result("boot", f"Created missing directory: {d}")
                except Exception as ex:
                    append_to_result("boot", f"Failed to create directory {d}: {ex}")
        if not missing:
            append_to_result("boot", "All context directories present.")

        # Check MCP endpoints (GET for memory, POST for parse_instruction)
        try:
            ep_mem = "http://localhost:8000/v1/research/memory"
            r = requests.get(ep_mem, timeout=3)
            append_to_result("boot", f"Endpoint {ep_mem} reachable (status {r.status_code}).")
        except Exception as ex:
            append_to_result("boot", f"Endpoint {ep_mem} not reachable: {ex}")
        try:
            ep_parse = "http://localhost:8000/v1/parse_instruction"
            r = requests.post(ep_parse, json={"prompt": "boot check"}, timeout=3)
            append_to_result("boot", f"Endpoint {ep_parse} reachable (status {r.status_code}).")
        except Exception as ex:
            append_to_result("boot", f"Endpoint {ep_parse} not reachable: {ex}")

        status_text.value = "Boot: validation complete"
        status_text.update()

    # start boot check in background
    t_boot = threading.Thread(target=boot_check, daemon=True)
    t_boot.start()

ft.app(target=main)
