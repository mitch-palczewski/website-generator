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
        super().__init__(container)
        self.component_folder = component_folder
        self.component_type = component_type
        self.selected_component_path = None
        #GROUPER FRAME
        body = tk.Frame(self, bg="blue")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=3)
        body.pack(padx=10, fill="both", expand=True)
        footer = tk.Frame(self, bg="blue")
        footer.pack(padx=10, fill="both", expand=True)
        #BODY RIGHT
        self.text_editor = TextEditor(body, component_type, component_folder, html_component_editor= self)
        self.text_editor.grid(column=1,row=0)
        #BODY LEFT
        scroll_frame = ScrollFrame(body)
        scroll_frame.grid(column=0, row=0)
        inner_scroll_frame = scroll_frame.inner_frame
        self.scroll_body = tk.Frame(inner_scroll_frame)
        self.scroll_body.pack(expand=True, fill="both")
        #FOOTER
        input_btn = tk.Button(footer,text=f"Update {component_type} HTML", command=self.update_html, bg="orange")
        input_btn.pack(expand=True, fill='both', padx=10, pady=10)

        self.load_components()

    def load_components(self):
        TkModel.clear_frame(self.scroll_body)
        components = os.listdir(self.component_folder)
        for component in components:
            c = Component(
                container = self.scroll_body, 
                html_component_editor = self, 
                component= component, 
                component_folder= self.component_folder, 
                text_editor= self.text_editor)
            c.pack()
    
    def update_html(self):
        HtmlController.update_component(
            component_type=self.component_type, 
            component_path = self.selected_component_path)

    def set_selected_component_path(self, path):
        self.selected_component_path = path

    

class TextEditor(tk.Frame):
    def __init__(self, container, component_type:str, component_folder:str, html_component_editor: HtmlComponentEditor):
        super().__init__(container)
        self.component_type = component_type
        self.component_folder = component_folder
        self.html_component_editor = html_component_editor

        self.text_field = ScrolledText(self, height=28)
        self.text_field.pack()
        footer = tk.Frame(self, bg="blue")
        footer.pack(fill='x', expand=True, ipady=10, ipadx=10)
        format_btn = tk.Button(footer, text="Format", command=self.format)
        format_btn.pack(side=tk.LEFT, padx=5)
        self.save_btn = tk.Button(footer, text="Save", command=self.save)
        self.save_btn.pack(side=tk.RIGHT, padx=5)
        self.validate_btn = tk.Button(footer, text="Validate", command=self.validate)
        self.validate_btn.pack(side=tk.RIGHT, padx=5)
    
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
    def __init__(self, container, html_component_editor: HtmlComponentEditor,component:str, component_folder:str, text_editor:TextEditor):
        super().__init__(container)
        self.html_component_editor = html_component_editor
        component_path = os.path.join(component_folder, component)
        self.text_editor = text_editor
        
        body = tk.Frame(container, bg="blue")
        body.pack(padx=10, pady=10)
        btn = tk.Button(body, 
                        text = component, 
                        command=lambda path=component_path: self.load(path))
        btn.pack()
    
    def load(self, component_path:str):
        self.html_component_editor.set_selected_component_path(component_path)
        self.text_editor.load_html(component_path)



