# gui_file_handler.py — File Handler Tool

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
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


def _make_scrollable_left(parent):
    c = T.get_colors()
    canvas = tk.Canvas(parent, bg=c["BG_CARD"], highlightthickness=0, width=260, bd=0)
    vsb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    inner = tk.Frame(canvas, bg=c["BG_CARD"], padx=16, pady=16)
    win_id = canvas.create_window((0, 0), window=inner, anchor="nw")
    def _on_configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())
    inner.bind("<Configure>", _on_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    def _mw(e): canvas.yview_scroll(int(-1*(e.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _mw)
    return inner


class FileHandlerApp(ToolWindow):

    def __init__(self, launcher=None):
        super().__init__(launcher=launcher, title="File Handler", width=900, height=680)

    # ── UI ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        c = T.get_colors()
        self.hdr = tk.Frame(self, bg=c["BG_CARD"], pady=14)
        self.hdr.pack(fill="x")
        self.hdr_title = tk.Label(self.hdr, text="⬡  FILE HANDLER", font=FONT_TITLE,
                                   fg=ACCENT, bg=c["BG_CARD"])
        self.hdr_title.pack(side="left", padx=PAD)
        self.hdr_sub = tk.Label(self.hdr, text="Inspect · Save — file loaded from main launcher",
                                 font=FONT_SMALL, fg=c["TEXT_MUTED"], bg=c["BG_CARD"])
        self.hdr_sub.pack(side="left", padx=6)

        self.body = tk.Frame(self, bg=c["BG_DARK"])
        self.body.pack(fill="both", expand=True, padx=PAD, pady=PAD)

        self.left_outer = tk.Frame(self.body, bg=c["BG_CARD"], width=260)
        self.left_outer.pack(side="left", fill="y", padx=(0, 10))
        self.left_outer.pack_propagate(False)
        left = _make_scrollable_left(self.left_outer)

        self.right_frame = tk.Frame(self.body, bg=c["BG_CARD"], padx=16, pady=16)
        self.right_frame.pack(side="left", fill="both", expand=True)

        self._build_left(left)
        self._build_right(self.right_frame)

        self.status_var = tk.StringVar(value="Waiting for file from launcher…")
        self.status_lbl = tk.Label(self, textvariable=self.status_var,
                                    font=FONT_SMALL, fg=c["TEXT_MUTED"],
                                    bg=c["BG_DARK"], anchor="w")
        self.status_lbl.pack(fill="x", padx=PAD, pady=(0, 8))

    def _build_left(self, parent):
        c = T.get_colors()

        def sec(title):
            f = tk.Frame(parent, bg=c["BG_CARD"], bd=0)
            tk.Label(f, text=title, font=FONT_HEADING, fg=ACCENT,
                     bg=c["BG_CARD"]).pack(anchor="w", pady=(0, 6))
            tk.Frame(f, bg=T.BORDER, height=1).pack(fill="x", pady=(0, 10))
            return f

        def btn(parent, text, cmd, color=ACCENT, fg_=None):
            fg_ = fg_ or c["BG_DARK"]
            b = tk.Button(parent, text=text, command=cmd, bg=color, fg=fg_,
                          activebackground=ACCENT_DIM, activeforeground=c["BG_DARK"],
                          font=FONT_BODY, relief="flat", cursor="hand2",
                          padx=10, pady=7, width=22, bd=0)
            b.bind("<Enter>", lambda e: b.config(bg=ACCENT_DIM if color == ACCENT else c["BG_HOVER"]))
            b.bind("<Leave>", lambda e: b.config(bg=color))
            return b

        s1 = sec("SAVE FILE")
        s1.pack(fill="x", pady=(0, 16))
        btn(s1, "💾  Save as CSV",   self._save_csv,   SUCCESS).pack(fill="x", pady=4)
        btn(s1, "💾  Save as Excel", self._save_excel, SUCCESS).pack(fill="x", pady=4)

        s2 = sec("INSPECT")
        s2.pack(fill="x", pady=(0, 16))
        btn(s2, "🔍  Show File Info", self._show_info, WARN, c["BG_DARK"]).pack(fill="x", pady=4)

        s3 = sec("ACTION LOG")
        s3.pack(fill="x")
        btn(s3, "📋  Export Log", self._export_log,
            c["BG_HOVER"], c["TEXT_PRIMARY"]).pack(fill="x", pady=4)

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

        _apply_treeview_style("FH")
        self.tree = ttk.Treeview(frame, style="FH.Treeview",
                                  show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1); frame.columnconfigure(0, weight=1)

        self.info_var = tk.StringVar(value="Load a file from the main launcher.")
        self.info_lbl = tk.Label(parent, textvariable=self.info_var, font=FONT_SMALL,
                                  fg=c["TEXT_MUTED"], bg=c["BG_CARD"], justify="left")
        self.info_lbl.pack(anchor="w", pady=(8, 0))

    # ── receive_df override ───────────────────────────────────────────────

    def _post_load(self, path):
        self._refresh_table()
        name = os.path.basename(path) if path else "shared file"
        self._set_status(f"✔  Loaded: {name}", SUCCESS)

    # ── Actions ───────────────────────────────────────────────────────────

    def _show_info(self):
        if not self._need_df(): return
        c = T.get_colors()
        info = (f"Shape : {self.df.shape[0]} rows × {self.df.shape[1]} cols\n"
                f"Columns : {', '.join(self.df.columns.tolist())}\n\n"
                + self.df.dtypes.to_string())
        win = tk.Toplevel(self)
        win.title("File Info"); win.configure(bg=c["BG_DARK"])
        center_window(win, 520, 380)
        tk.Label(win, text="FILE INFORMATION", font=FONT_HEADING,
                 fg=ACCENT, bg=c["BG_DARK"]).pack(pady=(16, 6))
        txt = tk.Text(win, bg=c["BG_CARD"], fg=c["TEXT_PRIMARY"], font=FONT_MONO,
                      relief="flat", padx=12, pady=12)
        txt.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        txt.insert("1.0", info); txt.config(state="disabled")

    # ── Refresh ───────────────────────────────────────────────────────────

    def _refresh(self):
        self._refresh_table()

    def _refresh_table(self):
        if self.df is None: return
        c = T.get_colors()
        _apply_treeview_style("FH")
        self.tree.delete(*self.tree.get_children())
        cols = list(self.df.columns)
        self.tree["columns"] = cols
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=60)
        for i, row in self.df.head(200).iterrows():
            tag = "alt" if i % 2 else "norm"
            self.tree.insert("", "end", values=list(row), tags=(tag,))
        self.tree.tag_configure("alt",  background=c["TABLE_ALT"])
        self.tree.tag_configure("norm", background=c["BG_DARK"])
        r, cc = self.df.shape
        self.info_var.set(f"{r} rows × {cc} columns  |  showing first 200 rows")

    # ── Theme ─────────────────────────────────────────────────────────────

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
        if self.df is not None:
            self._refresh_table()


if __name__ == "__main__":
    root = tk.Tk(); root.withdraw()
    FileHandlerApp().mainloop()
