from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

NavCallback = Callable[[str], None]

NAV_TOOLS = "tools"
NAV_SETTINGS = "settings"


class SidebarNav(ttk.Frame):
    def __init__(self, master: tk.Misc, on_navigate: NavCallback, **kwargs) -> None:
        super().__init__(master, style="Sidebar.TFrame", padding=(12, 16), **kwargs)
        self._on_navigate = on_navigate
        self._active = NAV_TOOLS
        self._buttons: dict[str, ttk.Button] = {}
        self._build()

    def _build(self) -> None:
        ttk.Label(self, text="导航", style="Muted.TLabel").pack(anchor=tk.W, pady=(0, 8))

        self._buttons[NAV_TOOLS] = ttk.Button(
            self,
            text="工具栏",
            style="SidebarActive.TButton",
            command=lambda: self.select(NAV_TOOLS),
        )
        self._buttons[NAV_TOOLS].pack(fill=tk.X, pady=4)

        self._buttons[NAV_SETTINGS] = ttk.Button(
            self,
            text="基础配置",
            style="Sidebar.TButton",
            command=lambda: self.select(NAV_SETTINGS),
        )
        self._buttons[NAV_SETTINGS].pack(fill=tk.X, pady=4)

        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=(16, 0))

    def select(self, nav_id: str) -> None:
        if nav_id == self._active:
            return

        self._buttons[self._active].configure(style="Sidebar.TButton")
        self._active = nav_id
        self._buttons[self._active].configure(style="SidebarActive.TButton")
        self._on_navigate(nav_id)

    @property
    def active(self) -> str:
        return self._active
