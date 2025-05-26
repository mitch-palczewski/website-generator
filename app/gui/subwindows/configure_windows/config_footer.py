import tkinter as tk
import os
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app.gui.components.html_component_editor import HtmlComponentEditor
from app.util.controller import JsonController


FOOTER_COMPONENT_PATH = os.path.join("html_components", "footer")

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
