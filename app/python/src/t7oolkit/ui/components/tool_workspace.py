from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from t7oolkit.tools.base import Tool

BackCallback = Callable[[], None]
StatusCallback = Callable[[str], None]


class ToolWorkspaceView(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        on_back: BackCallback,
        on_status: StatusCallback,
        **kwargs,
    ) -> None:
        super().__init__(master, padding=24, **kwargs)
        self._on_back = on_back
        self._on_status = on_status
        self._current_tool: Tool | None = None

        self._header = ttk.Frame(self)
        self._header.pack(fill=tk.X)

        self._back_btn = ttk.Button(self._header, text="← 返回", command=self._handle_back)
        self._back_btn.pack(side=tk.LEFT)

        self._title = ttk.Label(self._header, text="", style="SectionTitle.TLabel")
        self._title.pack(side=tk.LEFT, padx=(16, 0))

        self._content = ttk.Frame(self)
        self._content.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

    def open_tool(self, tool: Tool) -> None:
        self.clear()
        self._current_tool = tool
        self._title.configure(text=tool.name)
        tool.entry(self._content, on_status=self._on_status)

    def clear(self) -> None:
        for child in self._content.winfo_children():
            child.destroy()
        self._current_tool = None
        self._title.configure(text="")

    def _handle_back(self) -> None:
        self.clear()
        self._on_back()

    @property
    def current_tool(self) -> Tool | None:
        return self._current_tool
