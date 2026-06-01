import tkinter as tk

from t7oolkit.config import AppConfig
from t7oolkit.tools.register import register_all_tools
from t7oolkit.ui.main_window import MainWindow
from t7oolkit.ui.theme import apply_theme


def main() -> None:
    config = AppConfig.load()
    register_all_tools()

    root = tk.Tk()
    apply_theme(root)
    MainWindow(root, config=config)

    def on_close() -> None:
        config.save()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
