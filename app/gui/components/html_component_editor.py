import tkinter as tk
import os
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from util.model import FileModel
from gui.components.scroll_frame import ScrollFrame



class HtmlComponentEditor(tk.Frame):
    def __init__(self, container, component_folder_path: str):
        super().__init__(container)
        body = tk.Frame(self, bg="blue")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.pack(padx=10, pady=10, fill="both", expand=True)
        scroll_frame = ScrollFrame(body)
        scroll_frame.grid(column=0, row=0)
        inner_scroll_frame = scroll_frame.inner_frame
        components = os.listdir(component_folder_path)
        for component_path in components:
            c = Component(inner_scroll_frame, component_path)
            c.pack()



class Component(tk.Frame):
    def __init__(self, container, component_path: str):
        super().__init__(container)
        body = tk.Frame(container, bg="blue")
        body.pack(padx=10, pady=10)
        btn = tk.Button(body, text = component_path, command=lambda path=component_path: self.load(path))
        btn.pack()
        

    def load(self,component_path:str):
        print(component_path)
        pass