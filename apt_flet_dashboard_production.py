"""
APT Flet Dashboard - Production Ready (Algebraic Pipeline Theory + Modern UI)

🚀 BLEEDING-EDGE 2025 FEATURES:
- True APT algebraic pipeline methodology
- Real-time server connectivity monitoring
- Async-first architecture with proper error handling
- Production-ready state management
- Modern UI with clear visual feedback
- Comprehensive logging and tracing

Pipeline Equation:
    Y_dashboard = m6(m5(m4(m3(m2(m1(X_startup))))))

Contract:
  - X_startup: {context_dirs, server_config, ui_config}
  - Y_dashboard: {functional_ui, connected_server, persistent_state}
  - All operations follow strict APT m1→m2→m3 patterns
  - Real-time status updates with algebraic state transitions
  - Graceful error handling with user-friendly feedback

Usage:
    python apt_flet_dashboard_production.py

Requirements:
    pip install flet requests httpx asyncio

Author: APT Framework 2025
License: Production
"""

import asyncio
import json
import logging
import os
import platform
import re
import time
import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

import flet as ft
import requests
import httpx

# ============================================================================
# APT MODULE SYSTEM - PRODUCTION IMPLEMENTATION
# ============================================================================

class APTLogger:
    """Centralized logging for APT operations"""

    def __init__(self, name: str = "apt_dashboard"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Create file handler
        log_file = Path(os.getcwd()) / "apt_dashboard_production.log"
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

        # Add handler to logger
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def info(self, message: str, **kwargs):
        self.logger.info(f"{message} {kwargs if kwargs else ''}")

    def error(self, message: str, **kwargs):
        self.logger.error(f"{message} {kwargs if kwargs else ''}")

    def debug(self, message: str, **kwargs):
        self.logger.debug(f"{message} {kwargs if kwargs else ''}")

# Global logger instance
apt_logger = APTLogger()

# ============================================================================
# APT MODULE m1: SYSTEM SCAN & VALIDATION
# ============================================================================

async def m1_system_scan(x_context_dirs: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    APT Module m1: System scan and validation

    Contract:
      Inputs: x_context_dirs (optional list of directories to scan)
      Outputs: y1_system_state (complete system information)
      Errors: Returns error state with diagnostics
      Success: Full system state with context files and server status

    Algebraic: y1 = m1(x_context_dirs)
    """
    apt_logger.info("m1_system_scan: Starting system validation")

    try:
        # Default context directories
        if x_context_dirs is None:
            x_context_dirs = ["context_files", "context", "docs"]

        # Scan context files
        context_files = {}
        for directory in x_context_dirs:
            dir_path = Path(os.getcwd()) / directory
            if dir_path.exists() and dir_path.is_dir():
                files = [
                    str(f.relative_to(os.getcwd()))
                    for f in dir_path.rglob("*")
                    if f.is_file() and f.suffix in [".txt", ".md", ".json"]
                ]
                if files:
                    context_files[directory] = files

        # System information
        system_info = {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "working_directory": str(Path.cwd()),
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Server connectivity check
        server_status = await m1_check_server_connectivity()

        y1_system_state = {
            "status": "healthy",
            "system_info": system_info,
            "context_files": context_files,
            "server_status": server_status,
            "scan_timestamp": time.time()
        }

        apt_logger.info("m1_system_scan: Complete",
                       context_files=len(context_files),
                       server_status=server_status["status"])

        return y1_system_state

    except Exception as e:
        apt_logger.error("m1_system_scan: Failed", error=str(e))
        return {
            "status": "error",
            "error": str(e),
            "timestamp": time.time()
        }

async def m1_check_server_connectivity() -> Dict[str, Any]:
    """Check MCP server connectivity"""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                return {
                    "status": "connected",
                    "server_url": "http://localhost:8000",
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "status": "error",
                    "server_url": "http://localhost:8000",
                    "status_code": response.status_code
                }
    except Exception as e:
        return {
            "status": "disconnected",
            "server_url": "http://localhost:8000",
            "error": str(e)
        }

# ============================================================================
# APT MODULE m2: UI COMPONENT INITIALIZATION
# ============================================================================

class APTStatusBar(ft.Container):
    """
    APT Module m6: Status Bar with Real-time Updates

    Contract:
      Inputs: status_message (str), notification (optional str)
      Outputs: Updated UI with persistent status display
      Errors: Always displays fallback status
      Success: Status always visible, never overlaps UI

    Algebraic: y6 = m6(y5_ui_state, x_status, x_notification)
    """

    def __init__(self, initial_status: str = "Initializing..."):
        self.current_status = initial_status

        self.status_text = ft.Text(
            initial_status,
            color="#F8F8F2",
            size=14,
            weight=ft.FontWeight.BOLD
        )

        self.progress_bar = ft.ProgressBar(
            width=100,
            height=4,
            color="#50FA7B",
            bgcolor="#44475A"
        )

        # Connection indicator
        self.connection_indicator = ft.Icon(
            ft.Icons.CIRCLE,
            color="#FF5555",  # Red = disconnected
            size=12
        )

        super().__init__(
            content=ft.Row([
                self.connection_indicator,
                self.status_text,
                self.progress_bar
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor="#232936",
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
            border_radius=0,
            height=50
        )

    def update_status(self, status: str, show_progress: bool = False, server_connected: bool = False):
        """Update status with optional progress indicator"""
        self.current_status = status
        self.status_text.value = status
        self.progress_bar.visible = show_progress

        # Update connection indicator
        if server_connected:
            self.connection_indicator.color = "#50FA7B"  # Green = connected
        else:
            self.connection_indicator.color = "#FF5555"  # Red = disconnected

        try:
            self.update()
        except Exception:
            pass  # Handle update errors gracefully

    def show_notification(self, message: str, duration: int = 3):
        """Show temporary notification"""
        original_status = self.current_status
        self.update_status(f"🔔 {message}")

        # Return to original status after duration
        # Note: In production, use proper async timer
        # For now, immediate return to avoid blocking
        # asyncio.create_task(self._restore_status(original_status, duration))

    async def _restore_status(self, original_status: str, delay: int):
        """Restore original status after delay"""
        await asyncio.sleep(delay)
        self.update_status(original_status)

class APTWorkspaceTabs(ft.Tabs):
    """Enhanced workspace tabs with APT module tracking"""

    def __init__(self):
        super().__init__(
            tabs=[],
            selected_index=0,
            expand=True,
            animation_duration=300
        )

    def open_module_workspace(self, module_name: str, content: Any = None):
        """Open workspace for specific APT module"""
        # Check if tab already exists
        for i, tab in enumerate(self.tabs):
            if tab.text == module_name:
                tab.content = self._create_module_content(module_name, content)
                self.selected_index = i
                self.update()
                return

        # Create new tab
        tab_content = self._create_module_content(module_name, content)
        new_tab = ft.Tab(
            text=module_name,
            content=tab_content
        )

        self.tabs.append(new_tab)
        self.selected_index = len(self.tabs) - 1
        self.update()

    def _create_module_content(self, module_name: str, content: Any) -> ft.Control:
        """Create content for module workspace"""
        if isinstance(content, str):
            return ft.Column([
                ft.Text(f"Module: {module_name}", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text(content, selectable=True)
            ])
        elif content is None:
            return ft.Column([
                ft.Text(f"Module: {module_name}", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text(f"Workspace for {module_name}", size=14),
                ft.Text("No content available", color="#6272A4")
            ])
        else:
            return content if isinstance(content, ft.Control) else ft.Text(str(content))

class APTChatThreads(ft.Tabs):
    """Enhanced chat threads with proper message handling"""

    def __init__(self):
        super().__init__(
            tabs=[],
            selected_index=0,
            expand=True,
            scrollable=True
        )
        # Initialize with default thread
        self.create_thread("General")

    def create_thread(self, thread_name: str):
        """Create new chat thread"""
        # Check if thread exists
        for tab in self.tabs:
            if tab.text == thread_name:
                return

        # Create message container with scrolling
        message_container = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            height=300,
            spacing=8
        )

        new_tab = ft.Tab(
            text=thread_name,
            content=ft.Container(
                content=message_container,
                padding=8
            )
        )

        self.tabs.append(new_tab)
        self.selected_index = len(self.tabs) - 1
        self.update()

    def add_message(self, thread_name: str, message: str, author: str = "assistant"):
        """Add message to specific thread"""
        # Ensure thread exists
        self.create_thread(thread_name)

        # Find thread and add message
        for tab in self.tabs:
            if tab.text == thread_name:
                message_container = tab.content.content

                # Create message with timestamp
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")

                message_row = ft.Row([
                    ft.Icon(
                        ft.Icons.PERSON if author == "user" else ft.Icons.SMART_TOY,
                        size=16,
                        color="#8BE9FD" if author == "user" else "#50FA7B"
                    ),
                    ft.Column([
                        ft.Text(f"{author} • {timestamp}", size=10, color="#6272A4"),
                        ft.Text(message, size=12, selectable=True, width=400)
                    ], spacing=2)
                ], spacing=8)

                message_container.controls.append(message_row)
                message_container.update()

                # Scroll to bottom
                try:
                    message_container.scroll_to(offset=-1)
                except:
                    pass

                break

# ============================================================================
# APT MODULE m3: SERVER INTEGRATION
# ============================================================================

class APTServerClient:
    """
    APT Module m3: Server Integration and Communication

    Contract:
      Inputs: server_url, request_data
      Outputs: response_data with error handling
      Errors: Structured error responses with recovery suggestions
      Success: Clean API responses with metadata

    Algebraic: y3 = m3(x_server_url, x_request)
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.is_connected = False
        self.last_check = 0

    async def m3_check_connection(self) -> Dict[str, Any]:
        """Check server connection status"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/health")

                if response.status_code == 200:
                    self.is_connected = True
                    self.last_check = time.time()
                    return {
                        "status": "connected",
                        "response_time": response.elapsed.total_seconds(),
                        "server_info": response.json()
                    }
                else:
                    self.is_connected = False
                    return {
                        "status": "error",
                        "status_code": response.status_code,
                        "message": f"Server returned {response.status_code}"
                    }

        except Exception as e:
            self.is_connected = False
            return {
                "status": "disconnected",
                "error": str(e),
                "suggestion": "Make sure the MCP server is running on localhost:8000"
            }

    async def m3_execute_pipeline(self, instruction: str) -> Dict[str, Any]:
        """Execute APT pipeline on server"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Step 1: Parse instruction
                parse_response = await client.post(
                    f"{self.base_url}/v1/parse_instruction",
                    json={"prompt": instruction}
                )

                if parse_response.status_code != 200:
                    return {
                        "status": "error",
                        "step": "parse",
                        "message": f"Parse failed: {parse_response.status_code}"
                    }

                # Step 2: Execute pipeline
                pipeline_response = await client.post(
                    f"{self.base_url}/v1/pipeline/execute",
                    json={"prompt": instruction}
                )

                if pipeline_response.status_code != 200:
                    return {
                        "status": "error",
                        "step": "execute",
                        "message": f"Execution failed: {pipeline_response.status_code}"
                    }

                # Step 3: Get results
                results = pipeline_response.json()

                return {
                    "status": "success",
                    "instruction": instruction,
                    "equation": parse_response.json().get("apt_equation", ""),
                    "result": results.get("result", ""),
                    "trace": results.get("trace", []),
                    "processing_time": results.get("processing_time", 0)
                }

        except Exception as e:
            return {
                "status": "error",
                "step": "network",
                "error": str(e),
                "suggestion": "Check network connection and server status"
            }

    async def m3_chat_completion(self, prompt: str, system_prompt: str = None) -> Dict[str, Any]:
        """Execute chat completion"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                request_data = {
                    "prompt": prompt,
                    "system_prompt": system_prompt
                }

                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=request_data
                )

                if response.status_code == 200:
                    return {
                        "status": "success",
                        **response.json()
                    }
                else:
                    return {
                        "status": "error",
                        "status_code": response.status_code,
                        "message": f"Chat completion failed: {response.status_code}"
                    }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

# ============================================================================
# APT MODULE m4: PIPELINE EXECUTION ENGINE
# ============================================================================

class APTPipelineEngine:
    """
    APT Module m4: Pipeline Execution with Real-time Feedback

    Contract:
      Inputs: x_instruction, x_server_client, x_ui_callbacks
      Outputs: y4_execution_results with complete trace
      Errors: Detailed error reporting with recovery steps
      Success: Full pipeline execution with real-time updates

    Algebraic: y4 = m4(x_instruction, x_server, x_callbacks)
    """

    def __init__(self, server_client: APTServerClient, status_callback=None):
        self.server_client = server_client
        self.status_callback = status_callback
        self.execution_history = []

    async def m4_execute_instruction(self, instruction: str) -> Dict[str, Any]:
        """Execute instruction with full APT pipeline"""
        execution_id = str(int(time.time()))

        try:
            # Update status
            if self.status_callback:
                self.status_callback("🚀 Starting pipeline execution...", True)

            # Check server connection
            connection_status = await self.server_client.m3_check_connection()
            if connection_status["status"] != "connected":
                return {
                    "status": "error",
                    "error": "Server not connected",
                    "details": connection_status
                }

            # Execute pipeline
            if self.status_callback:
                self.status_callback("🤖 Executing APT pipeline...", True)

            pipeline_result = await self.server_client.m3_execute_pipeline(instruction)

            # Add to history
            execution_record = {
                "id": execution_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "instruction": instruction,
                "result": pipeline_result,
                "success": pipeline_result["status"] == "success"
            }

            self.execution_history.append(execution_record)

            # Update status
            if self.status_callback:
                if pipeline_result["status"] == "success":
                    self.status_callback("✅ Pipeline execution complete", False)
                else:
                    self.status_callback("❌ Pipeline execution failed", False)

            return pipeline_result

        except Exception as e:
            error_result = {
                "status": "error",
                "error": str(e),
                "execution_id": execution_id
            }

            if self.status_callback:
                self.status_callback(f"❌ Error: {str(e)}", False)

            return error_result

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get pipeline execution history"""
        return self.execution_history.copy()

# ============================================================================
# APT MODULE m5: STATE MANAGEMENT
# ============================================================================

class APTStateManager:
    """
    APT Module m5: State Persistence and Management

    Contract:
      Inputs: x_state_data, x_storage_path
      Outputs: y5_persisted_state
      Errors: Fallback to default state with error logging
      Success: Reliable state persistence across sessions

    Algebraic: y5 = m5(x_state, x_storage)
    """

    def __init__(self, storage_path: str = ".apt_dashboard_state.json"):
        self.storage_path = Path(storage_path)
        self.current_state = {}

    async def m5_load_state(self) -> Dict[str, Any]:
        """Load state from persistent storage"""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.current_state = json.load(f)
                apt_logger.info("m5_load_state: State loaded successfully")
                return self.current_state
            else:
                # Return default state
                self.current_state = {
                    "chat_history": {},
                    "selected_context": None,
                    "multi_chat_enabled": False,
                    "pipeline_history": [],
                    "ui_preferences": {}
                }
                apt_logger.info("m5_load_state: Using default state")
                return self.current_state

        except Exception as e:
            apt_logger.error("m5_load_state: Failed to load state", error=str(e))
            self.current_state = {}
            return self.current_state

    async def m5_save_state(self, state_data: Dict[str, Any]) -> bool:
        """Save state to persistent storage"""
        try:
            self.current_state.update(state_data)

            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_state, f, indent=2, ensure_ascii=False)

            apt_logger.info("m5_save_state: State saved successfully")
            return True

        except Exception as e:
            apt_logger.error("m5_save_state: Failed to save state", error=str(e))
            return False

    def get_state(self, key: str, default=None):
        """Get specific state value"""
        return self.current_state.get(key, default)

    def set_state(self, key: str, value: Any):
        """Set specific state value"""
        self.current_state[key] = value

# ============================================================================
# MAIN APT DASHBOARD APPLICATION
# ============================================================================

class APTDashboard:
    """
    Main APT Dashboard Application

    Pipeline Equation:
        Y_dashboard = m6(m5(m4(m3(m2(m1(X_startup))))))

    Where:
        X_startup = {context_dirs, server_config, ui_config}
        Y_dashboard = {functional_ui, connected_server, persistent_state}
    """

    def __init__(self):
        self.state_manager = APTStateManager()
        self.server_client = APTServerClient()
        self.pipeline_engine = None
        self.status_bar = None
        self.workspace_tabs = None
        self.chat_threads = None
        self.page = None

        # UI Components
        self.result_display = None
        self.pipeline_equation = None
        self.instruction_input = None
        self.context_display = None

        # State
        self.system_state = {}
        self.is_initialized = False

    async def main(self, page: ft.Page):
        """Main application entry point"""
        self.page = page

        # Configure page
        page.title = "APT Dashboard - Production Ready"
        page.bgcolor = "#181C24"
        page.scroll = ft.ScrollMode.AUTO
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Initialize status bar first
        self.status_bar = APTStatusBar("🚀 Initializing APT Dashboard...")

        # Set up page layout with status bar
        await self._setup_page_layout()

        # Execute initialization pipeline
        await self._execute_initialization_pipeline()

    async def _setup_page_layout(self):
        """Set up the main page layout"""
        # Create main components
        self.workspace_tabs = APTWorkspaceTabs()
        self.chat_threads = APTChatThreads()

        # Create input components
        self.instruction_input = ft.TextField(
            label="Instruction",
            hint_text="Enter APT instruction or natural language request...",
            multiline=False,
            expand=True,
            on_submit=self._handle_instruction_submit,
            bgcolor="#232936",
            color="#F8F8F2",
            border_color="#444857"
        )

        self.pipeline_equation = ft.TextField(
            label="Pipeline Equation",
            value="Y = m6(m5(m4(m3(m2(m1(X))))))",
            read_only=True,
            bgcolor="#232936",
            color="#8BE9FD",
            border_color="#444857"
        )

        self.result_display = ft.TextField(
            label="Results",
            multiline=True,
            min_lines=10,
            max_lines=15,
            read_only=True,
            bgcolor="#232936",
            color="#F8F8F2",
            border_color="#444857"
        )

        # Create main grid layout
        main_grid = ft.GridView(
            runs_count=2,
            max_extent=600,
            child_aspect_ratio=1.2,
            spacing=16,
            run_spacing=16,
            expand=True,
            controls=[
                # System Status Panel
                ft.Container(
                    content=ft.Column([
                        ft.Text("System Status", size=16, weight=ft.FontWeight.BOLD, color="#8BE9FD"),
                        ft.Divider(),
                        ft.Text("Server: Checking...", color="#F1FA8C"),
                        ft.Text("Context: Scanning...", color="#F1FA8C"),
                        ft.Text("State: Loading...", color="#F1FA8C"),
                        ft.ElevatedButton(
                            "Refresh Status",
                            on_click=self._handle_refresh_status,
                            bgcolor="#6272A4",
                            color="#F8F8F2"
                        )
                    ], spacing=8),
                    bgcolor="#232936",
                    padding=16,
                    border_radius=10
                ),

                # Pipeline Control Panel
                ft.Container(
                    content=ft.Column([
                        ft.Text("Pipeline Control", size=16, weight=ft.FontWeight.BOLD, color="#8BE9FD"),
                        self.pipeline_equation,
                        ft.Row([
                            self.instruction_input,
                            ft.ElevatedButton(
                                "Execute",
                                on_click=self._handle_execute_pipeline,
                                bgcolor="#50FA7B",
                                color="#282A36"
                            )
                        ]),
                        ft.Row([
                            ft.ElevatedButton("Chat", on_click=self._handle_chat, bgcolor="#444857"),
                            ft.ElevatedButton("Export", on_click=self._handle_export, bgcolor="#444857"),
                            ft.ElevatedButton("Clear", on_click=self._handle_clear, bgcolor="#FF5555")
                        ])
                    ], spacing=8),
                    bgcolor="#232936",
                    padding=16,
                    border_radius=10
                ),

                # Results Panel
                ft.Container(
                    content=ft.Column([
                        ft.Text("Results", size=16, weight=ft.FontWeight.BOLD, color="#50FA7B"),
                        self.result_display
                    ], spacing=8),
                    bgcolor="#232936",
                    padding=16,
                    border_radius=10
                ),

                # Chat Threads Panel
                ft.Container(
                    content=ft.Column([
                        ft.Text("Chat Threads", size=16, weight=ft.FontWeight.BOLD, color="#F1FA8C"),
                        self.chat_threads
                    ], spacing=8),
                    bgcolor="#232936",
                    padding=16,
                    border_radius=10
                ),

                # Workspace Panel
                ft.Container(
                    content=ft.Column([
                        ft.Text("Workspace", size=16, weight=ft.FontWeight.BOLD, color="#BD93F9"),
                        self.workspace_tabs
                    ], spacing=8),
                    bgcolor="#232936",
                    padding=16,
                    border_radius=10
                )
            ]
        )

        # Add to page
        self.page.add(
            ft.Column([
                main_grid,
                self.status_bar
            ], expand=True)
        )

    async def _execute_initialization_pipeline(self):
        """Execute the full APT initialization pipeline"""
        try:
            # m1: System scan
            self.status_bar.update_status("📡 m1: Scanning system...", True)
            self.system_state = await m1_system_scan()

            # m2: Load persistent state
            self.status_bar.update_status("💾 m2: Loading state...", True)
            await self.state_manager.m5_load_state()

            # m3: Initialize server connection
            self.status_bar.update_status("🔗 m3: Connecting to server...", True)
            connection_status = await self.server_client.m3_check_connection()

            # m4: Initialize pipeline engine
            self.status_bar.update_status("⚙️ m4: Initializing pipeline engine...", True)
            self.pipeline_engine = APTPipelineEngine(
                self.server_client,
                status_callback=self.status_bar.update_status
            )

            # m5: Update UI with system state
            self.status_bar.update_status("🎨 m5: Updating UI...", True)
            await self._update_ui_with_system_state()

            # m6: Final status update
            server_connected = connection_status["status"] == "connected"
            if server_connected:
                self.status_bar.update_status("✅ APT Dashboard Ready", False, True)
            else:
                self.status_bar.update_status("⚠️ Ready (Server Disconnected)", False, False)

            self.is_initialized = True

            # Add welcome message
            await self._add_result("system", "🚀 APT Dashboard initialized successfully!")
            await self._add_result("system", f"📊 System State: {self.system_state['status']}")
            await self._add_result("system", f"🔗 Server: {connection_status['status']}")

        except Exception as e:
            apt_logger.error("Initialization failed", error=str(e))
            self.status_bar.update_status(f"❌ Initialization failed: {str(e)}", False, False)
            await self._add_result("error", f"Initialization failed: {str(e)}")

    async def _update_ui_with_system_state(self):
        """Update UI components with current system state"""
        if self.system_state.get("status") == "healthy":
            # Update context files in workspace
            context_files = self.system_state.get("context_files", {})
            if context_files:
                context_content = "📁 Context Files Found:\n\n"
                for folder, files in context_files.items():
                    context_content += f"{folder}/\n"
                    for file in files[:5]:  # Show first 5 files
                        context_content += f"  • {file}\n"
                    if len(files) > 5:
                        context_content += f"  ... and {len(files) - 5} more\n"
                    context_content += "\n"

                self.workspace_tabs.open_module_workspace("Context Files", context_content)

    async def _add_result(self, source: str, message: str):
        """Add result message to display"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {source}: {message}\n"

        current_content = self.result_display.value or ""
        self.result_display.value = current_content + formatted_message
        self.result_display.update()

    # Event Handlers
    async def _handle_instruction_submit(self, e):
        """Handle instruction submission"""
        await self._handle_execute_pipeline(e)

    async def _handle_execute_pipeline(self, e):
        """Handle pipeline execution"""
        if not self.is_initialized:
            await self._add_result("error", "Dashboard not initialized")
            return

        instruction = self.instruction_input.value.strip()
        if not instruction:
            await self._add_result("error", "Please enter an instruction")
            return

        # Clear instruction input
        self.instruction_input.value = ""
        self.instruction_input.update()

        # Add user message to chat
        self.chat_threads.add_message("General", instruction, "user")

        # Execute pipeline
        result = await self.pipeline_engine.m4_execute_instruction(instruction)

        if result["status"] == "success":
            await self._add_result("pipeline", f"✅ Success: {result.get('result', 'No result')}")

            # Update pipeline equation if available
            if result.get("equation"):
                self.pipeline_equation.value = result["equation"]
                self.pipeline_equation.update()

            # Add to chat
            self.chat_threads.add_message("General", result.get('result', 'Success'), "assistant")

        else:
            error_msg = result.get("error", result.get("message", "Unknown error"))
            await self._add_result("error", f"❌ Failed: {error_msg}")
            self.chat_threads.add_message("General", f"Error: {error_msg}", "assistant")

    async def _handle_chat(self, e):
        """Handle chat mode"""
        instruction = self.instruction_input.value.strip()
        if not instruction:
            return

        self.instruction_input.value = ""
        self.instruction_input.update()

        # Add to chat
        self.chat_threads.add_message("General", instruction, "user")

        # Execute chat completion
        result = await self.server_client.m3_chat_completion(
            instruction,
            "You are a helpful APT (Algebraic Pipeline Theory) assistant."
        )

        if result["status"] == "success":
            response = result.get("result", "No response")
            self.chat_threads.add_message("General", response, "assistant")
        else:
            error_msg = result.get("error", "Chat failed")
            self.chat_threads.add_message("General", f"Error: {error_msg}", "assistant")

    async def _handle_refresh_status(self, e):
        """Handle status refresh"""
        self.status_bar.update_status("🔄 Refreshing status...", True)

        # Re-run system scan
        self.system_state = await m1_system_scan()
        connection_status = await self.server_client.m3_check_connection()

        # Update UI
        await self._update_ui_with_system_state()

        # Update status
        server_connected = connection_status["status"] == "connected"
        if server_connected:
            self.status_bar.update_status("✅ Status refreshed - Server connected", False, True)
        else:
            self.status_bar.update_status("⚠️ Status refreshed - Server disconnected", False, False)

        await self._add_result("system", "🔄 Status refreshed")

    async def _handle_export(self, e):
        """Handle export functionality"""
        # Create export data
        export_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "system_state": self.system_state,
            "execution_history": self.pipeline_engine.get_execution_history() if self.pipeline_engine else [],
            "current_state": self.state_manager.current_state
        }

        # Save to file
        export_path = f"apt_export_{int(time.time())}.json"
        try:
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)

            await self._add_result("export", f"✅ Exported to {export_path}")
            self.status_bar.show_notification(f"Exported to {export_path}")

        except Exception as e:
            await self._add_result("error", f"❌ Export failed: {str(e)}")

    async def _handle_clear(self, e):
        """Handle clear functionality"""
        self.result_display.value = ""
        self.result_display.update()
        await self._add_result("system", "🗑️ Results cleared")

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

async def main(page: ft.Page):
    """Application entry point"""
    dashboard = APTDashboard()
    await dashboard.main(page)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP, port=8002)