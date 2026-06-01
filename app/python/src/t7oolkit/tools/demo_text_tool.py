from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass

import tkinter.ttk as ttk

from t7oolkit.tools.base import StatusCallback, Tool


@dataclass(frozen=True)
class DemoTextTool(Tool):
    name: str = "文本处理"
    description: str = "简单的文本输入/输出演示工具"

    def entry(self, parent: ttk.Frame, *, on_status: StatusCallback) -> None:
        input_var = tk.StringVar(value="Hello, t7oolkit!")
        result_var = tk.StringVar(value="")

        ttk.Label(parent, text="输入文本", style="Field.TLabel").pack(anchor=tk.W)
        entry = ttk.Entry(parent, textvariable=input_var, width=48)
        entry.pack(anchor=tk.W, pady=(8, 16))

        output = ttk.Label(parent, textvariable=result_var, style="Muted.TLabel", wraplength=560)
        output.pack(anchor=tk.W, pady=(0, 16))

        def run() -> None:
            on_status("处理中…")
            text = input_var.get().strip()
            result_var.set(f"字符数：{len(text)} · 大写：{text.upper()}")
            on_status("处理完成")

        ttk.Button(parent, text="运行", style="Accent.TButton", command=run).pack(anchor=tk.W)
