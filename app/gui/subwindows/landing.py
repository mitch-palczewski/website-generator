import tkinter as tk
from tkinter import font, ttk
from tkinter.messagebox import askyesno
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app.util.controller import JsonController
from app.util.serve_localhost import start_server

BUTTON_WIDTH = 25
BUTTON_HEIGHT = 2
BUTTON_PADDING = 15
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]

class Landing(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        BUTTON_FONT = font.Font(family="Helvetica", size=20, weight="bold")
        FONT_XL = font.Font(family="Helvetica", size=30, weight="bold")
        FONT_MD = font.Font(family="Helvetica", size=16, weight="bold")
        self.config(bg=C1)
        #GROUPER
        self.body = tk.Frame(self, bg=C2, border=3, relief="groove")
        self.body.pack( expand=True, padx=40, pady=80, fill='both')
        
        #BODY
        new_post_btn = tk.Button(
            self.body, 
            text="New Post", 
            command=lambda: main_window.load_content("NewPost"),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font= FONT_XL,
            bg="white"
        )
        new_post_btn.pack(padx=BUTTON_PADDING, pady=(80,BUTTON_PADDING))

        configure_post_btn = tk.Button(
            self.body,
            text="Configure Website",
            command=lambda: main_window.load_content("ConfigureWebsite"),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font=FONT_XL,
            bg="white"
        )
        configure_post_btn.pack(padx=BUTTON_PADDING, pady=BUTTON_PADDING)

        edit_post_btn = tk.Button(
            self.body,
            text="Edit Posts",
            command=lambda: main_window.load_content("EditPosts"),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font=BUTTON_FONT
        )
        edit_post_btn.pack(padx=BUTTON_PADDING, pady=BUTTON_PADDING)

        

        base_link = BaseLink(self.body)
        base_link.pack()

        test_webpage_btn = tk.Button(
            self.body,
            text="Test With Local Host",
            command= start_server,
            width=40,
            height= 1,
            font=FONT_MD,
            bg="white"
        )
        test_webpage_btn.pack(padx=BUTTON_PADDING, pady=BUTTON_PADDING)

        pass

class BaseLink(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        FONT_LG = font.Font(family="Helvetica", size=20, weight="bold")
        FONT_SM = font.Font(family="Helvetica", size=10, weight="bold")
        self.config_data = None
        self.base_link = None
        self.base_link_var = tk.StringVar()

        #GROUPER
        self.body = tk.Frame(self, bg=C4)
        self.body.columnconfigure(0, weight=1)
        self.body.columnconfigure(1, weight=3)
        self.body.columnconfigure(2, weight=1)
        self.body.columnconfigure(3, weight=1)
        self.body.pack(fill='x', pady=2, padx=2)

        #BODY
        self.lbl = tk.Label(self.body, text="Base Link:   ", font=FONT_LG, bg="white")
        self.lbl.grid(column=0, row=0)

        self.text_field = ttk.Entry(
            master=self.body, 
            width= 40,
            font=FONT_LG,
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
        new_base_link = self.text_field.get()
        if askyesno(title="Change Base Link", message=f"Are you sure you want to replace {self.base_link} with {new_base_link}"):
            JsonController.update_base_link(new_base_link)
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
        self.config_data = JsonController.get_config_data()

        self.base_link = self.config_data["base_link"]
        self.text_field.config(state="normal")
        self.text_field.delete(0, tk.END)
        self.text_field.insert(0, self.base_link)
        self.text_field.config(state="disabled")
        pass