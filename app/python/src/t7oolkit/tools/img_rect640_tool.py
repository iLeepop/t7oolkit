from __future__ import annotations

import threading
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, scrolledtext

import tkinter.ttk as ttk

from t7oolkit.config import AppConfig
from t7oolkit.tools.base import StatusCallback, Tool
from t7oolkit.utils.image_resize import batch_resize_images, format_result_line, list_image_files


@dataclass(frozen=True)
class ImgRect640Tool(Tool):
    name: str = "图片缩放"
    description: str = "将文件夹内图片等比缩放至指定尺寸以内（默认 640×640）"

    def entry(self, parent: ttk.Frame, *, on_status: StatusCallback) -> None:
        config = AppConfig.load()
        root = parent.winfo_toplevel()

        input_var = tk.StringVar()
        output_var = tk.StringVar(value=config.effective_export_dir)
        size_var = tk.StringVar(value="640")
        progress_var = tk.DoubleVar(value=0)
        summary_var = tk.StringVar(value="请选择输入文件夹后开始处理。")
        running = {"value": False}

        form = ttk.Frame(parent)
        form.pack(fill=tk.X)
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="输入文件夹", style="Field.TLabel").grid(row=0, column=0, sticky=tk.W, pady=8)
        input_row = ttk.Frame(form)
        input_row.grid(row=0, column=1, sticky=tk.EW, pady=8, padx=(16, 0))
        input_row.columnconfigure(0, weight=1)
        ttk.Entry(input_row, textvariable=input_var).grid(row=0, column=0, sticky=tk.EW)
        ttk.Button(
            input_row,
            text="浏览…",
            command=lambda: _browse_directory(input_var, "选择输入文件夹"),
        ).grid(row=0, column=1, padx=(8, 0))

        ttk.Label(form, text="输出文件夹", style="Field.TLabel").grid(row=1, column=0, sticky=tk.W, pady=8)
        output_row = ttk.Frame(form)
        output_row.grid(row=1, column=1, sticky=tk.EW, pady=8, padx=(16, 0))
        output_row.columnconfigure(0, weight=1)
        ttk.Entry(output_row, textvariable=output_var).grid(row=0, column=0, sticky=tk.EW)
        ttk.Button(
            output_row,
            text="浏览…",
            command=lambda: _browse_directory(output_var, "选择输出文件夹", initial=output_var.get()),
        ).grid(row=0, column=1, padx=(8, 0))

        ttk.Label(form, text="最大边长", style="Field.TLabel").grid(row=2, column=0, sticky=tk.W, pady=8)
        size_spin = ttk.Spinbox(form, from_=1, to=8192, textvariable=size_var, width=10)
        size_spin.grid(row=2, column=1, sticky=tk.W, pady=8, padx=(16, 0))

        action_row = ttk.Frame(parent)
        action_row.pack(fill=tk.X, pady=(8, 0))
        run_btn = ttk.Button(action_row, text="开始处理", style="Accent.TButton")
        run_btn.pack(anchor=tk.W)

        ttk.Label(parent, textvariable=summary_var, style="Muted.TLabel").pack(anchor=tk.W, pady=(16, 8))

        progress = ttk.Progressbar(parent, variable=progress_var, maximum=100)
        progress.pack(fill=tk.X, pady=(0, 12))

        log_box = scrolledtext.ScrolledText(parent, height=14, wrap=tk.WORD, state=tk.DISABLED)
        log_box.pack(fill=tk.BOTH, expand=True)

        def append_log(message: str) -> None:
            log_box.configure(state=tk.NORMAL)
            log_box.insert(tk.END, message + "\n")
            log_box.see(tk.END)
            log_box.configure(state=tk.DISABLED)

        def set_running(active: bool) -> None:
            running["value"] = active
            state = tk.DISABLED if active else tk.NORMAL
            run_btn.configure(state=state)

        def finish_ui(message: str, success_count: int, error_count: int) -> None:
            progress_var.set(100 if success_count or error_count else 0)
            summary_var.set(message)
            on_status(message)
            set_running(False)

        def run() -> None:
            input_dir = input_var.get().strip()
            output_dir = output_var.get().strip()
            if not input_dir:
                summary_var.set("请先选择输入文件夹。")
                return
            if not Path(input_dir).is_dir():
                summary_var.set("输入文件夹不存在。")
                return
            if not output_dir:
                summary_var.set("请先选择输出文件夹。")
                return

            try:
                max_size = int(size_var.get())
            except ValueError:
                summary_var.set("最大边长必须是整数。")
                return
            if max_size <= 0:
                summary_var.set("最大边长必须大于 0。")
                return

            files = list_image_files(input_dir)
            if not files:
                summary_var.set("输入文件夹中没有可处理的图片。")
                return

            log_box.configure(state=tk.NORMAL)
            log_box.delete("1.0", tk.END)
            log_box.configure(state=tk.DISABLED)

            set_running(True)
            progress_var.set(0)
            summary_var.set(f"正在处理 {len(files)} 个图片…")
            on_status(f"正在处理 {len(files)} 个图片…")

            current_config = AppConfig.load()

            def worker() -> None:
                results, errors = batch_resize_images(
                    input_dir,
                    output_dir,
                    max_size=max_size,
                    workers=current_config.thread_count,
                )

                lines = [format_result_line(item) for item in results]
                lines.extend(f"{item.filename}: 失败 - {item.message}" for item in errors)

                message = f"处理完成：成功 {len(results)} 个，失败 {len(errors)} 个"

                def show_results() -> None:
                    for line in lines:
                        append_log(line)
                    finish_ui(message, len(results), len(errors))

                root.after(0, show_results)

            threading.Thread(target=worker, daemon=True).start()

        run_btn.configure(command=run)


def _browse_directory(var: tk.StringVar, title: str, initial: str = "") -> None:
    selected = filedialog.askdirectory(title=title, initialdir=initial or None)
    if selected:
        var.set(selected)
