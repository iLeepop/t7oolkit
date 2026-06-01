from __future__ import annotations

import tkinter as tk
from tkinter import ttk

COLORS = {
    "bg": "#F5F5F7",
    "surface": "#FFFFFF",
    "border": "#E5E5EA",
    "accent": "#007AFF",
    "accent_hover": "#0066DD",
    "text": "#1D1D1F",
    "text_secondary": "#86868B",
    "sidebar_active": "#E8F2FF",
    "footer_bg": "#FAFAFA",
}


def apply_theme(root: tk.Tk) -> ttk.Style:
    style = ttk.Style(root)
    style.theme_use("clam")

    root.configure(bg=COLORS["bg"])

    style.configure(".", background=COLORS["bg"], foreground=COLORS["text"], font=("", 13))
    style.configure("TFrame", background=COLORS["bg"])
    style.configure("Surface.TFrame", background=COLORS["surface"])
    style.configure("Card.TFrame", background=COLORS["surface"], relief="solid", borderwidth=1)
    style.configure("Header.TFrame", background=COLORS["surface"])
    style.configure("Sidebar.TFrame", background=COLORS["surface"])
    style.configure("Footer.TFrame", background=COLORS["footer_bg"])

    style.configure("HeaderTitle.TLabel", background=COLORS["surface"], foreground=COLORS["text"], font=("", 18, "bold"))
    style.configure("HeaderSubtitle.TLabel", background=COLORS["surface"], foreground=COLORS["text_secondary"], font=("", 12))
    style.configure("SectionTitle.TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=("", 15, "bold"))
    style.configure("CardTitle.TLabel", background=COLORS["surface"], foreground=COLORS["text"], font=("", 14, "bold"))
    style.configure("CardDesc.TLabel", background=COLORS["surface"], foreground=COLORS["text_secondary"], font=("", 12))
    style.configure("Muted.TLabel", background=COLORS["bg"], foreground=COLORS["text_secondary"], font=("", 12))
    style.configure("Status.TLabel", background=COLORS["footer_bg"], foreground=COLORS["text_secondary"], font=("", 12))
    style.configure("Field.TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=("", 13))

    style.configure(
        "Sidebar.TButton",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        borderwidth=0,
        padding=(16, 12),
        anchor="w",
        font=("", 13),
    )
    style.map(
        "Sidebar.TButton",
        background=[("active", COLORS["sidebar_active"]), ("pressed", COLORS["sidebar_active"])],
        foreground=[("active", COLORS["accent"])],
    )
    style.configure(
        "SidebarActive.TButton",
        background=COLORS["sidebar_active"],
        foreground=COLORS["accent"],
        borderwidth=0,
        padding=(16, 12),
        anchor="w",
        font=("", 13, "bold"),
    )
    style.map(
        "SidebarActive.TButton",
        background=[("active", COLORS["sidebar_active"]), ("pressed", COLORS["sidebar_active"])],
        foreground=[("active", COLORS["accent"])],
    )

    style.configure(
        "Accent.TButton",
        background=COLORS["accent"],
        foreground="#FFFFFF",
        borderwidth=0,
        padding=(14, 8),
        font=("", 13),
    )
    style.map(
        "Accent.TButton",
        background=[("active", COLORS["accent_hover"]), ("pressed", COLORS["accent_hover"])],
        foreground=[("active", "#FFFFFF")],
    )
    style.configure("TButton", padding=(12, 8), font=("", 13))
    style.configure("TEntry", padding=6)
    style.configure("TSpinbox", padding=6)

    return style
