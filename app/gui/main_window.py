import tkinter as tk
from tkinter import font
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from util.controller import JsonController
from .subwindows.landing import Landing
from .subwindows.new_post import NewPost
from .subwindows.configure_website import ConfigureWebsite
from .subwindows.edit_posts import EditPosts

colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        FONT_SM = font.Font(family="Helvetica", size=10, weight="bold")
        self.title("Website Generator")
        self.geometry(f"{1820}x{1080}+5+5")
        self.resizable(True, True)
        self.minsize(1820, 1080 )
        self.config(bg=C3, border=2, relief="solid")
        
        #HEADER
        self.header_frame = tk.Frame(self, bg=C2, relief="ridge", border=3)
        self.header_frame.pack(fill='x', expand=False ,padx=20, pady=10, ipady=10)
        self.landing_btn = None
        self.page_title_lbl = None
        
        #BODY
        self.body_frame = tk.Frame(self, bg=C2, relief="ridge", border=4)
        self.body_frame.pack(fill='both', expand= True,padx=20, pady=(0,20))
        self.body_content = None
        
        self.load_content("Landing")

    def new_content_frame(self):
        if self.body_content:
            self.body_content.destroy()
        self.body_content = tk.Frame(self.body_frame, bg=C2, border=1, relief="solid")
        self.body_content.pack(fill='both', expand= True,padx=10, pady=10)
    
    def pack_landing_page_btn(self):
        FONT_SM = font.Font(family="Helvetica", size=10)
        self.landing_btn = tk.Button(
            self.header_frame, 
            text="Landing Page", 
            command=lambda: self.load_content("Landing"),
            font=FONT_SM,
            bg=C4)
        self.landing_btn.place(relx=1.0, x=-20, y=20, anchor="ne") 
    
    def remove_landing_page_btn(self):
        if self.landing_btn:
            self.landing_btn.pack_forget()

    def set_page_title(self, title):
        if self.page_title_lbl:
            self.page_title_lbl.pack_forget()
        FONT= font.Font(family="Helvetica", size=30, weight="bold")
        self.page_title_lbl = tk.Label(
            self.header_frame, 
            text=title, 
            bg=C1, 
            font= FONT,
            border=1,
            relief="solid")
        self.page_title_lbl.pack(expand=True, fill='both', padx=10, pady=10)

    def load_content(self, content):
        """
        Accepts new_content: "Landing", "NewPost", "ConfigureWebsite", "EditPosts"
        """
        self.new_content_frame()
        if content == "Landing":
            self.remove_landing_page_btn()
            self.set_page_title("Website Generator")
            landing = Landing(self.body_content, self)
            landing.pack(fill='both', expand= True)
        elif content == "NewPost":
            self.set_page_title("New Post")
            self.pack_landing_page_btn()
            new_post = NewPost(self.body_content, self)
            new_post.pack(fill='both', expand= True)
        elif content == "ConfigureWebsite":
            self.set_page_title("Configure Website")
            self.pack_landing_page_btn()
            configure_post = ConfigureWebsite(self.body_content, self)
            configure_post.pack(fill='both', expand= True)
        elif content == "EditPosts":
            self.set_page_title("Edit Posts")
            self.pack_landing_page_btn() 
            edit_posts = EditPosts(self.body_content, self)
            edit_posts.pack(fill='both', expand= True)
  
        self.body_content.pack(fill='both', expand= True, padx=10, pady=10)
        pass

