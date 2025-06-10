import tkinter as tk
from tkinter import ttk, font
from tkinter.messagebox import askyesno


try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app.util.controller import JsonController
MAX_IMG_HEIGHT = 600
MAX_IMG_WIDTH = 700
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]

class ConfigTextEditor(tk.Frame):
    def __init__(self, container, title, update_func, data_key, text_width = 40):
        "type [base_link, github_repo_url]"
        super().__init__(container)
        self.title = title
        self.update_func = update_func
        self.data_key = data_key
        FONT_LG = font.Font(family="Helvetica", size=20, weight="bold")
        FONT_MD = font.Font(family="Helvetica", size=16, weight="bold")
        FONT_SM = font.Font(family="Helvetica", size=10, weight="bold")
        self.config_data = None
        self.data = None
        self.data_var = tk.StringVar()

        #GROUPER
        self.body = tk.Frame(self, bg=C4)
        self.body.columnconfigure(0, weight=1)
        self.body.columnconfigure(1, weight=3)
        self.body.columnconfigure(2, weight=1)
        self.body.columnconfigure(3, weight=1)
        self.body.pack(fill='x', pady=2, padx=2)

        #BODY
        self.lbl = tk.Label(self.body, text=title, font=FONT_MD, bg="white")
        self.lbl.grid(column=0, row=0)

        self.text_field = ttk.Entry(
            master=self.body, 
            width= text_width,
            font=FONT_MD,
            state="disabled")
        self.text_field.grid(column=1,row=0)

        self.edit_btn = tk.Button(self.body, text="Edit", font=FONT_SM, command=self.edit, bg="white")
        self.edit_btn.grid(column=2, row=0, padx=5)  
        self.update_btn = tk.Button(self.body, text="Update", font=FONT_SM, command=self.update, bg="white")
        self.cancel_btn = tk.Button(self.body, text="Cancel", font=FONT_SM, command=self.cancel, bg="white")
        self.load_config_base_link()

    def edit(self):
        self.edit_btn.grid_forget()
        self.update_btn.grid(column=2, row=0,padx=5)
        self.cancel_btn.grid(column=3, row=0, padx=5)
        self.text_field.config(state="normal")

    def update(self):
        new_data = self.text_field.get()
        if askyesno(title=f"Change {self.title}", message=f"Are you sure you want to replace {self.data} with {new_data}"):
            self.update_func(new_data)
        self.update_btn.grid_forget()
        self.cancel_btn.grid_forget()
        self.edit_btn.grid(column=2, row=0, padx=5)
        self.text_field.config(state="disabled")
        self.load_config_base_link()

    def cancel(self):
        self.update_btn.grid_forget()
        self.cancel_btn.grid_forget()
        self.edit_btn.grid(column=2, row=0)
        self.text_field.config(state="disabled")
        self.load_config_base_link()

    def load_config_base_link(self):
        self.data = JsonController.get_config_data(self.data_key)
        self.text_field.config(state="normal")
        self.text_field.delete(0, tk.END)
        self.text_field.insert(0, self.data)
        self.text_field.config(state="disabled")
        pass