from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import filedialog, ttk

from t7oolkit.config import AppConfig

SaveCallback = Callable[[], None]


class SettingsPanel(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        config: AppConfig,
        on_save: SaveCallback | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, padding=24, **kwargs)
        self.config = config
        self._on_save = on_save
        self._thread_var = tk.StringVar(value=str(config.thread_count))
        self._export_var = tk.StringVar(value=config.export_dir)
        self._message_var = tk.StringVar(value="")
        self._build()

    def _build(self) -> None:
        ttk.Label(self, text="基础配置", style="SectionTitle.TLabel").pack(anchor=tk.W)
        ttk.Label(
            self,
            text="通用线程数量与默认导出位置将应用于各工具。",
            style="Muted.TLabel",
        ).pack(anchor=tk.W, pady=(6, 20))

        form = ttk.Frame(self)
        form.pack(fill=tk.X)
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="线程数量", style="Field.TLabel").grid(row=0, column=0, sticky=tk.W, pady=8)
        thread_spin = ttk.Spinbox(
            form,
            from_=1,
            to=32,
            textvariable=self._thread_var,
            width=8,
        )
        thread_spin.grid(row=0, column=1, sticky=tk.W, pady=8, padx=(16, 0))

        ttk.Label(form, text="默认导出位置", style="Field.TLabel").grid(row=1, column=0, sticky=tk.W, pady=8)
        export_row = ttk.Frame(form)
        export_row.grid(row=1, column=1, sticky=tk.EW, pady=8, padx=(16, 0))
        export_row.columnconfigure(0, weight=1)

        export_entry = ttk.Entry(export_row, textvariable=self._export_var)
        export_entry.grid(row=0, column=0, sticky=tk.EW)

        browse_btn = ttk.Button(export_row, text="浏览…", command=self._browse_export_dir)
        browse_btn.grid(row=0, column=1, padx=(8, 0))

        actions = ttk.Frame(self)
        actions.pack(fill=tk.X, pady=(24, 8))

        save_btn = ttk.Button(actions, text="保存", style="Accent.TButton", command=self._save)
        save_btn.pack(anchor=tk.W)

        message = ttk.Label(actions, textvariable=self._message_var, style="Muted.TLabel")
        message.pack(anchor=tk.W, pady=(12, 0))

    def _browse_export_dir(self) -> None:
        initial = self._export_var.get().strip() or self.config.effective_export_dir
        selected = filedialog.askdirectory(title="选择默认导出位置", initialdir=initial)
        if selected:
            self._export_var.set(selected)

    def _save(self) -> None:
        try:
            thread_count = int(self._thread_var.get())
        except ValueError:
            self._message_var.set("线程数量必须是整数。")
            return

        if not 1 <= thread_count <= 32:
            self._message_var.set("线程数量需在 1 到 32 之间。")
            return

        self.config.thread_count = thread_count
        self.config.export_dir = self._export_var.get().strip()
        self.config.save()
        self._message_var.set("配置已保存。")
        if self._on_save:
            self._on_save()

    def refresh(self) -> None:
        self._thread_var.set(str(self.config.thread_count))
        self._export_var.set(self.config.export_dir)
        self._message_var.set("")
