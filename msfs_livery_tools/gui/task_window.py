import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from concurrent import futures
from queue import Queue
from pathlib import Path
import __main__

class TaskWindow(object):
    win:tk.Tk
    label_var:tk.StringVar
    label:ttk.Label
    progress_bar:ttk.Progressbar
    pool:futures.ThreadPoolExecutor
    task:futures.Future
    queue:Queue
    
    def __init__(self, title, text, func, callback, *args, **kwargs):
        # Window
        self.win = tk.Tk()
        self.win.title = title
        self.win.iconbitmap(Path(__main__.RESOURCES_DIR, 'msfs livery tools.ico'))
        self.label_var = tk.StringVar(self.win, text)
        self.label = ttk.Label(self.win, textvariable=self.label_var)
        self.label.pack(side=tk.TOP, fill=tk.X)
        self.progress_bar = ttk.Progressbar(self.win, mode='indeterminate', orient=tk.HORIZONTAL)
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Task
        self.callback = callback
        if 'queue' in kwargs.keys():
            self.queue = kwargs['queue']
        else:
            self.queue = None
        self.pool = futures.ThreadPoolExecutor()
        self.task = self.pool.submit(func, *args, **kwargs)
        
        # Monitor
        self.progress_bar.start()
        self.win.after(10, self.monitor)
        
    def monitor(self):
        if self.task.running():
            self.win.after(10, self.monitor)
            if self.queue:
                try:
                    self.label_var.set (self.label_var.get() + '\n' + self.queue.get_nowait())
                except:
                    pass
        else:
            self.progress_bar.stop()
            self.callback(self.task.result())
            self.pool.shutdown()
            self.win.destroy()
