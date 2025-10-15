"""
APT Flet Dashboard - TRUE APT METHODOLOGY
========================================

🚀 PURE APT ALGEBRAIC PIPELINE IMPLEMENTATION:
- Single unified pipeline equation: Y = m6(m5(m4(m3(m2(m1(X)))))
- Explicit variable definitions (x1, x2, y1, y2, etc.)
- Algebraic error handling (no scattered try-catch)
- Deterministic module contracts
- Unified state management

Pipeline Equation: Y_dashboard = m6_status(m5_persist(m4_execute(m3_connect(m2_ui(m1_init(X_startup)))))

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
import flet as ft
import requests
import os
import json
import datetime
import asyncio
import time

# ============================================================================
# APT MODULE DEFINITIONS - PURE ALGEBRAIC IMPLEMENTATION
# ============================================================================

class APTModule:
    """Base class for all APT modules with algebraic contracts"""

    def __init__(self, module_name: str):
        self.module_name = module_name
        self.execution_log = []

    def log_execution(self, inputs: dict, outputs: dict, success: bool):
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

    def to_dict(self) -> dict:
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

    def execute(self, x_startup: dict) -> tuple[dict, APTError | None]:
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
                try:
                    files = [f for f in os.listdir(dirname) if f.endswith(('.txt', '.md'))]
                    if files:
                        context_files[dirname] = files
                except Exception:
                    pass  # Skip inaccessible directories

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

    def execute(self, y1_system_state: dict, page: ft.Page) -> tuple[dict, APTError | None]:
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

    def execute(self, y2_ui_components: dict) -> tuple[dict, APTError | None]:
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
                "ui_components": y2_ui_components,
                "server_url": server_url,
                "server_status": server_status,
                "connection_time": connection_time,
                "connection_success": True
            }
            self.log_execution(inputs, {"y3_connected_system": "connected"}, True)
            return y3_connected_system, None
        else:
            error = APTError(
                "m3_server_connection",
                "connection_failure",
                f"Failed to connect to server: {server_status.get('error', 'Unknown error')}",
                "Check if MCP server is running on localhost:8000"
            )
            y3_connected_system = {
                "ui_components": y2_ui_components,
                "server_url": server_url,
                "server_status": server_status,
                "connection_time": connection_time,
                "connection_success": False
            }
            self.log_execution(inputs, {"y3_connected_system": "connection_failed"}, False)
            return y3_connected_system, error

    def _attempt_connection(self, server_url: str) -> dict:
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

    def execute(self, y3_connected_system: dict, x_instruction: str) -> tuple[dict, APTError | None]:
        """Execute m4 with full pipeline execution"""
        inputs = {"y3_connected_system": "system_ready", "x_instruction": x_instruction}

        if not y3_connected_system["connection_success"]:
            error = APTError(
                "m4_pipeline_execution",
                "no_connection",
                "Cannot execute pipeline: server not connected",
                "Ensure MCP server is running and accessible"
            )
            y4_results = {
                "instruction": x_instruction,
                "execution_trace": [{"error": "No server connection"}],
                "server_response": None,
                "success": False
            }
            self.log_execution(inputs, {"y4_results": "no_connection"}, False)
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
                        "parse_result": parse_data,
                        "chat_result": chat_data
                    },
                    "success": True
                }
                self.log_execution(inputs, {"y4_results": "success"}, True)
                return y4_results, None
            else:
                y4_results = {
                    "instruction": x_instruction,
                    "execution_trace": execution_trace,
                    "server_response": None,
                    "success": False
                }
                error = APTError(
                    "m4_pipeline_execution",
                    "server_error",
                    f"Server returned errors: parse={parse_response.status_code}, chat={chat_response.status_code}",
                    "Check server logs and ensure all endpoints are functional"
                )
                self.log_execution(inputs, {"y4_results": "server_error"}, False)
                return y4_results, error

        except Exception as e:
            y4_results = {
                "instruction": x_instruction,
                "execution_trace": execution_trace + [{"error": str(e)}],
                "server_response": None,
                "success": False
            }
            error = APTError(
                "m4_pipeline_execution",
                "execution_error",
                f"Pipeline execution failed: {str(e)}",
                "Check network connectivity and server status"
            )
            self.log_execution(inputs, {"y4_results": "execution_error"}, False)
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

    def execute(self, y4_results: dict) -> tuple[dict, APTError | None]:
        """Execute m5 with state persistence"""
        inputs = {"y4_results": "execution_completed"}

        try:
            # Load existing state
            existing_state = self._load_existing_state()

            # Create new state entry
            new_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "instruction": y4_results["instruction"],
                "success": y4_results["success"],
                "execution_trace": y4_results["execution_trace"]
            }

            # Update state
            existing_state["executions"] = existing_state.get("executions", []) + [new_entry]

            # Save state
            with open(self.state_file, 'w') as f:
                json.dump(existing_state, f, indent=2)

            y5_persisted_state = {
                "results": y4_results,
                "saved_state": existing_state,
                "persistence_success": True
            }

            self.log_execution(inputs, {"y5_persisted_state": "persisted"}, True)
            return y5_persisted_state, None

        except Exception as e:
            y5_persisted_state = {
                "results": y4_results,
                "saved_state": None,
                "persistence_success": False
            }
            error = APTError(
                "m5_state_persistence",
                "persistence_error",
                f"Failed to persist state: {str(e)}",
                "Check file permissions and disk space"
            )
            self.log_execution(inputs, {"y5_persisted_state": "persistence_error"}, False)
            return y5_persisted_state, error

    def _load_existing_state(self) -> dict:
        """Load existing state file"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {"executions": []}

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

    def execute(self, y5_persisted_state: dict, ui_components: dict) -> tuple[dict, APTError | None]:
        """Execute m6 with UI status updates"""
        inputs = {"y5_persisted_state": "state_persisted"}

        try:
            # Update status based on execution results
            if y5_persisted_state["results"]["success"]:
                status_message = "✅ Pipeline execution successful"
                status_color = "#50FA7B"
            else:
                status_message = "❌ Pipeline execution failed"
                status_color = "#FF5555"

            # Update UI components
            ui_components["status_text"].value = status_message
            ui_components["status_text"].color = status_color
            ui_components["status_icon"].color = status_color

            # Update result output
            result_text = f"Instruction: {y5_persisted_state['results']['instruction']}\n"
            result_text += f"Success: {y5_persisted_state['results']['success']}\n"
            result_text += f"Execution time: {len(y5_persisted_state['results']['execution_trace'])} steps\n"

            if y5_persisted_state["results"]["server_response"]:
                result_text += "\nServer Response:\n"
                result_text += json.dumps(y5_persisted_state["results"]["server_response"], indent=2)

            ui_components["result_output"].value = result_text

            # Update execution log
            log_text = ""
            for entry in y5_persisted_state["results"]["execution_trace"]:
                log_text += f"{entry}\n"

            ui_components["execution_log"].value = log_text

            # Force UI updates
            for component in ui_components.values():
                if hasattr(component, 'update'):
                    component.update()

            Y_dashboard = {
                "final_ui_state": ui_components,
                "status_updated": True,
                "dashboard_ready": True
            }

            self.log_execution(inputs, {"Y_dashboard": "updated"}, True)
            return Y_dashboard, None

        except Exception as e:
            Y_dashboard = {
                "final_ui_state": ui_components,
                "status_updated": False,
                "dashboard_ready": False
            }
            error = APTError(
                "m6_status_update",
                "ui_update_error",
                f"Failed to update UI: {str(e)}",
                "Check UI component references and Flet page state"
            )
            self.log_execution(inputs, {"Y_dashboard": "ui_update_error"}, False)
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

    async def execute_full_pipeline(self, page: ft.Page) -> dict:
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

    async def execute_instruction(self, instruction: str) -> dict:
        """Execute an instruction through the pipeline"""
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
        Y, error6 = self.m6.execute(y5, self.current_state["ui_components"])
        if error6:
            self.execution_errors.append(error6)

        return {
            "result": Y,
            "errors": [e.to_dict() for e in self.execution_errors[-3:]],  # Last 3 errors
            "success": not any([error4, error5, error6])
        }

    def _build_ui_layout(self, page: ft.Page, y2_ui_components: dict):
        """Build the UI layout from components"""

        # Create instruction handler
        async def handle_instruction(e):
            instruction = y2_ui_components["instruction_input"].value.strip()
            if instruction:
                y2_ui_components["status_text"].value = "🤖 Executing pipeline..."
                y2_ui_components["status_text"].update()

                result = await self.execute_instruction(instruction)

                if result["success"]:
                    y2_ui_components["status_text"].value = "✅ Pipeline complete"
                    y2_ui_components["status_text"].color = "#50FA7B"
                else:
                    y2_ui_components["status_text"].value = "❌ Pipeline failed"
                    y2_ui_components["status_text"].color = "#FF5555"

                y2_ui_components["status_text"].update()
                y2_ui_components["instruction_input"].value = ""
                y2_ui_components["instruction_input"].update()

        # Bind handler to input
        y2_ui_components["instruction_input"].on_submit = handle_instruction

        # Create main layout
        main_content = ft.Column([
            ft.Text("APT Dashboard - Pure Algebraic Pipeline", size=24, weight=ft.FontWeight.BOLD, color="#8BE9FD"),
            ft.Divider(),

            # Status bar
            ft.Container(
                content=ft.Row([
                    y2_ui_components["status_icon"],
                    y2_ui_components["status_text"]
                ]),
                bgcolor="#232936",
                padding=16,
                border_radius=8
            ),

            # Pipeline section
            ft.Container(
                content=ft.Column([
                    ft.Text("Pipeline Control", size=18, weight=ft.FontWeight.BOLD, color="#50FA7B"),
                    y2_ui_components["pipeline_display"],
                    y2_ui_components["instruction_input"],
                    ft.ElevatedButton("Execute Pipeline", on_click=handle_instruction, bgcolor="#50FA7B")
                ], spacing=12),
                bgcolor="#232936",
                padding=16,
                border_radius=8
            ),

            # Results section
            ft.Container(
                content=ft.Column([
                    ft.Text("Results", size=18, weight=ft.FontWeight.BOLD, color="#F1FA8C"),
                    y2_ui_components["result_output"]
                ], spacing=12),
                bgcolor="#232936",
                padding=16,
                border_radius=8
            ),

            # Execution log
            ft.Container(
                content=ft.Column([
                    ft.Text("Execution Log", size=18, weight=ft.FontWeight.BOLD, color="#BD93F9"),
                    y2_ui_components["execution_log"]
                ], spacing=12),
                bgcolor="#232936",
                padding=16,
                border_radius=8
            )
        ], spacing=16, scroll=ft.ScrollMode.AUTO)

        page.add(main_content)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

async def main(page: ft.Page):
    """Main application entry point"""
    orchestrator = APTPipelineOrchestrator()
    result = await orchestrator.execute_full_pipeline(page)

    # Log pipeline initialization
    if result["success"]:
        print("🚀 APT Dashboard initialized successfully!")
    else:
        print("⚠️ APT Dashboard initialized with errors:")
        for error in result["errors"]:
            print(f"  {error}")

if __name__ == "__main__":
    ft.app(target=main)