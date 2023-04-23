"""TTK styles for the whole application."""
from tkinter import ttk
from tkinter import font as tkFont

BOLD_BUTTON:str = 'Bold.TButton'

_font = ['TkDefaultFont', 10]
_bold = _font.copy()
_bold.append('bold')

def default(root, style_var):
    style_var.configure('.', font=_font)

def bold(root, style_var):
    style_var.configure(BOLD_BUTTON, font=_bold)

def init(root):
    style = ttk.Style(root)
    default(root, style)
    bold(root, style)