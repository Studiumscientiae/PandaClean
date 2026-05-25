# gui_formatting.py — Formatting Handler Tool

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


class FormattingApp(ToolWindow):

    def __init__(self, launcher=None):
        super().__init__(launcher=launcher, title="Formatting Handler", width=980, height=720)

    def _build_ui(self):
        c = T.get_colors()
        self.hdr = tk.Frame(self, bg=c["BG_CARD"], pady=14)
        self.hdr.pack(fill="x")
        self.hdr_title = tk.Label(self.hdr, text="⬡  FORMATTING HANDLER", font=FONT_TITLE,
                                   fg=ACCENT, bg=c["BG_CARD"])
        self.hdr_title.pack(side="left", padx=PAD)
        self.hdr_sub = tk.Label(self.hdr,
                                 text="Case · Trim · Replace  |  Ctrl+Z Undo  |  Ctrl+Y Redo",
                                 font=FONT_SMALL, fg=c["TEXT_MUTED"], bg=c["BG_CARD"])
        self.hdr_sub.pack(side="left", padx=6)

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
                          padx=10, pady=7, width=22, bd=0)
            b.bind("<Enter>", lambda e: b.config(bg=ACCENT_DIM if color==ACCENT else c["BG_HOVER"]))
            b.bind("<Leave>", lambda e: b.config(bg=color))
            return b

        lbl("TARGET COLUMN"); div()
        self.col_var = tk.StringVar()
        self.col_combo = ttk.Combobox(parent, textvariable=self.col_var,
                                       state="readonly", font=FONT_BODY)
        self.col_combo.pack(fill="x", pady=(0, 12))

        lbl("CASE CONVERSION"); div()
        btn("Aa  Title Case", self._to_title).pack(fill="x", pady=3)
        btn("aa  Lowercase",  self._to_lower, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)
        btn("AA  Uppercase",  self._to_upper, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)
        sep()
        lbl("CLEANING"); div()
        btn("✂  Remove Special Chars", self._rm_special,  WARN, c["BG_DARK"]).pack(fill="x", pady=3)
        btn("⎵  Remove Extra Spaces",  self._rm_extra_sp, WARN, c["BG_DARK"]).pack(fill="x", pady=3)
        sep()
        lbl("REPLACE VALUE"); div()
        tk.Label(parent, text="Old value:", font=FONT_SMALL,
                 fg=c["TEXT_MUTED"], bg=c["BG_CARD"]).pack(anchor="w")
        self.old_val = tk.Entry(parent, bg=c["BG_DARK"], fg=c["TEXT_PRIMARY"],
                                 insertbackground=ACCENT, font=FONT_BODY, relief="flat", bd=4)
        self.old_val.pack(fill="x", pady=(2, 6))
        tk.Label(parent, text="New value:", font=FONT_SMALL,
                 fg=c["TEXT_MUTED"], bg=c["BG_CARD"]).pack(anchor="w")
        self.new_val = tk.Entry(parent, bg=c["BG_DARK"], fg=c["TEXT_PRIMARY"],
                                 insertbackground=ACCENT, font=FONT_BODY, relief="flat", bd=4)
        self.new_val.pack(fill="x", pady=(2, 8))
        btn("🔁  Replace", self._replace_val).pack(fill="x", pady=3)
        sep()
        lbl("COLUMN NAMES"); div()
        btn("🏷  Format All Column Names", self._fmt_col_names,
            c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)
        sep()
        lbl("UNDO / REDO"); div()
        btn("↩  Undo  (Ctrl+Z)", self._undo, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)
        btn("↪  Redo  (Ctrl+Y)", self._redo, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)
        sep()
        lbl("SAVE & LOG"); div()
        btn("💾  Save CSV",        self._save_csv,   SUCCESS,       c["BG_DARK"]).pack(fill="x", pady=3)
        btn("📋  Export Action Log", self._export_log, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=3)

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

        _apply_treeview_style("Fmt")
        self.tree = ttk.Treeview(frame, style="Fmt.Treeview",
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
        self.col_combo["values"] = list(self.df.columns)
        if len(self.df.columns): self.col_var.set(self.df.columns[0])
        self._refresh()
        name = os.path.basename(path) if path else "shared file"
        self._set_status(f"✔  Loaded: {name}")

    def _get_col(self):
        if not self._need_df(): return None
        col = self.col_var.get()
        if not col:
            messagebox.showwarning("No Column", "Select a column first."); return None
        return col

    def _to_title(self):
        col = self._get_col()
        if col is None: return
        self._save_state()
        self.df[col] = self.df[col].astype(str).str.title()
        self._refresh(); self._push_to_launcher(); self._log(f"'{col}' → Title Case.")
        self._set_status(f"✔  '{col}' → Title Case", SUCCESS)

    def _to_lower(self):
        col = self._get_col()
        if col is None: return
        self._save_state()
        self.df[col] = self.df[col].astype(str).str.lower()
        self._refresh(); self._push_to_launcher(); self._log(f"'{col}' → lowercase.")
        self._set_status(f"✔  '{col}' → lowercase", SUCCESS)

    def _to_upper(self):
        col = self._get_col()
        if col is None: return
        self._save_state()
        self.df[col] = self.df[col].astype(str).str.upper()
        self._refresh(); self._push_to_launcher(); self._log(f"'{col}' → UPPERCASE.")
        self._set_status(f"✔  '{col}' → UPPERCASE", SUCCESS)

    def _rm_special(self):
        col = self._get_col()
        if col is None: return
        self._save_state()
        self.df[col] = self.df[col].astype(str).str.replace(r"[^a-zA-Z0-9 ]", "", regex=True)
        self._refresh(); self._push_to_launcher(); self._log(f"Removed special chars from '{col}'.")
        self._set_status(f"✔  Special chars removed from '{col}'", SUCCESS)

    def _rm_extra_sp(self):
        col = self._get_col()
        if col is None: return
        self._save_state()
        self.df[col] = self.df[col].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
        self._refresh(); self._push_to_launcher(); self._log(f"Removed extra spaces from '{col}'.")
        self._set_status(f"✔  Extra spaces removed from '{col}'", SUCCESS)

    def _replace_val(self):
        col = self._get_col()
        if col is None: return
        old = self.old_val.get(); new = self.new_val.get()
        if not old:
            messagebox.showwarning("Input", "Enter an old value."); return
        def do_it():
            self._save_state()
            self.df[col] = self.df[col].replace(old, new)
            self._refresh()
            self._push_to_launcher()
            self._log(f"Replaced '{old}' → '{new}' in '{col}'.")
            self._set_status(f"✔  Replaced '{old}' → '{new}' in '{col}'", SUCCESS)
        self._confirm_preview(f"Replace '{old}' → '{new}' in '{col}'", self.df, do_it)

    def _fmt_col_names(self):
        if not self._need_df(): return
        def do_it():
            self._save_state()
            self.df.columns = (self.df.columns.str.strip().str.title()
                               .str.replace(" ", "_"))
            self.col_combo["values"] = list(self.df.columns)
            if len(self.df.columns): self.col_var.set(self.df.columns[0])
            self._refresh()
            self._push_to_launcher()
            self._log("Formatted all column names (Title_Case).")
            self._set_status("✔  Column names formatted.", SUCCESS)
        self._confirm_preview("Format All Column Names", self.df, do_it)

    def _refresh(self):
        if self.df is None: return
        c = T.get_colors()
        _apply_treeview_style("Fmt")
        self.tree.delete(*self.tree.get_children())
        cols = list(self.df.columns)
        self.tree["columns"] = cols
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, minwidth=60)
        for i, row in self.df.head(200).iterrows():
            tag = "alt" if i % 2 else "norm"
            self.tree.insert("", "end", values=list(row), tags=(tag,))
        self.tree.tag_configure("alt",  background=c["TABLE_ALT"])
        self.tree.tag_configure("norm", background=c["BG_DARK"])
        r, cc = self.df.shape
        self.info_var.set(f"{r} rows × {cc} columns")

    def apply_theme(self):
        c = T.get_colors()
        self.configure(bg=c["BG_DARK"])
        self.hdr.config(bg=c["BG_CARD"])
        self.hdr_title.config(bg=c["BG_CARD"])
        self.hdr_sub.config(bg=c["BG_CARD"], fg=c["TEXT_MUTED"])
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
    FormattingApp().mainloop()
