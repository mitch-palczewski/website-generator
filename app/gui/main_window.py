import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from .subwindows.landing import Landing
from .subwindows.new_post import NewPost
from .subwindows.configure_website import ConfigureWebsite
from .subwindows.edit_posts import EditPosts

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Website Generator")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width-200}x{screen_height-200}+5+5")
        self.resizable(True, True)
        self.config(bg="blue")
        
        #HEADER
        self.header_frame = tk.Frame(self)
        self.header_frame.pack(fill='x',padx=10, pady=10)
        self.landing_btn = None
        self.page_title_lbl = None
        
        #BODY
        self.body_frame = tk.Frame(self, bg="brown")
        self.body_frame.pack(fill='both', expand= True,padx=10, pady=10)
        self.body_content = None
        
        
        self.load_content("Landing")



    
    def new_content_frame(self):
        if self.body_content:
            self.body_content.destroy()
        self.body_content = tk.Frame(self.body_frame, bg="green")
        self.body_content.pack(fill='both', expand= True,padx=10, pady=10)
    
    def pack_landing_page_btn(self):
        self.landing_btn = tk.Button(self.header_frame, text="Landing Page", command=lambda: self.load_content("Landing"))
        self.landing_btn.pack(side="right")
    
    def remove_landing_page_btn(self):
        if self.landing_btn:
            self.landing_btn.pack_forget()

    def set_page_title(self, title):
        if self.page_title_lbl:
            self.page_title_lbl.pack_forget()
        self.page_title_lbl = tk.Label(self.header_frame, text=title)
        self.page_title_lbl.pack()

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
