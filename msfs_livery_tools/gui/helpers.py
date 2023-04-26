"""Helpers to create composite widgets."""
from pathlib import PurePath
import tkinter as tk
from tkinter import ttk
from typing import Callable

NOT_SET = '---'

class ProjectMixin(object):
    """Mixin to add an update_project method.

    Args to __init__:
        app (object): object with "project" attribute. Defaults to None.
        property (str): name of the project attribute to update. Defaults to None.
        command: (Callable): callable to call if "app" and "property" are not set. Defaults to None.
        
    Raises:
        ValueError: Either "command" or both "project" and "property" must be set.
    """
    value:tk.StringVar
    app:object
    property:str
    command:Callable
    
    def __init__(self, app:object=None, property:str=None, command:Callable=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if command is None and (app is None or property is None):
            raise ValueError('Either "command" or both "app" and "property" must be set.')
        self.app, self.property, self.command = app, property, command
    
    def update_event(self, event):
        self.update_project()
    
    def load(self):
        try:
            value = getattr(self.app.project, self.property)
        except KeyError: # Not set on livery.ini:
            return
        self.set(value, loading=True)
    
    def set(self, value, loading=False):
        self.value.set(value)
        if not loading:
            self.update_project()
    
    def update_project(self):
        if not self.command:
            # Clears property from config file
            try:
                if self.value.get() == '':
                    delattr(self.app.project, self.property)
                else:
                    setattr(self.app.project, self.property, self.value.get())
            except AttributeError:
                pass # Not set
        else:
            self.command()

class CheckButton(ProjectMixin, ttk.Checkbutton):
    value:tk.BooleanVar
    
    def __init__(self, master, app:object=None, property:str=None, command:Callable=None, default:bool|None=None, *args, **kwargs):
        if default is None:
            self.value = tk.BooleanVar(master)
        else:
            self.value = tk.BooleanVar(master, default)
        super().__init__(master=master, app=app, property=property, command=command, variable=self.value, *args, **kwargs)
        self.bind('<FocusOut>', self.update_event) # <Button-1> and <space> trigger before value update.
        

class FolderChooser(ProjectMixin, ttk.Frame):
    label:ttk.Label
    button:ttk.Button
    value:tk.StringVar
    label_var:tk.StringVar
    title:str
    
    def __init__(self, master, app:object=None, property:str=None, button_command:Callable=None, title:str='', button_text='Choose…', value=NOT_SET, state=tk.DISABLED, *args, **kwargs):
        super().__init__(master=master, app=app, property=property, *args, **kwargs)
        self.value = tk.StringVar(self, value)
        self.title = title
        self.label_var = tk.StringVar(self, str(self))
        self.label = ttk.Label(self, textvariable=self.label_var)
        self.button = ttk.Button(self, text=button_text, command=button_command, state=state)
    
    def __str__(self):
        return f'{self.title}: "{PurePath(self.value.get())}"'
    
    def get(self):
        return self.value
    
    def set(self, *args, **kwargs):
        super().set(*args, **kwargs)
        self.label_var.set(str(self))
    
    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.label.pack(fill=tk.BOTH, side=tk.LEFT)
        self.button.pack(side=tk.RIGHT)

class LabelEntry(ProjectMixin, ttk.Frame):
    label:ttk.Label
    entry:ttk.Entry
    value:tk.StringVar
    property:str
    project:object
    command:Callable
    
    def __init__(self, master, label_text:str, value='', state=tk.DISABLED,
                 app=None, property:str=None, command:Callable=None, *args, **kwargs):
        super().__init__(master=master, app=app, property=property, command=command, *args, **kwargs)
        self.label = ttk.Label(self, text=label_text, )
        self.value = tk.StringVar(self, value)
        self.entry = ttk.Entry(self, textvariable=self.value, state=state)
        self.entry.bind('<FocusOut>', self.update_event)
        self.entry.bind('<Return>', self.update_event)
    
    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.label.pack(side=tk.LEFT)
        self.entry.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
    
    def get(self):
        return self.value.get()
