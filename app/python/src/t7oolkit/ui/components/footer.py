from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class StatusFooter(ttk.Frame):
    DEFAULT_STATUS = "就绪"

    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, style="Footer.TFrame", padding=(20, 10), **kwargs)
        self._status_var = tk.StringVar(value=self.DEFAULT_STATUS)
        self._build()

    def _build(self) -> None:
        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=(0, 8))

        self._label = ttk.Label(self, textvariable=self._status_var, style="Status.TLabel")
        self._label.pack(anchor=tk.W)

    def set_status(self, message: str) -> None:
        self._status_var.set(message)

    def reset(self) -> None:
        self.set_status(self.DEFAULT_STATUS)

    def set_tool_active(self, tool_name: str) -> None:
        self.set_status(f"正在使用「{tool_name}」")
