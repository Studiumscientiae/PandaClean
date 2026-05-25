# gui_missing.py — Missing Values Handler Tool

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


class MissingApp(ToolWindow):

    def __init__(self, launcher=None):
        super().__init__(launcher=launcher, title="Missing Values Handler", width=1000, height=720)

    def _build_ui(self):
        c = T.get_colors()
        self.hdr = tk.Frame(self, bg=c["BG_CARD"], pady=14)
        self.hdr.pack(fill="x")
        self.hdr_title = tk.Label(self.hdr, text="⬡  MISSING VALUES HANDLER", font=FONT_TITLE,
                                   fg=ACCENT, bg=c["BG_CARD"])
        self.hdr_title.pack(side="left", padx=PAD)
        self.hdr_sub = tk.Label(self.hdr,
                                 text="Detect · Drop · Fill · Impute  |  Ctrl+Z Undo  |  Ctrl+Y Redo",
                                 font=FONT_SMALL, fg=c["TEXT_MUTED"], bg=c["BG_CARD"])
        self.hdr_sub.pack(side="left", padx=6)

        self.stat_frame = tk.Frame(self, bg=c["BG_DARK"], pady=8)
        self.stat_frame.pack(fill="x", padx=PAD)
        self._build_stats()

        self.body = tk.Frame(self, bg=c["BG_DARK"])
        self.body.pack(fill="both", expand=True, padx=PAD, pady=(0, PAD))

        self.left_outer = tk.Frame(self.body, bg=c["BG_CARD"], width=300)
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

    def _build_stats(self):
        c = T.get_colors()
        for w in self.stat_frame.winfo_children(): w.destroy()
        total   = len(self.df) if self.df is not None else 0
        missing = int(self.df.isnull().sum().sum()) if self.df is not None else 0
        cols_m  = int((self.df.isnull().sum() > 0).sum()) if self.df is not None else 0
        for label, val, color in [
            ("TOTAL ROWS",      str(total),   ACCENT),
            ("MISSING CELLS",   str(missing), DANGER),
            ("COLS W/ MISSING", str(cols_m),  WARN),
        ]:
            card = tk.Frame(self.stat_frame, bg=c["BG_CARD"], padx=20, pady=10)
            card.pack(side="left", padx=(0, 10))
            tk.Label(card, text=str(val), font=("Consolas", 20, "bold"),
                     fg=color, bg=c["BG_CARD"]).pack()
            tk.Label(card, text=label, font=FONT_SMALL,
                     fg=c["TEXT_MUTED"], bg=c["BG_CARD"]).pack()

    def _build_left(self, parent):
        c = T.get_colors()

        def sep(): tk.Frame(parent, bg=T.BORDER, height=1).pack(fill="x", pady=10)
        def lbl(t): tk.Label(parent, text=t, font=FONT_HEADING,
                              fg=ACCENT, bg=c["BG_CARD"]).pack(anchor="w")
        def div(): tk.Frame(parent, bg=T.BORDER, height=1).pack(fill="x", pady=(4, 8))

        def btn(text, cmd, color=ACCENT, fg_=None):
            fg_ = fg_ or c["BG_DARK"]
            b = tk.Button(parent, text=text, command=cmd, bg=color, fg=fg_,
                          activebackground=ACCENT_DIM, activeforeground=c["BG_DARK"],
                          font=FONT_BODY, relief="flat", cursor="hand2",
                          padx=10, pady=7, width=24, bd=0)
            b.bind("<Enter>", lambda e: b.config(bg=ACCENT_DIM if color==ACCENT else c["BG_HOVER"]))
            b.bind("<Leave>", lambda e: b.config(bg=color))
            return b

        lbl("TARGET COLUMN"); div()
        tk.Label(parent, text="Apply fill to specific column:", font=FONT_SMALL,
                 fg=c["TEXT_MUTED"], bg=c["BG_CARD"]).pack(anchor="w")
        self.miss_col_var = tk.StringVar(value="— All Columns —")
        self.miss_col_combo = ttk.Combobox(parent, textvariable=self.miss_col_var,
                                            state="readonly", font=FONT_BODY)
        self.miss_col_combo.pack(fill="x", pady=(2, 6))
        sep()
        lbl("INSPECT"); div()
        btn("🔍  Check Missing Values", self._check_missing, WARN, c["BG_DARK"]).pack(fill="x", pady=3)
        sep()
        lbl("DROP"); div()
        btn("🗑  Drop Rows w/ Missing", self._drop_rows, DANGER, "#fff").pack(fill="x", pady=3)
        btn("🗑  Drop Empty Columns",   self._drop_cols, DANGER, "#fff").pack(fill="x", pady=3)
        sep()
        lbl("FILL"); div()
        tk.Label(parent, text="Custom fill value:", font=FONT_SMALL,
                 fg=c["TEXT_MUTED"], bg=c["BG_CARD"]).pack(anchor="w")
        self.fill_val = tk.Entry(parent, bg=c["BG_DARK"], fg=c["TEXT_PRIMARY"],
                                  insertbackground=ACCENT, font=FONT_BODY, relief="flat", bd=4)
        self.fill_val.insert(0, "unknown")
        self.fill_val.pack(fill="x", pady=(2, 6))
        btn("✏  Fill w/ Custom Value", self._fill_custom).pack(fill="x", pady=3)
        sep()
        lbl("IMPUTE NUMERIC"); div()
        btn("〜  Fill w/ Mean",   self._fill_mean,   c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)
        btn("〜  Fill w/ Median", self._fill_median, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)
        btn("〜  Fill w/ Mode",   self._fill_mode,   c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)
        sep()
        lbl("UNDO / REDO"); div()
        btn("↩  Undo  (Ctrl+Z)", self._undo, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)
        btn("↪  Redo  (Ctrl+Y)", self._redo, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)
        sep()
        lbl("SAVE & LOG"); div()
        btn("💾  Save Result CSV",    self._save_csv,   SUCCESS,       c["BG_DARK"]).pack(fill="x", pady=3)
        btn("📋  Export Action Log",   self._export_log, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)

    def _build_right(self, parent):
        c = T.get_colors()
        self.preview_lbl = tk.Label(parent, text="MISSING VALUE HEATMAP + PREVIEW",
                                     font=FONT_HEADING, fg=ACCENT, bg=c["BG_CARD"])
        self.preview_lbl.pack(anchor="w")
        self.divider = tk.Frame(parent, bg=T.BORDER, height=1)
        self.divider.pack(fill="x", pady=(4, 10))

        self.heatmap_frame = tk.Frame(parent, bg=c["BG_CARD"], height=36)
        self.heatmap_frame.pack(fill="x", pady=(0, 8))
        self.heatmap_frame.pack_propagate(False)

        frame = tk.Frame(parent, bg=c["BG_CARD"])
        frame.pack(fill="both", expand=True)
        self._tree_frame = frame

        _apply_treeview_style("Miss")
        self.tree = ttk.Treeview(frame, style="Miss.Treeview",
                                  show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1); frame.columnconfigure(0, weight=1)

        self.info_var = tk.StringVar(value="No file loaded.")
        self.info_lbl = tk.Label(parent, textvariable=self.info_var, font=FONT_SMALL,
                                  fg=c["TEXT_MUTED"], bg=c["BG_CARD"], anchor="w")
        self.info_lbl.pack(anchor="w", pady=(8, 0))

    # ── Actions ───────────────────────────────────────────────────────────

    def _post_load(self, path):
        if self.df is not None:
            cols = ["— All Columns —"] + list(self.df.columns)
            self.miss_col_combo["values"] = cols
            self.miss_col_var.set("— All Columns —")
        self._refresh()
        name = os.path.basename(path) if path else "shared file"
        self._set_status(f"✔  Loaded: {name}")

    def _get_target_col(self):
        val = self.miss_col_var.get()
        return None if val == "— All Columns —" else val

    def _check_missing(self):
        if not self._need_df(): return
        c = T.get_colors()
        summary = self.df.isnull().sum()
        summary = summary[summary > 0]
        text = summary.to_string() if not summary.empty else "✔  No missing values found!"
        win = tk.Toplevel(self); win.title("Missing Value Summary")
        win.configure(bg=c["BG_DARK"]); center_window(win, 460, 340)
        tk.Label(win, text="MISSING PER COLUMN", font=FONT_HEADING,
                 fg=WARN, bg=c["BG_DARK"]).pack(pady=(14, 6))
        txt = tk.Text(win, bg=c["BG_CARD"], fg=c["TEXT_PRIMARY"], font=FONT_MONO,
                      relief="flat", padx=10, pady=10)
        txt.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        txt.insert("1.0", text); txt.config(state="disabled")

    def _drop_rows(self):
        if not self._need_df(): return
        def do_it():
            self._save_state()
            before = len(self.df)
            self.df = self.df.dropna()
            self._refresh()
            self._push_to_launcher()
            self._log(f"Dropped {before - len(self.df)} rows with missing values.")
            self._set_status(f"✔  Dropped {before - len(self.df)} rows.", SUCCESS)
        self._confirm_preview("Drop Rows with Missing Values", self.df, do_it)

    def _drop_cols(self):
        if not self._need_df(): return
        def do_it():
            self._save_state()
            before = len(self.df.columns)
            self.df = self.df.dropna(axis=1, how="all")
            self._refresh()
            self._push_to_launcher()
            self._log(f"Dropped {before - len(self.df.columns)} empty columns.")
            self._set_status(f"✔  Dropped {before - len(self.df.columns)} columns.", SUCCESS)
        self._confirm_preview("Drop Empty Columns", self.df, do_it)

    def _fill_custom(self):
        if not self._need_df(): return
        self._save_state()
        val = self.fill_val.get()
        col = self._get_target_col()
        if col:
            self.df[col] = self.df[col].fillna(val)
            self._log(f"Filled missing in '{col}' with '{val}'.")
        else:
            self.df = self.df.fillna(val)
            self._log(f"Filled all missing values with '{val}'.")
        self._refresh()
        self._push_to_launcher()
        self._set_status(f"✔  Filled missing with '{val}'.", SUCCESS)

    def _fill_mean(self):
        if not self._need_df(): return
        self._save_state()
        col = self._get_target_col()
        cols = [col] if col else list(self.df.select_dtypes(include=["number"]).columns)
        for c_ in cols: self.df[c_] = self.df[c_].fillna(self.df[c_].mean())
        self._refresh(); self._push_to_launcher(); self._log("Filled missing with mean."); self._set_status("✔  Filled with mean.", SUCCESS)

    def _fill_median(self):
        if not self._need_df(): return
        self._save_state()
        col = self._get_target_col()
        cols = [col] if col else list(self.df.select_dtypes(include=["number"]).columns)
        for c_ in cols: self.df[c_] = self.df[c_].fillna(self.df[c_].median())
        self._refresh(); self._push_to_launcher(); self._log("Filled missing with median."); self._set_status("✔  Filled with median.", SUCCESS)

    def _fill_mode(self):
        if not self._need_df(): return
        self._save_state()
        col = self._get_target_col()
        cols = [col] if col else list(self.df.select_dtypes(include=["number"]).columns)
        for c_ in cols:
            mode = self.df[c_].mode()
            if not mode.empty: self.df[c_] = self.df[c_].fillna(mode[0])
        self._refresh(); self._push_to_launcher(); self._log("Filled missing with mode."); self._set_status("✔  Filled with mode.", SUCCESS)

    def _refresh(self):
        c = T.get_colors()
        self._build_stats()
        self._build_heatmap()
        if self.df is None: return
        _apply_treeview_style("Miss")
        self.tree.delete(*self.tree.get_children())
        cols = list(self.df.columns)
        self.tree["columns"] = cols
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, minwidth=60)
        missing_rows = self.df[self.df.isnull().any(axis=1)].index
        for i, row in self.df.head(200).iterrows():
            tag = "missing" if i in missing_rows else ("alt" if i % 2 else "norm")
            self.tree.insert("", "end", values=list(row), tags=(tag,))
        self.tree.tag_configure("missing", background="#2A1A10", foreground=WARN)
        self.tree.tag_configure("alt",     background=c["TABLE_ALT"])
        self.tree.tag_configure("norm",    background=c["BG_DARK"])
        r, cc = self.df.shape
        missing = int(self.df.isnull().sum().sum())
        self.info_var.set(f"{r} rows × {cc} columns  |  {missing} missing cells highlighted in amber")

    def _build_heatmap(self):
        c = T.get_colors()
        for w in self.heatmap_frame.winfo_children(): w.destroy()
        if self.df is None: return
        miss = self.df.isnull().sum()
        total = max(len(self.df), 1)
        tk.Label(self.heatmap_frame, text="Missing %: ",
                 font=FONT_SMALL, fg=c["TEXT_MUTED"], bg=c["BG_CARD"]).pack(side="left")
        for col in self.df.columns:
            pct = miss[col] / total
            color = DANGER if pct > 0.5 else WARN if pct > 0.1 else SUCCESS if pct == 0 else "#F59E0B"
            lbl = tk.Label(self.heatmap_frame, text=f" {col[:8]} ",
                           font=FONT_SMALL, fg=c["BG_DARK"], bg=color,
                           relief="flat", padx=3, pady=2, cursor="question_arrow")
            lbl.pack(side="left", padx=2, pady=4)

    def apply_theme(self):
        c = T.get_colors()
        self.configure(bg=c["BG_DARK"])
        self.hdr.config(bg=c["BG_CARD"])
        self.hdr_title.config(bg=c["BG_CARD"])
        self.hdr_sub.config(bg=c["BG_CARD"], fg=c["TEXT_MUTED"])
        self.stat_frame.config(bg=c["BG_DARK"])
        self.body.config(bg=c["BG_DARK"])
        self.left_outer.config(bg=c["BG_CARD"])
        self.right_frame.config(bg=c["BG_CARD"])
        self.preview_lbl.config(bg=c["BG_CARD"])
        self.divider.config(bg=T.BORDER)
        self.heatmap_frame.config(bg=c["BG_CARD"])
        self._tree_frame.config(bg=c["BG_CARD"])
        self.info_lbl.config(bg=c["BG_CARD"], fg=c["TEXT_MUTED"])
        self.status_lbl.config(bg=c["BG_DARK"], fg=c["TEXT_MUTED"])
        self._refresh()


if __name__ == "__main__":
    root = tk.Tk(); root.withdraw()
    MissingApp().mainloop()
