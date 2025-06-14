import tkinter as tk
import os 
from bs4 import BeautifulSoup as bs
from tkinter import font, ttk
from tkinter import filedialog as fd
from tkinter.colorchooser import askcolor

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app.util.controller import JsonController, FileController, HtmlController, Controller
from app.gui.components.config_text_editor import ConfigTextEditor

colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]


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
        icon_config = IconConfig(body)
        icon_config.grid(column=0, row=1, sticky=tk.W, pady=10)
        column_config = ColumnConfig(body)
        column_config.grid(column=0, row=2, sticky=tk.W, pady=10)
        bg_config = BackgroundColor(body)
        bg_config.grid(column=0, row=3, sticky=tk.W, pady=10)
        git_hub_config = ConfigTextEditor(body, "Github Repository Link:", update_github_repo_url, "github_repo_url", 60)
        git_hub_config.grid(column=0, row=4, sticky= tk.W, pady=10)

def update_github_repo_url(new_github_repo_url):
    JsonController.set_config_data("github_repo_url", new_github_repo_url)

class BackgroundColor(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(bg=C1)
        FONT_LG = font.Font(family="Helvetica", size=15, weight="bold")
        FONT_SM = font.Font(family="Helvetica", size=10, weight="bold")
        body= tk.Frame(self, bg = "white")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.pack(padx=5, pady=5)
        lbl = tk.Label(body, text="Background Color: ", font=FONT_LG, bg="white")
        lbl.grid(column=0, row=0)
        btn = tk.Button(body,
                        text= "Background Color",
                        command=  self.get_color,
                        font=FONT_SM
                        )
        btn.grid(column=1, row=0)
    
    def get_color(self):
        color = askcolor(title="Background Color")
        print(color)
        HtmlController.update_bg_color(color[1])
        Controller.web_page_change()
        pass

class IconConfig(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(bg=C1)
        FONT_LG = font.Font(family="Helvetica", size=15, weight="bold")
        FONT_SM = font.Font(family="Helvetica", size=10, weight="bold")
        body= tk.Frame(self, bg = "white")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.pack(padx=5, pady=5)
        lbl = tk.Label(body, text="Web Tab Icon: ", font=FONT_LG, bg="white")
        lbl.grid(column=0, row=0)
        btn = tk.Button(body,
                        text= "Upload Image",
                        command=  self.update_icon
                        ,font=FONT_SM
                        )
        btn.grid(column=1, row=0)

    def update_icon(self):
        self.get_media()
        Controller.web_page_change()

    def get_media(self):
        filetypes = (
            ('PNG', '*.png'),
            ('ICO', '*.ico'),
            ('SVG', '*.svg'),
        )
        file_path = fd.askopenfilename(
            title="media upload",
            initialdir=os.path.expanduser("~"),
            filetypes=filetypes
        )
        if file_path:
            self.set_webpage_icon(file_path)
            pass
    
    @staticmethod
    def set_webpage_icon(file_path:str):
        html_webpage: bs = HtmlController.get_webpage_html()
        icon_link = html_webpage.find("link", rel="icon")
        head_tag = html_webpage.find("head")
        paths = FileController.add_media_to_assets_folder([file_path])
        icon_path:str = paths[0]
        if icon_path.endswith(".ico"):
            html = f"<link rel='icon' type='image/x-icon' href='{icon_path}'>"
        else: 
            html = f"<link rel='icon' type='image/png' href='{icon_path}'>"
        bs_html = bs(html, "html.parser")
        if icon_link: 
            icon_link.decompose()
        head_tag.insert(0, bs_html)
        HtmlController.set_webpage_html(html_webpage)
    

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
        JsonController.update_tab_title(new_tab_title)
        Controller.web_page_change()
      
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

        self.config_data = JsonController.get_config_data()
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
        HtmlController.update_grid_cols(sm,md,lg)
      
    def cancel(self):
        self.sm_entry.delete(0,tk.END)
        self.md_entry.delete(0,tk.END)
        self.lg_entry.delete(0,tk.END)
        self.sm_entry.insert(0, self.grid_cols["sm"])
        self.md_entry.insert(0, self.grid_cols["md"])
        self.lg_entry.insert(0, self.grid_cols["lg"])
        pass