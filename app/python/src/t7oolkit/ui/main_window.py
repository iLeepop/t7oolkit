from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from t7oolkit.config import AppConfig
from t7oolkit.tools.base import Tool
from t7oolkit.ui.components.footer import StatusFooter
from t7oolkit.ui.components.header import HeaderBar
from t7oolkit.ui.components.settings_panel import SettingsPanel
from t7oolkit.ui.components.sidebar import NAV_SETTINGS, NAV_TOOLS, SidebarNav
from t7oolkit.ui.components.tool_workspace import ToolWorkspaceView
from t7oolkit.ui.components.tools_grid import ToolsGridView


class MainWindow:
    def __init__(self, root: tk.Tk, *, config: AppConfig) -> None:
        self.root = root
        self.config = config
        self._in_tool = False
        self._setup_window()
        self._build_ui()

    def _setup_window(self) -> None:
        self.root.title("t7oolkit")
        self.root.geometry("960x640")
        self.root.minsize(760, 520)

    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        shell = ttk.Frame(self.root)
        shell.grid(row=0, column=0, sticky=tk.NSEW)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(1, weight=1)

        self._header = HeaderBar(shell)
        self._header.grid(row=0, column=0, sticky=tk.EW)

        body = ttk.Frame(shell)
        body.grid(row=1, column=0, sticky=tk.NSEW)
        body.columnconfigure(2, weight=1)
        body.rowconfigure(0, weight=1)

        self._sidebar = SidebarNav(body, on_navigate=self._on_navigate)
        self._sidebar.grid(row=0, column=0, sticky=tk.NS)
        self._sidebar.configure(width=220)
        self._sidebar.grid_propagate(False)

        body_separator = ttk.Separator(body, orient=tk.VERTICAL)
        body_separator.grid(row=0, column=1, sticky=tk.NS, padx=(0, 0))

        self._main_host = ttk.Frame(body, padding=0)
        self._main_host.grid(row=0, column=2, sticky=tk.NSEW)
        self._main_host.columnconfigure(0, weight=1)
        self._main_host.rowconfigure(0, weight=1)

        self._tools_grid = ToolsGridView(self._main_host, on_tool_select=self._open_tool)
        self._tool_workspace = ToolWorkspaceView(
            self._main_host,
            on_back=self._back_to_tools,
            on_status=self._set_tool_status,
        )
        self._settings_panel = SettingsPanel(self._main_host, self.config)

        self._footer = StatusFooter(shell)
        self._footer.grid(row=2, column=0, sticky=tk.EW)

        self._show_tools_grid()

    def _set_tool_status(self, message: str) -> None:
        if self._tool_workspace.current_tool:
            self._footer.set_status(f"「{self._tool_workspace.current_tool.name}」· {message}")
        else:
            self._footer.set_status(message)

    def _on_navigate(self, nav_id: str) -> None:
        if nav_id == NAV_TOOLS:
            self._show_tools_grid()
            return

        if nav_id == NAV_SETTINGS:
            self._show_settings()

    def _show_view(self, view: ttk.Frame) -> None:
        for child in (self._tools_grid, self._tool_workspace, self._settings_panel):
            child.grid_remove()
        view.grid(row=0, column=0, sticky=tk.NSEW)

    def _show_tools_grid(self) -> None:
        self._in_tool = False
        self._tool_workspace.clear()
        self._tools_grid.refresh()
        self._show_view(self._tools_grid)
        self._footer.reset()

    def _show_settings(self) -> None:
        self._in_tool = False
        self._tool_workspace.clear()
        self._settings_panel.refresh()
        self._show_view(self._settings_panel)
        self._footer.set_status("基础配置")

    def _open_tool(self, tool: Tool) -> None:
        self._in_tool = True
        self._tool_workspace.open_tool(tool)
        self._show_view(self._tool_workspace)
        self._footer.set_tool_active(tool.name)

    def _back_to_tools(self) -> None:
        if self._sidebar.active == NAV_TOOLS:
            self._show_tools_grid()
        else:
            self._footer.reset()
