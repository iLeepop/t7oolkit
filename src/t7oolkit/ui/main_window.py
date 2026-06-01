import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._setup_window()
        self._build_ui()

    def _setup_window(self) -> None:
        self.root.title("t7oolkit")
        self.root.geometry("800x600")
        self.root.minsize(640, 480)

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(container, text="Welcome to t7oolkit", font=("", 18, "bold"))
        title.pack(anchor=tk.W, pady=(0, 8))

        subtitle = ttk.Label(container, text="Tkinter application starter template.")
        subtitle.pack(anchor=tk.W)
