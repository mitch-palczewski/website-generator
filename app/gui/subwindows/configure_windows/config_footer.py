import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from gui.components.html_component_editor import HtmlComponentEditor
import os

FOOTER_COMPONENT_PATH = os.path.join("html_components", "footer")
from util.controller import JsonController
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]

class ConfigFooter(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(bg=C1)
        #GROUPER FRAMES
        body = tk.Frame(self, bg="red")
        body.pack()
        
        component_editor = HtmlComponentEditor(body, FOOTER_COMPONENT_PATH, "footer")
        component_editor.pack()
