import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import os
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from util.model import HtmlModel, TkModel
from util.controller import HtmlController
from gui.components.scroll_frame import ScrollFrame




class HtmlComponentEditor(tk.Frame):
    def __init__(self, container, component_folder: str, component_type:str):
        """
        component_type Literal ["post", "header", "footer"]
        """
        self.component_folder = component_folder
        super().__init__(container)
        body = tk.Frame(self, bg="blue")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=3)
        body.pack(padx=10, pady=10, fill="both", expand=True)
        #text Field
        self.text_editor = TextEditor(body, self, component_type, component_folder)
        self.text_editor.grid(column=1,row=0)
        
        #SELECTOR
        scroll_frame = ScrollFrame(body)
        scroll_frame.grid(column=0, row=0)
        inner_scroll_frame = scroll_frame.inner_frame
        self.scroll_body = tk.Frame(inner_scroll_frame)
        self.scroll_body.pack(expand=True, fill="both")

        self.load_components()

    def load_components(self):
        TkModel.clear_frame(self.scroll_body)
        components = os.listdir(self.component_folder)
        for component in components:
            c = Component(self.scroll_body, component, self.component_folder, self.text_editor)
            c.pack()

    

class TextEditor(tk.Frame):
    def __init__(self, container, html_component_editor: HtmlComponentEditor,component_type:str, component_folder:str):
        super().__init__(container)
        self.component_type = component_type
        self.component_folder = component_folder
        self.html_component_editor = html_component_editor

        self.text_field = ScrolledText(self, height=30)
        self.text_field.pack()
        footer = tk.Frame(self, bg="blue")
        footer.pack(fill='x', expand=True)
        format_btn = tk.Button(footer, text="Format", command=self.format)
        format_btn.pack(side=tk.LEFT, padx=5, pady=3)
        self.save_btn = tk.Button(footer, text="Save", command=self.save)
        self.save_btn.pack(side=tk.RIGHT, padx=5, pady=3)
        self.validate_btn = tk.Button(footer, text="Validate", command=self.validate)
        self.validate_btn.pack(side=tk.RIGHT, padx=5, pady=3)
    
    def load_html(self, component_path:str):
        self.selected_component_path = component_path
        html_component = HtmlModel.open_html(component_path)
        self.clear_text()
        self.text_field.insert('1.0', html_component)
    
    def clear_text(self):
        self.text_field.delete('1.0', tk.END)
    
    def format(self):
        text = self.text_field.get('1.0', tk.END)
        self.clear_text()
        text = HtmlModel.format_html(text)
        self.text_field.insert('1.0', text)
        pass

    def validate(self):
        text = self.text_field.get('1.0', tk.END)
        valid = HtmlController.validate_html(type="post", html=text)
        if valid:
            self.change_validate_btn_color("green")
        else:
            self.change_validate_btn_color("red")
        self.after(3000,lambda: self.change_validate_btn_color('#f0f0f0'))
        
    def save(self):
        html = self.text_field.get('1.0', tk.END)
        HtmlController.save_component_file(html, self.component_type)
        self.html_component_editor.load_components()
        

    def change_validate_btn_color(self, color):
        self.validate_btn.config(bg=color)
        
    def change_save_btn_color(self, color):
        self.save_btn.config(bg=color)

class Component(tk.Frame):
    def __init__(self, container, component:str, component_folder:str, text_editor:TextEditor):
        super().__init__(container)
        component_path = os.path.join(component_folder, component)
        self.text_editor = text_editor
        
        body = tk.Frame(container, bg="blue")
        body.pack(padx=10, pady=10)
        btn = tk.Button(body, 
                        text = component, 
                        command=lambda path=component_path: self.load(path))
        btn.pack()
    
    def load(self, component_path:str):
        self.text_editor.load_html(component_path)



