from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from t7oolkit import __version__


class HeaderBar(ttk.Frame):
    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, style="Header.TFrame", padding=(20, 16), **kwargs)
        self._build()

    def _build(self) -> None:
        title = ttk.Label(self, text="t7oolkit", style="HeaderTitle.TLabel")
        title.pack(anchor=tk.W)

        subtitle = ttk.Label(
            self,
            text=f"v{__version__} · 工具箱",
            style="HeaderSubtitle.TLabel",
        )
        subtitle.pack(anchor=tk.W, pady=(4, 0))

        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=(12, 0))
