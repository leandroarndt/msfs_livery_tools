"""TTK styles for the whole application."""
import tkinter as tk
from tkinter import ttk

FRAME_PADDING = 5
BOLD_BUTTON = 'Bold.TButton'
HEADING = 'Heading.TLabel'

_font = ['TkDefaultFont', 10]
_bold_font = _font.copy()
_bold_font.append('bold')
_heading_font = [_font[0], int(_font[1]*1.6), 'bold']

def _default(style_var:ttk.Style):
    style_var.configure('.', font=_font)
    style_var.configure('.', padding=2)

def _bold(style_var:ttk.Style):
    style_var.configure(BOLD_BUTTON, font=_bold_font)

def _heading(style_var:ttk.Style):
    style_var.configure(HEADING, font=_heading_font)

def init(root):
    style = ttk.Style(root)
    _default(style)
    _bold(style)
    _heading(style)

class Separator(ttk.Separator):
    def pack(self, *args, **kwargs):
        kwargs.update({'padx': 2, 'pady': 2})
        super().pack(*args, **kwargs)
