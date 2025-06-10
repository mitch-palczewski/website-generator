import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app.gui.components.html_component_editor import HtmlComponentEditor
from app.util.controller import JsonController, Controller
SITE_COMPONENT_PATH = Controller.get_resource_paths("html_webpage")
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]

class ConfigSite(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(bg=C1)
        #GROUPER FRAMES
        body = tk.Frame(self, bg="red")
        body.pack()
        
        component_editor = HtmlComponentEditor(body, SITE_COMPONENT_PATH, "site")
        component_editor.pack()
