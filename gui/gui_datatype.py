# gui_datatype.py — Datatype Converter Tool

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


class DatatypeApp(ToolWindow):

    def __init__(self, launcher=None):
        super().__init__(launcher=launcher, title="Datatype Converter", width=900, height=700)

    def _build_ui(self):
        c = T.get_colors()
        self.hdr = tk.Frame(self, bg=c["BG_CARD"], pady=14)
        self.hdr.pack(fill="x")
        self.hdr_title = tk.Label(self.hdr, text="⬡  DATATYPE CONVERTER", font=FONT_TITLE,
                                   fg=ACCENT, bg=c["BG_CARD"])
        self.hdr_title.pack(side="left", padx=PAD)
        self.hdr_sub = tk.Label(self.hdr,
                                 text="Cast · Validate · Clean  |  Ctrl+Z Undo  |  Ctrl+Y Redo",
                                 font=FONT_SMALL, fg=c["TEXT_MUTED"], bg=c["BG_CARD"])
        self.hdr_sub.pack(side="left", padx=6)

        self.body = tk.Frame(self, bg=c["BG_DARK"])
        self.body.pack(fill="both", expand=True, padx=PAD, pady=(0, PAD))

        self.left_outer = tk.Frame(self.body, bg=c["BG_CARD"], width=280)
        self.left_outer.pack(side="left", fill="y", padx=(0, 10))
        self.left_outer.pack_propagate(False)
        left = _make_scrollable_left(self.left_outer)

        self.right_frame = tk.Frame(self.body, bg=c["BG_CARD"], padx=14, pady=14)
        self.right_frame.pack(side="left", fill="both", expand=True)

        self._build_controls(left)
        self._build_preview(self.right_frame)

        self.status_var = tk.StringVar(value="Waiting for file from launcher…")
        self.status_lbl = tk.Label(self, textvariable=self.status_var, font=FONT_SMALL,
                                    fg=c["TEXT_MUTED"], bg=c["BG_DARK"], anchor="w")
        self.status_lbl.pack(fill="x", padx=PAD, pady=(0, 6))

    def _build_controls(self, parent):
        c = T.get_colors()

        def sep(): tk.Frame(parent, bg=T.BORDER, height=1).pack(fill="x", pady=12)
        def lbl(t): tk.Label(parent, text=t, font=FONT_HEADING,
                              fg=ACCENT, bg=c["BG_CARD"]).pack(anchor="w")
        def div(): tk.Frame(parent, bg=T.BORDER, height=1).pack(fill="x", pady=(4, 10))

        def btn(text, cmd, color=ACCENT, fg_=None, width=22):
            fg_ = fg_ or c["BG_DARK"]
            b = tk.Button(parent, text=text, command=cmd, bg=color, fg=fg_,
                          activebackground=ACCENT_DIM, activeforeground=c["BG_DARK"],
                          font=FONT_BODY, relief="flat", cursor="hand2",
                          padx=10, pady=7, width=width, bd=0)
            b.bind("<Enter>", lambda e: b.config(bg=ACCENT_DIM if color==ACCENT else c["BG_HOVER"]))
            b.bind("<Leave>", lambda e: b.config(bg=color))
            return b

        lbl("CONVERT COLUMN"); div()
        tk.Label(parent, text="Select Column:", font=FONT_BODY,
                 fg=c["TEXT_MUTED"], bg=c["BG_CARD"]).pack(anchor="w")
        self.col_var = tk.StringVar()
        self.col_combo = ttk.Combobox(parent, textvariable=self.col_var,
                                       state="readonly", font=FONT_BODY)
        self.col_combo.pack(fill="x", pady=(4, 12))

        tk.Label(parent, text="Target Datatype:", font=FONT_BODY,
                 fg=c["TEXT_MUTED"], bg=c["BG_CARD"]).pack(anchor="w")
        self.dtype_var = tk.StringVar(value="Integer")
        for dt in ["Integer", "Float", "String", "Datetime", "Boolean"]:
            tk.Radiobutton(parent, text=dt, variable=self.dtype_var, value=dt,
                           bg=c["BG_CARD"], fg=c["TEXT_PRIMARY"],
                           selectcolor=c["BG_DARK"],
                           activebackground=c["BG_CARD"], activeforeground=ACCENT,
                           font=FONT_BODY, cursor="hand2").pack(anchor="w", pady=2)

        btn("⚡  Convert Column", self._convert_column).pack(fill="x", pady=(14, 6))
        sep()
        lbl("UTILITIES"); div()
        btn("🔍  Check All Dtypes",      self._check_dtypes,    WARN,          c["BG_DARK"]).pack(fill="x", pady=4)
        btn("💱  Remove Currency",        self._remove_currency, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=4)
        btn("⚠  Find Invalid Numerics",  self._find_invalid,    DANGER,        "#fff").pack(fill="x", pady=4)
        sep()
        lbl("UNDO / REDO"); div()
        btn("↩  Undo  (Ctrl+Z)", self._undo, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=4)
        btn("↪  Redo  (Ctrl+Y)", self._redo, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=4)
        sep()
        lbl("ACTION LOG"); div()
        btn("📋  Export Log", self._export_log, c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=4)

    def _build_preview(self, parent):
        c = T.get_colors()
        self.preview_lbl = tk.Label(parent, text="DATAFRAME PREVIEW", font=FONT_HEADING,
                                     fg=ACCENT, bg=c["BG_CARD"])
        self.preview_lbl.pack(anchor="w")
        self.divider = tk.Frame(parent, bg=T.BORDER, height=1)
        self.divider.pack(fill="x", pady=(4, 10))

        frame = tk.Frame(parent, bg=c["BG_CARD"])
        frame.pack(fill="both", expand=True)
        self._tree_frame = frame

        _apply_treeview_style("DT")
        self.tree = ttk.Treeview(frame, style="DT.Treeview",
                                  show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1); frame.columnconfigure(0, weight=1)

        self.dtype_display = tk.Text(parent, height=4, bg=c["BG_DARK"], fg=ACCENT,
                                      font=FONT_MONO, relief="flat", padx=8, pady=6)
        self.dtype_display.pack(fill="x", pady=(10, 0))
        self.dtype_display.insert("1.0", "Column dtypes will appear here after loading a file.")
        self.dtype_display.config(state="disabled")

    # ── Actions ───────────────────────────────────────────────────────────

    def _post_load(self, path):
        c = T.get_colors()
        self.col_combo["values"] = list(self.df.columns)
        if len(self.df.columns): self.col_var.set(self.df.columns[0])
        self._refresh_table(); self._update_dtype_display()
        name = os.path.basename(path) if path else "shared file"
        self._set_status(f"✔  Loaded: {name}")

    def _convert_column(self):
        if not self._need_df(): return
        col = self.col_var.get(); dtype = self.dtype_var.get()
        if not col: return
        def do_it():
            self._save_state()
            try:
                if dtype == "Integer":
                    self.df[col] = pd.to_numeric(self.df[col], errors="coerce").astype("Int64")
                elif dtype == "Float":
                    self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
                elif dtype == "String":
                    self.df[col] = self.df[col].astype(str)
                elif dtype == "Datetime":
                    self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
                elif dtype == "Boolean":
                    self.df[col] = self.df[col].astype(bool)
                self._refresh_table(); self._update_dtype_display()
                self._push_to_launcher()
                self._log(f"Converted '{col}' to {dtype}.")
                self._set_status(f"✔  '{col}' → {dtype}", SUCCESS)
            except Exception as e:
                messagebox.showerror("Conversion Error", str(e))
        self._confirm_preview(f"Convert '{col}' to {dtype}", self.df, do_it)

    def _check_dtypes(self):
        if not self._need_df(): return
        self._update_dtype_display()
        self._set_status("Datatypes refreshed.")

    def _remove_currency(self):
        if not self._need_df(): return
        col = self.col_var.get()
        if not col: return
        self._save_state()
        try:
            self.df[col] = self.df[col].astype(str).str.replace(r"[^0-9.]", "", regex=True)
            self._refresh_table()
            self._push_to_launcher()
            self._log(f"Removed currency symbols from '{col}'.")
            self._set_status(f"✔  Currency removed from '{col}'", SUCCESS)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _find_invalid(self):
        if not self._need_df(): return
        col = self.col_var.get()
        if not col: return
        c = T.get_colors()
        invalid = self.df[pd.to_numeric(self.df[col], errors="coerce").isna()]
        win = tk.Toplevel(self); win.title(f"Invalid Numerics in '{col}'")
        win.configure(bg=c["BG_DARK"]); center_window(win, 600, 340)
        tk.Label(win, text=f"Invalid rows in '{col}': {len(invalid)}",
                 font=FONT_HEADING, fg=DANGER, bg=c["BG_DARK"]).pack(pady=(14, 6))
        txt = tk.Text(win, bg=c["BG_CARD"], fg=c["TEXT_PRIMARY"], font=FONT_MONO,
                      relief="flat", padx=10, pady=10)
        txt.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        txt.insert("1.0", invalid.to_string() if not invalid.empty else "No invalid rows found.")
        txt.config(state="disabled")
        self._log(f"Checked invalid numerics in '{col}': {len(invalid)} found.")

    def _refresh(self):
        self._refresh_table(); self._update_dtype_display()

    def _refresh_table(self):
        if self.df is None: return
        c = T.get_colors()
        _apply_treeview_style("DT")
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

    def _update_dtype_display(self):
        if self.df is None: return
        text = "\n".join(f"  {col:<25} {str(t)}" for col, t in self.df.dtypes.items())
        self.dtype_display.config(state="normal")
        self.dtype_display.delete("1.0", "end")
        self.dtype_display.insert("1.0", text)
        self.dtype_display.config(state="disabled")

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
        self.dtype_display.config(bg=c["BG_DARK"])
        self.status_lbl.config(bg=c["BG_DARK"], fg=c["TEXT_MUTED"])
        if self.df is not None: self._refresh()


if __name__ == "__main__":
    root = tk.Tk(); root.withdraw()
    DatatypeApp().mainloop()
