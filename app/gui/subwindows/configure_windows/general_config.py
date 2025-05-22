import tkinter as tk
from tkinter import font, ttk
from tkinter.messagebox import askyesno
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from util.model_controller import Controller
from util.controller import JsonController
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]

"""
TODO 
Icon
"""
class GeneralConfig(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        FONT_SM = font.Font(family="Helvetica", size=10, weight="bold")
        FONT_MD = font.Font(family="Helvetica", size=15, weight="bold")
        FONT_LG = font.Font(family="Helvetica", size=15, weight="bold")
        self.config(bg=C1)

        #GROUPER FRAMES
        body = tk.Frame(self, bg=C1)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1,weight=1)
        body.pack(fill='both', padx=30, pady=30, expand=True)
        tab_title_config = TabTitleConfig(body)
        tab_title_config.grid(column=0, row=0, sticky=tk.W, pady=10)
        column_config = ColumnConfig(body)
        column_config.grid(column=0, row=1, sticky=tk.W, pady=10)

        

class TabTitleConfig(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(bg="white")
        FONT_SM = font.Font(family="Helvetica", size=10, weight="bold")
        FONT_MD = font.Font(family="Helvetica", size=15, weight="bold")
        FONT_LG = font.Font(family="Helvetica", size=15, weight="bold")
        self.config_data = JsonController.get_config_data()
        body= tk.Frame(self, bg = "white")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.columnconfigure(2, weight=1)
        body.columnconfigure(3, weight=1)
        body.pack(padx=5, pady=5)
        lbl = tk.Label(body, text="Web Tab Title: ", font=FONT_LG, bg="white")
        lbl.grid(column=0, row=0)
        self.entry = ttk.Entry(
            master=body, 
            font=FONT_MD,
            width= 38)
        self.entry.insert(0,self.config_data["tab_title"])
        self.entry.grid(column=1,row=0)
        update_btn = tk.Button(body, text="Update", font=FONT_SM, command=self.update)
        update_btn.grid(column=2,row=0)
        cancel_btn = tk.Button(body, text="Cancel", font=FONT_SM, command=self.cancel)
        cancel_btn.grid(column=3, row=0)

    def update(self):
        new_tab_title = self.entry.get()
        Controller.update_tab_title(new_tab_title)
      
    def cancel(self):
        self.entry.delete(0,tk.END)
        self.entry.insert(0,self.config_data["tab_title"])

class ColumnConfig(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(bg="white")
        FONT_SM = font.Font(family="Helvetica", size=10, weight="bold")
        FONT_MD = font.Font(family="Helvetica", size=15, weight="bold")
        FONT_LG = font.Font(family="Helvetica", size=15, weight="bold")

        self.config_data = Controller.get_config_data()
        self.grid_cols = self.config_data["grid_cols"]

        body= tk.Frame(self, bg="white")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.columnconfigure(2, weight=1)
        body.columnconfigure(3, weight=1)
        body.columnconfigure(4, weight=1)
        body.columnconfigure(5, weight=1)
        body.pack(padx=5, pady=5)


        screen_size_lbl = tk.Label(body, text="Screensize", font=FONT_SM, bg="white")
        screen_size_lbl.grid(column=1, row=0, padx=10, columnspan=3)
        lbl = tk.Label(body, text="Webpage Columns: ", font=FONT_LG, bg="white")
        lbl.grid(column=0, row=2)
        sm_lbl = tk.Label(body, text="Small", font=FONT_MD, bg="white")
        sm_lbl.grid(column=1, row=1, padx=10)
        md_lbl = tk.Label(body, text="Medium", font=FONT_MD, bg="white")
        md_lbl.grid(column=2, row=1, padx=10)
        lg_lbl = tk.Label(body, text="Large", font=FONT_MD, bg="white")
        lg_lbl.grid(column=3, row=1, padx=10)

        self.sm_entry = ttk.Entry( 
            master=body, 
            font=FONT_MD,
            width= 3)
        self.sm_entry.grid(column=1,row=2)
        self.sm_entry.insert(0, self.grid_cols["sm"])
        self.md_entry = ttk.Entry( 
            master=body, 
            font=FONT_MD,
            width= 3)
        self.md_entry.grid(column=2,row=2)
        self.md_entry.insert(0, self.grid_cols["md"])
        self.lg_entry = ttk.Entry( 
            master=body, 
            font=FONT_MD,
            width= 3)
        self.lg_entry.grid(column=3,row=2)
        self.lg_entry.insert(0, self.grid_cols["lg"])

        update_btn = tk.Button(body, text="Update", font=FONT_SM, command=self.update)
        update_btn.grid(column=4,row=2)
        cancel_btn = tk.Button(body, text="Cancel", font=FONT_SM, command=self.cancel)
        cancel_btn.grid(column=5, row=2)

    def update(self):
        sm = self.sm_entry.get()
        md = self.md_entry.get()
        lg = self.lg_entry.get()
        Controller.update_grid_cols(sm,md,lg)
      
    def cancel(self):
        self.sm_entry.delete(0,tk.END)
        self.md_entry.delete(0,tk.END)
        self.lg_entry.delete(0,tk.END)
        self.sm_entry.insert(0, self.grid_cols["sm"])
        self.md_entry.insert(0, self.grid_cols["md"])
        self.lg_entry.insert(0, self.grid_cols["lg"])
        pass