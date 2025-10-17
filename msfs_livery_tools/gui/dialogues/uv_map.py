import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
from .. import helpers, styles
import __main__

class UVDialogue(object):
    win:tk.Tk
    container:ttk.Frame
    dest:helpers.PathChooser
    texture_frame:ttk.Frame
    texture:helpers.PathChooser
    clear_texture_button:ttk.Button
    model:helpers.PathChooser
    buttons_frame:ttk.Frame
    cancel_button:ttk.Button
    create_button:ttk.Button
    
    def __init__(self, *args, **kwargs):
        self.win = tk.Tk()
        self.win.title('MSFS Livery Tools – create texture map')
        self.win.iconbitmap(Path(__main__.RESOURCES_DIR, 'msfs livery tools.ico'))
        self.container = ttk.Frame(self.win, padding=styles.FRAME_PADDING)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.dest = helpers.PathChooser(
            self.container,
            title='Destination folder',
            state=tk.NORMAL,
            dialog=filedialog.askdirectory,
            dialog_title='Choose texture map destination folder',
            command=lambda: None,
        )
        self.dest.pack(fill=tk.X)
        self.texture_frame = ttk.Frame(self.container)
        self.texture_frame.pack(fill=tk.X)
        self.texture = helpers.PathChooser(
            self.texture_frame,
            title='Texture file (optional)',
            state=tk.NORMAL,
            dialog=filedialog.askopenfilename,
            dialog_title='Choose texture file',
            # extension=(('DDS texture', '.dds'), ('PNG image', '.png')),
            command=lambda: None,
        )
        self.texture.pack(fill=tk.X, side=tk.LEFT)
        self.clear_texture_button = ttk.Button(self.texture_frame, command=self.clear_texture, text='Clear')
        self.clear_texture_button.pack(side=tk.RIGHT)
        self.model = helpers.PathChooser(
            self.container,
            title='Model',
            state=tk.NORMAL,
            dialog=filedialog.askopenfilename,
            dialog_title='Choose model file',
            command=lambda: None,
        )
        self.model.pack(fill=tk.X)
        self.buttons_frame = ttk.Frame(self.win, padding=styles.FRAME_PADDING)
        self.buttons_frame.pack(fill=tk.X)
        self.cancel_button = ttk.Button(self.buttons_frame, text='Cancel', command=self.cancel)
        self.cancel_button.pack(side=tk.RIGHT)

    def clear_texture(self):
        self.texture.set(helpers.NOT_SET)
    
    def cancel(self):
        self.win.destroy()
    
    def extract_textures(self):
        pass
