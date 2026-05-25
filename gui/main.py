# main.py — 🐼  PANDACLEAN  🐼 Launcher


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, sys
from datetime import datetime

import theme as T
from theme import *
from tkinter import ttk

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

# ── Lazy imports for each tool module ─────────────────────────────────────────
def _get_tools():
    from gui_file_handler import FileHandlerApp
    from gui_datatype import DatatypeApp
    from gui_duplicates import DuplicatesApp
    from gui_formatting import FormattingApp
    from gui_missing import MissingApp
    return FileHandlerApp, DatatypeApp, DuplicatesApp, FormattingApp, MissingApp


TOOLS_META = [
    {
        "title":    "File Handler",
        "subtitle": "Load · Save · Inspect",
        "icon":     "📂",
        "key":      "file_handler",
        "accent":   ACCENT,
    },
    {
        "title":    "Datatype Converter",
        "subtitle": "Cast · Validate · Clean",
        "icon":     "🔢",
        "key":      "datatype",
        "accent":   "#A78BFA",
    },
    {
        "title":    "Duplicates Handler",
        "subtitle": "Detect · Remove · Mark",
        "icon":     "🔁",
        "key":      "duplicates",
        "accent":   DANGER,
    },
    {
        "title":    "Formatting Handler",
        "subtitle": "Case · Trim · Replace",
        "icon":     "✏️",
        "key":      "formatting",
        "accent":   WARN,
    },
    {
        "title":    "Missing Values",
        "subtitle": "Detect · Drop · Impute",
        "icon":     "🔍",
        "key":      "missing",
        "accent":   "#F472B6",
    },
]


