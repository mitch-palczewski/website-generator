import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from gui.components.html_component_editor import HtmlComponentEditor

FOOTER_COMPONENT_PATH = "html_components\header"

class ConfigFooter(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        #GROUPER FRAMES
        body = tk.Frame(self, bg="red")
        body.pack()
        
        component_editor = HtmlComponentEditor(body, FOOTER_COMPONENT_PATH, "footer")
        component_editor.pack()
