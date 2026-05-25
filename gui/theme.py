# theme.py — Shared design tokens for the Data Cleaning Suite
# Supports Dark (default) and Light mode

# ── Accent colours (same in both themes) ────────────────────────────────
ACCENT       = "#00D4AA"
ACCENT_DIM   = "#00A87F"
DANGER       = "#FF4C6A"
WARN         = "#F59E0B"
SUCCESS      = "#10B981"

# ── Typography ────────────────────────────────────────────────────────────────
# Available font families (all ship with Windows; most work on Mac/Linux too)
FONT_FAMILIES = [
    "Consolas",        # default — clean monospace
    "Courier New",     # classic monospace
    "Segoe UI",        # modern sans-serif
    "Arial",           # neutral sans-serif
    "Calibri",         # soft sans-serif
    "Georgia",         # serif
    "Trebuchet MS",    # rounded sans-serif
    "Verdana",         # wide & readable
    "Ink Free",        # casual handwriting (Windows 10+)
    "Segoe Script",    # cursive handwriting
    "Comic Sans MS",   # informal / rounded
]

_current_font = "Arial"   # change this default to switch the whole app

def _make_fonts(family):
    return {
        "FONT_TITLE":   (family, 22, "bold"),
        "FONT_HEADING": (family, 13, "bold"),
        "FONT_BODY":    (family, 11),
        "FONT_SMALL":   (family, 9),
        "FONT_MONO":    (family, 10),
    }

_fonts = _make_fonts(_current_font)
FONT_TITLE   = _fonts["FONT_TITLE"]
FONT_HEADING = _fonts["FONT_HEADING"]
FONT_BODY    = _fonts["FONT_BODY"]
FONT_SMALL   = _fonts["FONT_SMALL"]
FONT_MONO    = _fonts["FONT_MONO"]

def get_font():
    return _current_font

def set_font(family: str):
    """Switch font family app-wide and broadcast apply_theme() to all windows."""
    global _current_font, FONT_TITLE, FONT_HEADING, FONT_BODY, FONT_SMALL, FONT_MONO
    _current_font = family
    f = _make_fonts(family)
    FONT_TITLE   = f["FONT_TITLE"]
    FONT_HEADING = f["FONT_HEADING"]
    FONT_BODY    = f["FONT_BODY"]
    FONT_SMALL   = f["FONT_SMALL"]
    FONT_MONO    = f["FONT_MONO"]
    # Reuse the same broadcast mechanism as set_theme()
    for win in list(_open_windows):
        try:
            if win.winfo_exists() and hasattr(win, "apply_theme"):
                win.apply_theme()
        except Exception:
            pass

# ── Geometry helpers ──────────────────────────────────────────────────────────
PAD    = 16
RADIUS = 8

# ── Theme palettes ────────────────────────────────────────────────────────────
_DARK = {
    "BG_DARK":      "#0D1117",
    "BG_CARD":      "#161B22",
    "BG_HOVER":     "#1F2937",
    "TEXT_PRIMARY": "#E6EDF3",
    "TEXT_MUTED":   "#8B949E",
    "BORDER":       "#30363D",
    "TABLE_ALT":    "#1A2030",
}

_LIGHT = {
    "BG_DARK":      "#F0F4F8",
    "BG_CARD":      "#FFFFFF",
    "BG_HOVER":     "#E2E8F0",
    "TEXT_PRIMARY": "#1A202C",
    "TEXT_MUTED":   "#718096",
    "BORDER":       "#CBD5E0",
    "TABLE_ALT":    "#EBF4FF",
}

# Current theme state
_current_theme = "dark"
_theme_data    = dict(_DARK)

# Module-level colour vars (imported by all GUIs as `from theme import *`)
BG_DARK      = _theme_data["BG_DARK"]
BG_CARD      = _theme_data["BG_CARD"]
BG_HOVER     = _theme_data["BG_HOVER"]
TEXT_PRIMARY = _theme_data["TEXT_PRIMARY"]
TEXT_MUTED   = _theme_data["TEXT_MUTED"]
BORDER       = _theme_data["BORDER"]
TABLE_ALT    = _theme_data["TABLE_ALT"]

# Registry of all open windows so theme changes can be broadcast
_open_windows = []

def register_window(win):
    """Call this from every Toplevel/Tk window on creation."""
    _open_windows.append(win)

def unregister_window(win):
    if win in _open_windows:
        _open_windows.remove(win)

def get_theme():
    return _current_theme

def get_colors():
    """Return the current palette dict."""
    return dict(_theme_data)

def set_theme(name: str):
    """Switch to 'dark' or 'light' and notify all registered windows."""
    global _current_theme, _theme_data
    global BG_DARK, BG_CARD, BG_HOVER, TEXT_PRIMARY, TEXT_MUTED, BORDER, TABLE_ALT
    if name not in ("dark", "light"):
        return
    _current_theme = name
    _theme_data    = dict(_DARK if name == "dark" else _LIGHT)
    BG_DARK      = _theme_data["BG_DARK"]
    BG_CARD      = _theme_data["BG_CARD"]
    BG_HOVER     = _theme_data["BG_HOVER"]
    TEXT_PRIMARY = _theme_data["TEXT_PRIMARY"]
    TEXT_MUTED   = _theme_data["TEXT_MUTED"]
    BORDER       = _theme_data["BORDER"]
    TABLE_ALT    = _theme_data["TABLE_ALT"]
    # Notify all open windows
    for win in list(_open_windows):
        try:
            if win.winfo_exists() and hasattr(win, "apply_theme"):
                win.apply_theme()
        except Exception:
            pass

def center_window(win, w, h):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x  = (sw - w) // 2
    y  = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

def apply_base_style(win, title="Data Cleaning Suite"):
    win.title(title)
    win.configure(bg=BG_DARK)
    win.resizable(True, True)