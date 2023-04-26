"""TTK styles for the whole application."""
import tkinter as tk
from tkinter import ttk

BOLD_BUTTON:str = 'Bold.TButton'

_font = ['TkDefaultFont', 10]
_bold = _font.copy()
_bold.append('bold')

def default(style_var:ttk.Style):
    style_var.configure('.', font=_font)
    style_var.configure('.', padding=2)

def bold(style_var:ttk.Style):
    style_var.configure(BOLD_BUTTON, font=_bold)

def init(root):
    style = ttk.Style(root)
    default(style)
    bold(style)

class Separator(ttk.Separator):
    def pack(self, *args, **kwargs):
        kwargs.update({'padx': 2, 'pady': 2})
        super().pack(*args, **kwargs)