class LauncherApp(tk.Tk):
    """Main launcher — owns the shared DataFrame and theme state."""

    def __init__(self):
        super().__init__()
        T.register_window(self)
        apply_base_style(self, "Data Cleaning Suite")
        center_window(self, 800, 620)
        self.resizable(True, True)

        # ── Shared state ──────────────────────────────────────────────────
        self.shared_df   = None        # the one DataFrame shared by all tools
        self.shared_path = None        # path label for display
        self._open_tools = {}          # key → Toplevel instance

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── UI build ──────────────────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()
        self._build_file_bar()
        self._build_tool_grid()
        self._build_footer()

    def _build_header(self):
        self.hero = tk.Frame(self, bg=T.BG_CARD, pady=26)
        self.hero.pack(fill="x")

        left = tk.Frame(self.hero, bg=T.BG_CARD)
        left.pack(side="left", expand=True)

        self.lbl_title = tk.Label(left, text="🐼  PANDACLEAN  🐼",
                                   font=FONT_TITLE, fg=ACCENT, bg=T.BG_CARD)
        self.lbl_title.pack()
        self.lbl_sub = tk.Label(left,
                                 text="Professional pandas- automated cleaning toolkit",
                                 font=FONT_BODY, fg=T.TEXT_MUTED, bg=T.BG_CARD)
        self.lbl_sub.pack(pady=(4, 0))

        # Theme toggle button (right side of header)
        self.theme_btn = tk.Button(
            self.hero,
            text="☀  Light Mode" if T.get_theme() == "dark" else "☾  Dark Mode",
            command=self._toggle_theme,
            bg=T.BG_HOVER, fg=T.TEXT_PRIMARY,
            activebackground=ACCENT, activeforeground=T.BG_DARK,
            font=FONT_SMALL, relief="flat", cursor="hand2",
            padx=12, pady=6, bd=0
        )
        self.theme_btn.pack(side="right", padx=20)

        self.accent_line = tk.Frame(self, bg=ACCENT, height=2)
        self.accent_line.pack(fill="x")

        self.sub_bar = tk.Frame(self, bg=T.BG_DARK, pady=12)
        self.sub_bar.pack(fill="x")
        self.lbl_select = tk.Label(self.sub_bar,
                                    text="S E L E C T   A   M O D U L E   T O   L A U N C H",
                                    font=FONT_SMALL, fg=T.TEXT_MUTED, bg=T.BG_DARK)
        self.lbl_select.pack()

    def _build_file_bar(self):
        """Central file-load bar — load once, all tools share it."""
        self.file_bar = tk.Frame(self, bg=T.BG_CARD, pady=10)
        self.file_bar.pack(fill="x", padx=PAD)

        tk.Label(self.file_bar, text="SHARED FILE:", font=FONT_HEADING,
                 fg=ACCENT, bg=T.BG_CARD).pack(side="left", padx=(0, 10))

        self._make_fbar_btn("📂  Load CSV",   self._load_csv,   ACCENT,    T.BG_DARK)
        self._make_fbar_btn("📊  Load Excel", self._load_excel, T.BG_HOVER, T.TEXT_PRIMARY)

        self.file_status = tk.Label(self.file_bar, text="No file loaded — load once, use everywhere",
                                     font=FONT_SMALL, fg=T.TEXT_MUTED, bg=T.BG_CARD)
        self.file_status.pack(side="left", padx=14)

        # Export button (far right)
        self._make_fbar_btn("💾  Export CSV",   self._export_csv,   SUCCESS, T.BG_DARK, side="right")
        self._make_fbar_btn("💾  Export Excel", self._export_excel, SUCCESS, T.BG_DARK, side="right")

        # Separator
        tk.Frame(self, bg=T.BORDER, height=1).pack(fill="x", padx=PAD, pady=(4, 0))

    def _make_fbar_btn(self, text, cmd, bg, fg, side="left"):
        b = tk.Button(self.file_bar, text=text, command=cmd,
                      bg=bg, fg=fg, activebackground=ACCENT_DIM, activeforeground=T.BG_DARK,
                      font=FONT_SMALL, relief="flat", cursor="hand2",
                      padx=10, pady=5, bd=0)
        b.pack(side=side, padx=4)
        return b

    def _build_tool_grid(self):
        self.grid_frame = tk.Frame(self, bg=T.BG_DARK)
        self.grid_frame.pack(fill="both", expand=True, padx=PAD, pady=8)

        self._cards = {}
        for i, tool in enumerate(TOOLS_META):
            row = i // 3
            col = i %  3
            card = self._make_card(self.grid_frame, tool)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            self._cards[tool["key"]] = card

        for c in range(3):
            self.grid_frame.columnconfigure(c, weight=1)
        for r in range(2):
            self.grid_frame.rowconfigure(r, weight=1)

    def _build_footer(self):
        self.footer = tk.Frame(self, bg=T.BG_CARD, pady=10)
        self.footer.pack(fill="x", side="bottom")
        self.footer_lbl = tk.Label(
            self.footer,
            text="🐼  PANDACLEAN  🐼·  Built with Python & Tkinter  ·  Load file once, use everywhere",
            font=FONT_SMALL, fg=T.TEXT_MUTED, bg=T.BG_CARD
        )
        self.footer_lbl.pack()

    def _make_card(self, parent, tool):
        accent = tool["accent"]
        c = T.get_colors()

        card = tk.Frame(parent, bg=c["BG_CARD"], cursor="hand2",
                        padx=18, pady=18, relief="flat", bd=0)

        bar   = tk.Frame(card, bg=accent, height=3)
        bar.pack(fill="x", pady=(0, 12))

        icon  = tk.Label(card, text=tool["icon"], font=("Segoe UI Emoji", 28),
                         bg=c["BG_CARD"])
        icon.pack()

        title = tk.Label(card, text=tool["title"],
                         font=FONT_HEADING, fg=c["TEXT_PRIMARY"], bg=c["BG_CARD"])
        title.pack(pady=(6, 2))

        sub   = tk.Label(card, text=tool["subtitle"],
                         font=FONT_SMALL, fg=c["TEXT_MUTED"], bg=c["BG_CARD"])
        sub.pack()

        btn_frame = tk.Frame(card, bg=c["BG_CARD"])
        btn_frame.pack(pady=(14, 0))
        btn = tk.Button(btn_frame, text="OPEN  →",
                        command=lambda k=tool["key"]: self._launch(k),
                        bg=accent, fg=c["BG_DARK"],
                        activebackground=c["BG_HOVER"],
                        activeforeground=c["TEXT_PRIMARY"],
                        font=("Consolas", 10, "bold"),
                        relief="flat", cursor="hand2",
                        padx=16, pady=6, bd=0)
        btn.pack()

        # Store widget refs for theme refresh
        card._theme_widgets = {
            "card": card, "icon": icon, "title": title,
            "sub": sub, "btn_frame": btn_frame
        }
        card._accent = accent

        def on_enter(e):
            hover = T.get_colors()["BG_HOVER"]
            card.config(bg=hover); icon.config(bg=hover)
            title.config(bg=hover); sub.config(bg=hover)
            btn_frame.config(bg=hover); bar.config(bg=accent)
        def on_leave(e):
            bg = T.get_colors()["BG_CARD"]
            card.config(bg=bg); icon.config(bg=bg)
            title.config(bg=bg); sub.config(bg=bg)
            btn_frame.config(bg=bg); bar.config(bg=accent)

        for w in [card, bar, icon, title, sub, btn_frame]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", lambda e, k=tool["key"]: self._launch(k))

        return card

    # ── Theme ─────────────────────────────────────────────────────────────

    def _toggle_theme(self):
        new = "light" if T.get_theme() == "dark" else "dark"
        T.set_theme(new)   # broadcasts apply_theme() to all registered windows

    def apply_theme(self):
        """Called by theme.set_theme() to repaint this window."""
        c = T.get_colors()
        self.configure(bg=c["BG_DARK"])

        self.hero.config(bg=c["BG_CARD"])
        self.lbl_title.config(bg=c["BG_CARD"])
        self.lbl_sub.config(bg=c["BG_CARD"], fg=c["TEXT_MUTED"])
        self.theme_btn.config(
            bg=c["BG_HOVER"], fg=c["TEXT_PRIMARY"],
            text="☀  Light Mode" if T.get_theme() == "dark" else "☾  Dark Mode"
        )
        self.sub_bar.config(bg=c["BG_DARK"])
        self.lbl_select.config(bg=c["BG_DARK"], fg=c["TEXT_MUTED"])

        self.file_bar.config(bg=c["BG_CARD"])
        self.file_status.config(bg=c["BG_CARD"], fg=c["TEXT_MUTED"])
        for w in self.file_bar.winfo_children():
            try: w.config(bg=c["BG_CARD"] if isinstance(w, tk.Label) else w.cget("bg"))
            except: pass

        self.grid_frame.config(bg=c["BG_DARK"])

        # Repaint cards
        for key, card in self._cards.items():
            tw = card._theme_widgets
            acc = card._accent
            card.config(bg=c["BG_CARD"])
            tw["icon"].config(bg=c["BG_CARD"])
            tw["title"].config(bg=c["BG_CARD"], fg=c["TEXT_PRIMARY"])
            tw["sub"].config(bg=c["BG_CARD"], fg=c["TEXT_MUTED"])
            tw["btn_frame"].config(bg=c["BG_CARD"])

        self.footer.config(bg=c["BG_CARD"])
        self.footer_lbl.config(bg=c["BG_CARD"], fg=c["TEXT_MUTED"])

    # ── File loading (shared) ─────────────────────────────────────────────

    def _load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path: return
        try:
            self.shared_df   = pd.read_csv(path)
            self.shared_path = path
            self._on_file_loaded(path)
            self._push_df_to_open_tools()
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def _load_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not path: return
        try:
            self.shared_df   = pd.read_excel(path)
            self.shared_path = path
            self._on_file_loaded(path)
            self._push_df_to_open_tools()
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def _on_file_loaded(self, path):
        name = os.path.basename(path)
        r, c = self.shared_df.shape
        self.file_status.config(
            text=f"✔  {name}  ({r} rows × {c} cols)  — shared across all tools",
            fg=SUCCESS
        )

    def _push_df_to_open_tools(self):
        """Push (or re-push) the shared df into every already-open tool."""
        for win in list(self._open_tools.values()):
            try:
                if win.winfo_exists():
                    win.receive_df(self.shared_df.copy(), self.shared_path)
            except Exception:
                pass

    # ── Export (uses current state of shared_df) ──────────────────────────

    def _export_csv(self):
        if self.shared_df is None:
            messagebox.showwarning("No Data", "Load a file first."); return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV", "*.csv")])
        if not path: return
        self.shared_df.to_csv(path, index=False)
        messagebox.showinfo("Saved", f"Saved to {os.path.basename(path)}")

    def _export_excel(self):
        if self.shared_df is None:
            messagebox.showwarning("No Data", "Load a file first."); return
        path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                            filetypes=[("Excel", "*.xlsx")])
        if not path: return
        self.shared_df.to_excel(path, index=False)
        messagebox.showinfo("Saved", f"Saved to {os.path.basename(path)}")

    # ── Tool launching ────────────────────────────────────────────────────

    def _launch(self, key):
        # If already open, just raise it
        if key in self._open_tools:
            win = self._open_tools[key]
            try:
                if win.winfo_exists():
                    win.lift(); win.focus_force(); return
            except Exception:
                pass

        FileHandlerApp, DatatypeApp, DuplicatesApp, FormattingApp, MissingApp = _get_tools()
        klass_map = {
            "file_handler": FileHandlerApp,
            "datatype":     DatatypeApp,
            "duplicates":   DuplicatesApp,
            "formatting":   FormattingApp,
            "missing":      MissingApp,
        }
        klass = klass_map[key]

        # Pass launcher reference so tool can push df changes back
        win = klass(launcher=self)
        self._open_tools[key] = win

        # If a file is already loaded, immediately pass it to the new tool
        if self.shared_df is not None:
            win.receive_df(self.shared_df.copy(), self.shared_path)

        def on_close():
            self._open_tools.pop(key, None)
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

    def push_df_from_tool(self, df, path=None):
        """Called by a tool when it saves/modifies data, updating the shared df."""
        self.shared_df   = df.copy()
        if path:
            self.shared_path = path
        self._on_file_loaded(path or self.shared_path or "modified")
        self._push_df_to_open_tools()

    def _on_close(self):
        T.unregister_window(self)
        self.destroy()


if __name__ == "__main__":
    LauncherApp().mainloop()