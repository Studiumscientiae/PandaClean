# gui_duplicates.py — Duplicates Handler Tool

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import theme as T
from theme import *
from tool_base import ToolWindow, _apply_treeview_style

try:
    import pandas as pd
except ImportError:
    pd = None


def _make_scrollable_left(parent):
    c = T.get_colors()
    canvas = tk.Canvas(parent, bg=c["BG_CARD"], highlightthickness=0, bd=0)
    vsb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    inner = tk.Frame(canvas, bg=c["BG_CARD"], padx=14, pady=14)
    win_id = canvas.create_window((0, 0), window=inner, anchor="nw")
    def _on_configure(e): canvas.configure(scrollregion=canvas.bbox("all"))
    inner.bind("<Configure>", _on_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    def _mw(e): canvas.yview_scroll(int(-1*(e.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _mw)
    return inner


class DuplicatesApp(ToolWindow):

    def __init__(self, launcher=None):
        super().__init__(launcher=launcher, title="Duplicates Handler", width=960, height=700)

    def _build_ui(self):
        c = T.get_colors()
        self.hdr = tk.Frame(self, bg=c["BG_CARD"], pady=14)
        self.hdr.pack(fill="x")
        self.hdr_title = tk.Label(self.hdr, text="⬡  DUPLICATES HANDLER", font=FONT_TITLE,
                                   fg=ACCENT, bg=c["BG_CARD"])
        self.hdr_title.pack(side="left", padx=PAD)
        self.hdr_sub = tk.Label(self.hdr,
                                 text="Detect · Remove · Mark  |  Ctrl+Z Undo  |  Ctrl+Y Redo",
                                 font=FONT_SMALL, fg=c["TEXT_MUTED"], bg=c["BG_CARD"])
        self.hdr_sub.pack(side="left", padx=6)

        self.stats_frame = tk.Frame(self, bg=c["BG_DARK"], pady=8)
        self.stats_frame.pack(fill="x", padx=PAD)
        self._build_stat_cards()

        self.body = tk.Frame(self, bg=c["BG_DARK"])
        self.body.pack(fill="both", expand=True, padx=PAD, pady=(0, PAD))

        self.left_outer = tk.Frame(self.body, bg=c["BG_CARD"], width=270)
        self.left_outer.pack(side="left", fill="y", padx=(0, 10))
        self.left_outer.pack_propagate(False)
        left = _make_scrollable_left(self.left_outer)

        self.right_frame = tk.Frame(self.body, bg=c["BG_CARD"], padx=14, pady=14)
        self.right_frame.pack(side="left", fill="both", expand=True)

        self._build_left(left)
        self._build_right(self.right_frame)

        self.status_var = tk.StringVar(value="Waiting for file from launcher…")
        self.status_lbl = tk.Label(self, textvariable=self.status_var, font=FONT_SMALL,
                                    fg=c["TEXT_MUTED"], bg=c["BG_DARK"], anchor="w")
        self.status_lbl.pack(fill="x", padx=PAD, pady=(0, 6))

    def _build_stat_cards(self):
        c = T.get_colors()
        for w in self.stats_frame.winfo_children(): w.destroy()
        for label, val, color in [
            ("TOTAL ROWS",  str(len(self.df)) if self.df is not None else "—", ACCENT),
            ("DUPLICATES",  str(self.df.duplicated().sum()) if self.df is not None else "—", DANGER),
            ("UNIQUE ROWS", str(len(self.df.drop_duplicates())) if self.df is not None else "—", SUCCESS),
        ]:
            card = tk.Frame(self.stats_frame, bg=c["BG_CARD"], padx=20, pady=10)
            card.pack(side="left", padx=(0, 10))
            tk.Label(card, text=val, font=("Consolas", 20, "bold"),
                     fg=color, bg=c["BG_CARD"]).pack()
            tk.Label(card, text=label, font=FONT_SMALL,
                     fg=c["TEXT_MUTED"], bg=c["BG_CARD"]).pack()

    def _build_left(self, parent):
        c = T.get_colors()

        def sep(): tk.Frame(parent, bg=T.BORDER, height=1).pack(fill="x", pady=12)
        def lbl(text): tk.Label(parent, text=text, font=FONT_HEADING,
                                 fg=ACCENT, bg=c["BG_CARD"]).pack(anchor="w")
        def div(): tk.Frame(parent, bg=T.BORDER, height=1).pack(fill="x", pady=(4, 10))

        def btn(text, cmd, color=ACCENT, fg_=None):
            fg_ = fg_ or c["BG_DARK"]
            b = tk.Button(parent, text=text, command=cmd, bg=color, fg=fg_,
                          activebackground=ACCENT_DIM, activeforeground=c["BG_DARK"],
                          font=FONT_BODY, relief="flat", cursor="hand2",
                          padx=10, pady=7, width=22, bd=0)
            b.bind("<Enter>", lambda e: b.config(bg=ACCENT_DIM if color==ACCENT else c["BG_HOVER"]))
            b.bind("<Leave>", lambda e: b.config(bg=color))
            return b

        lbl("DUPLICATE ACTIONS"); div()
        btn("🔍  Check Duplicates",   self._check_dups,   WARN,       c["BG_DARK"]).pack(fill="x", pady=4)
        btn("🗑  Remove Duplicates",   self._remove_dups,  DANGER,     "#fff").pack(fill="x", pady=4)
        btn("🔃  Keep Last Duplicate", self._keep_last,    c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=4)
        btn("🏷  Mark Duplicates",     self._mark_dups,    c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=4)
        sep()
        lbl("BY COLUMN"); div()
        self.col_var = tk.StringVar()
        self.col_combo = ttk.Combobox(parent, textvariable=self.col_var,
                                       state="readonly", font=FONT_BODY)
        self.col_combo.pack(fill="x", pady=(0, 6))
        btn("🗑  Remove by Column", self._remove_by_col, DANGER, "#fff").pack(fill="x", pady=4)
        sep()
        lbl("UNDO / REDO"); div()
        btn("↩  Undo  (Ctrl+Z)", self._undo, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=4)
        btn("↪  Redo  (Ctrl+Y)", self._redo, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=4)
        sep()
        lbl("SAVE & LOG"); div()
        btn("💾  Save Result CSV", self._save_csv,   SUCCESS,       c["BG_DARK"]).pack(fill="x", pady=4)
        btn("📋  Export Action Log", self._export_log, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=4)

    def _build_right(self, parent):
        c = T.get_colors()
        self.preview_lbl = tk.Label(parent, text="DATAFRAME PREVIEW", font=FONT_HEADING,
                                     fg=ACCENT, bg=c["BG_CARD"])
        self.preview_lbl.pack(anchor="w")
        self.divider = tk.Frame(parent, bg=T.BORDER, height=1)
        self.divider.pack(fill="x", pady=(4, 10))

        frame = tk.Frame(parent, bg=c["BG_CARD"])
        frame.pack(fill="both", expand=True)
        self._tree_frame = frame

        _apply_treeview_style("Dup")
        self.tree = ttk.Treeview(frame, style="Dup.Treeview",
                                  show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1); frame.columnconfigure(0, weight=1)

        self.row_info = tk.StringVar(value="No file loaded.")
        self.info_lbl = tk.Label(parent, textvariable=self.row_info, font=FONT_SMALL,
                                  fg=c["TEXT_MUTED"], bg=c["BG_CARD"], anchor="w")
        self.info_lbl.pack(anchor="w", pady=(8, 0))

    # ── Actions ───────────────────────────────────────────────────────────

    def _post_load(self, path):
        if self.df is not None:
            self.col_combo["values"] = list(self.df.columns)
            if len(self.df.columns): self.col_var.set(self.df.columns[0])
        self._refresh()
        name = os.path.basename(path) if path else "shared file"
        self._set_status(f"✔  Loaded: {name}")

    def _check_dups(self):
        if not self._need_df(): return
        dups = self.df[self.df.duplicated()]
        self._show_popup(f"Duplicate Rows ({len(dups)} found)", dups.to_string())

    def _remove_dups(self):
        if not self._need_df(): return
        def do_it():
            self._save_state()
            before = len(self.df)
            self.df = self.df.drop_duplicates(keep="first")
            self._refresh()
            self._push_to_launcher()
            self._log(f"Removed {before - len(self.df)} duplicate rows.")
            self._set_status(f"✔  Removed {before - len(self.df)} rows.", SUCCESS)
        self._confirm_preview("Remove Duplicate Rows", self.df, do_it)

    def _keep_last(self):
        if not self._need_df(): return
        def do_it():
            self._save_state()
            before = len(self.df)
            self.df = self.df.drop_duplicates(keep="last")
            self._refresh()
            self._push_to_launcher()
            self._log(f"Kept last — removed {before - len(self.df)} rows.")
            self._set_status(f"✔  Kept last.", SUCCESS)
        self._confirm_preview("Keep Last Duplicate", self.df, do_it)

    def _mark_dups(self):
        if not self._need_df(): return
        self._save_state()
        self.df["is_duplicate"] = self.df.duplicated()
        self._refresh()
        self._push_to_launcher()
        self._log("Marked duplicates — added 'is_duplicate' column.")
        self._set_status("✔  Added 'is_duplicate' column.", SUCCESS)

    def _remove_by_col(self):
        if not self._need_df(): return
        col = self.col_var.get()
        if not col: return
        def do_it():
            self._save_state()
            before = len(self.df)
            self.df = self.df.drop_duplicates(subset=[col])
            self._refresh()
            self._push_to_launcher()
            self._log(f"Removed {before - len(self.df)} rows by '{col}'.")
            self._set_status(f"✔  Removed {before - len(self.df)} rows.", SUCCESS)
        self._confirm_preview(f"Remove Duplicates by '{col}'", self.df, do_it)

    def _refresh(self):
        c = T.get_colors()
        self._build_stat_cards()
        if self.df is None: return
        _apply_treeview_style("Dup")
        self.tree.delete(*self.tree.get_children())
        cols = list(self.df.columns)
        self.tree["columns"] = cols
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, minwidth=60)
        for i, row in self.df.head(200).iterrows():
            is_dup = self.df.duplicated().iloc[i] if i < len(self.df) else False
            tag = "dup" if is_dup else ("alt" if i % 2 else "norm")
            self.tree.insert("", "end", values=list(row), tags=(tag,))
        self.tree.tag_configure("dup",  background="#3B1219", foreground=DANGER)
        self.tree.tag_configure("alt",  background=c["TABLE_ALT"])
        self.tree.tag_configure("norm", background=c["BG_DARK"])
        r, cc = self.df.shape
        self.row_info.set(f"{r} rows × {cc} columns  |  {self.df.duplicated().sum()} duplicates in red")

    def _show_popup(self, title, content):
        c = T.get_colors()
        win = tk.Toplevel(self); win.title(title)
        win.configure(bg=c["BG_DARK"]); center_window(win, 620, 380)
        tk.Label(win, text=title, font=FONT_HEADING, fg=DANGER, bg=c["BG_DARK"]).pack(pady=(14, 6))
        txt = tk.Text(win, bg=c["BG_CARD"], fg=c["TEXT_PRIMARY"], font=FONT_MONO,
                      relief="flat", padx=10, pady=10)
        txt.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        txt.insert("1.0", content if content.strip() else "No duplicates found.")
        txt.config(state="disabled")

    def apply_theme(self):
        c = T.get_colors()
        self.configure(bg=c["BG_DARK"])
        self.hdr.config(bg=c["BG_CARD"])
        self.hdr_title.config(bg=c["BG_CARD"])
        self.hdr_sub.config(bg=c["BG_CARD"], fg=c["TEXT_MUTED"])
        self.stats_frame.config(bg=c["BG_DARK"])
        self._build_stat_cards()
        self.body.config(bg=c["BG_DARK"])
        self.left_outer.config(bg=c["BG_CARD"])
        self.right_frame.config(bg=c["BG_CARD"])
        self.preview_lbl.config(bg=c["BG_CARD"])
        self.divider.config(bg=T.BORDER)
        self._tree_frame.config(bg=c["BG_CARD"])
        self.info_lbl.config(bg=c["BG_CARD"], fg=c["TEXT_MUTED"])
        self.status_lbl.config(bg=c["BG_DARK"], fg=c["TEXT_MUTED"])
        if self.df is not None: self._refresh()


if __name__ == "__main__":
    root = tk.Tk(); root.withdraw()
    DuplicatesApp().mainloop()
