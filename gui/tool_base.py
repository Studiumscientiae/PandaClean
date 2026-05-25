# tool_base.py — Base class for all tool windows
# Handles: theme registration, receive_df() shared file injection,
#          dark/light-aware helper widgets

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime

import theme as T
from theme import *


def _apply_treeview_style(style_name):
    """Apply current theme colours to a named Treeview style."""
    c = T.get_colors()
    style = ttk.Style()
    style.theme_use("default")
    style.configure(f"{style_name}.Treeview",
                    background=c["BG_DARK"], fieldbackground=c["BG_DARK"],
                    foreground=c["TEXT_PRIMARY"], rowheight=26,
                    font=FONT_MONO, borderwidth=0)
    style.configure(f"{style_name}.Treeview.Heading",
                    background=c["BG_CARD"], foreground=ACCENT,
                    font=FONT_HEADING, relief="flat")
    style.map(f"{style_name}.Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", c["BG_DARK"])])


class ToolWindow(tk.Toplevel):
    """
    Base Toplevel for all tool windows.

    Subclasses must implement:
        _build_ui(self)           — build all widgets
        _refresh(self)            — repopulate table / stats from self.df
        _post_load(self, path)    — called after df is set (update combos, etc.)
        apply_theme(self)         — repaint every widget with current colours

    Optional overrides:
        _get_tree_style_name()    — return the ttk style name string used for Treeview
    """

    def __init__(self, launcher=None, title="Tool", width=960, height=700):
        super().__init__()
        self.launcher = launcher
        self.df          = None
        self.history     = []
        self.future      = []
        self.action_log  = []

        T.register_window(self)
        apply_base_style(self, title)
        center_window(self, width, height)
        self.resizable(True, True)

        self._build_ui()

        self.bind("<Control-z>", self._undo)
        self.bind("<Control-y>", self._redo)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── Shared file injection ─────────────────────────────────────────────

    def receive_df(self, df, path=None):
        """Called by the launcher to inject a fresh copy of the shared DataFrame."""
        self.df = df
        self.history.clear()
        self.future.clear()
        self._post_load(path or "shared file")

    def _push_to_launcher(self):
        """Push the current self.df back to the launcher's shared_df.
        Call this at the end of every operation that modifies self.df so
        all other open tools stay in sync automatically."""
        if self.launcher is not None and self.df is not None:
            self.launcher.push_df_from_tool(self.df)

    # ── Undo / Redo (default impl) ────────────────────────────────────────

    def _save_state(self):
        self.history.append(self.df.copy())
        if len(self.history) > 10:
            self.history.pop(0)
        self.future.clear()

    def _undo(self, event=None):
        if not self.history:
            self._set_status("Nothing to undo."); return
        self.future.append(self.df.copy())
        self.df = self.history.pop()
        self._refresh()
        self._push_to_launcher()
        self._set_status("↩  Undo applied.")

    def _redo(self, event=None):
        if not self.future:
            self._set_status("Nothing to redo."); return
        self.history.append(self.df.copy())
        self.df = self.future.pop()
        self._refresh()
        self._push_to_launcher()
        self._set_status("↪  Redo applied.")

    # ── Export helpers ────────────────────────────────────────────────────

    def _save_csv(self):
        if not self._need_df(): return
        p = filedialog.asksaveasfilename(defaultextension=".csv",
                                         filetypes=[("CSV", "*.csv")])
        if not p: return
        self.df.to_csv(p, index=False)
        self._log(f"Saved CSV: {os.path.basename(p)}")
        self._set_status(f"✔  Saved: {os.path.basename(p)}", SUCCESS)
        # push changes back to launcher
        if self.launcher:
            self.launcher.push_df_from_tool(self.df, p)

    def _save_excel(self):
        if not self._need_df(): return
        p = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                         filetypes=[("Excel", "*.xlsx")])
        if not p: return
        self.df.to_excel(p, index=False)
        self._log(f"Saved Excel: {os.path.basename(p)}")
        self._set_status(f"✔  Saved: {os.path.basename(p)}", SUCCESS)
        if self.launcher:
            self.launcher.push_df_from_tool(self.df, p)

    def _export_log(self):
        if not self.action_log:
            messagebox.showinfo("Log Empty", "No actions recorded yet."); return
        p = filedialog.asksaveasfilename(defaultextension=".txt",
                                         filetypes=[("Text file", "*.txt")])
        if not p: return
        with open(p, "w") as f:
            f.write("\n".join(self.action_log))
        self._set_status(f"✔  Log saved: {os.path.basename(p)}", SUCCESS)

    # ── Helpers ───────────────────────────────────────────────────────────

    def _log(self, message):
        self.action_log.append(f"[{datetime.now().strftime('%H:%M:%S')}]  {message}")

    def _need_df(self):
        if self.df is None:
            messagebox.showwarning("No Data",
                "No file loaded yet.\n\nLoad a file from the main launcher (top bar).")
            return False
        return True

    def _set_status(self, msg, color=None):
        if hasattr(self, "status_var"):
            self.status_var.set(msg)
            self.after(4000, lambda: self.status_var.set("Ready."))

    def _confirm_preview(self, operation_name, preview_df, action_callback):
        c = T.get_colors()
        win = tk.Toplevel(self)
        win.title(f"Preview — {operation_name}")
        win.configure(bg=c["BG_DARK"])
        center_window(win, 700, 420)
        tk.Label(win, text=f"⚠  You are about to: {operation_name}",
                 font=FONT_HEADING, fg=WARN, bg=c["BG_DARK"]).pack(pady=(14, 4))
        tk.Label(win, text="Sample of data BEFORE the operation (first 5 rows):",
                 font=FONT_SMALL, fg=c["TEXT_MUTED"], bg=c["BG_DARK"]).pack(anchor="w", padx=14)
        txt = tk.Text(win, height=8, bg=c["BG_CARD"], fg=c["TEXT_PRIMARY"],
                      font=FONT_MONO, relief="flat", padx=10, pady=8)
        txt.pack(fill="x", padx=14, pady=(4, 10))
        txt.insert("1.0", preview_df.head(5).to_string())
        txt.config(state="disabled")
        btn_row = tk.Frame(win, bg=c["BG_DARK"])
        btn_row.pack(pady=6)
        def confirm(): win.destroy(); action_callback()
        tk.Button(btn_row, text="✔  Apply", command=confirm,
                  bg=SUCCESS, fg=c["BG_DARK"], font=FONT_BODY,
                  relief="flat", padx=18, pady=7, cursor="hand2").pack(side="left", padx=8)
        tk.Button(btn_row, text="✖  Cancel", command=win.destroy,
                  bg=DANGER, fg="#fff", font=FONT_BODY,
                  relief="flat", padx=18, pady=7, cursor="hand2").pack(side="left", padx=8)

    def _on_close(self):
        T.unregister_window(self)
        self.destroy()

    # ── Stubs (must be implemented by subclasses) ─────────────────────────

    def _build_ui(self):
        raise NotImplementedError

    def _refresh(self):
        pass

    def _post_load(self, path):
        pass

    def apply_theme(self):
        pass
