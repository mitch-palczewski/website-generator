import tkinter as tk
from tkinter import font, ttk
from tkinter.messagebox import askyesno
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from gui.components.html_component_editor import HtmlComponentEditor

HEADER_COMPONENT_PATH = "html_components\header"

class ConfigHeader(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        #GROUPER FRAMES
        body = tk.Frame(self, bg="red")
        body.pack()
        
        component_editor = HtmlComponentEditor(body, HEADER_COMPONENT_PATH, "header")
        component_editor.pack()
