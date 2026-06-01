from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from t7oolkit.registry.tool_registry import registry
from t7oolkit.tools.base import Tool

ToolSelectCallback = Callable[[Tool], None]

CARD_MIN_WIDTH = 240
CARD_PADX = 12
CARD_PADY = 12


class ToolsGridView(ttk.Frame):
    def __init__(self, master: tk.Misc, on_tool_select: ToolSelectCallback, **kwargs) -> None:
        super().__init__(master, padding=24, **kwargs)
        self._on_tool_select = on_tool_select
        self._canvas = tk.Canvas(self, highlightthickness=0, bg=self._bg_color())
        self._scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._canvas.yview)
        self._scrollable = ttk.Frame(self._canvas)
        self._window_id = self._canvas.create_window((0, 0), window=self._scrollable, anchor=tk.NW)
        self._cards: list[ttk.Frame] = []

        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._scrollable.bind("<Configure>", self._on_scrollable_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind("<Configure>", self._on_resize)

        self.refresh()

    @staticmethod
    def _bg_color() -> str:
        from t7oolkit.ui.theme import COLORS

        return COLORS["bg"]

    def refresh(self) -> None:
        for card in self._cards:
            card.destroy()
        self._cards.clear()

        tools = registry.list_tools()
        ttk.Label(self._scrollable, text="工具栏", style="SectionTitle.TLabel").grid(
            row=0,
            column=0,
            columnspan=8,
            sticky=tk.W,
            pady=(0, 16),
        )

        if not tools:
            ttk.Label(
                self._scrollable,
                text="暂无已注册工具。请在 tools/register.py 中注册工具。",
                style="Muted.TLabel",
            ).grid(row=1, column=0, sticky=tk.W)
            return

        for index, tool in enumerate(tools):
            card = self._create_card(tool)
            self._cards.append(card)

        self._layout_cards()

    def _create_card(self, tool: Tool) -> ttk.Frame:
        card = ttk.Frame(self._scrollable, style="Card.TFrame", padding=16, cursor="hand2")

        title = ttk.Label(card, text=tool.name, style="CardTitle.TLabel")
        title.pack(anchor=tk.W)

        desc = ttk.Label(card, text=tool.description, style="CardDesc.TLabel", wraplength=220)
        desc.pack(anchor=tk.W, pady=(8, 0))

        for widget in (card, title, desc):
            widget.bind("<Button-1>", lambda _event, selected=tool: self._on_tool_select(selected))

        return card

    def _layout_cards(self) -> None:
        if not self._cards:
            return

        width = max(self._canvas.winfo_width(), CARD_MIN_WIDTH)
        cols = max(1, width // (CARD_MIN_WIDTH + CARD_PADX * 2))

        for card in self._cards:
            card.grid_forget()

        for index, card in enumerate(self._cards):
            row = index // cols + 1
            col = index % cols
            card.grid(
                row=row,
                column=col,
                padx=CARD_PADX,
                pady=CARD_PADY,
                sticky=tk.NSEW,
            )

        for col in range(cols):
            self._scrollable.columnconfigure(col, weight=1, uniform="tool_cards")

    def _on_resize(self, _event: tk.Event) -> None:
        self._layout_cards()

    def _on_canvas_configure(self, event: tk.Event) -> None:
        self._canvas.itemconfigure(self._window_id, width=event.width)
        self._layout_cards()

    def _on_scrollable_configure(self, _event: tk.Event) -> None:
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
