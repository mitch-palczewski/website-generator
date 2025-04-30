import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from .subwindows.landing import Landing
from .subwindows.new_post import NewPost

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Website Generator")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width-200}x{screen_height-200}+5+5")
        self.resizable(True, True)
        self.config(bg="blue")
        
        self.body_frame = tk.Frame(self, bg="brown")
        self.body_frame.pack(fill='both', expand= True,padx=10, pady=10)


        #This Data is subject to change
        self.body_content  = tk.Frame(self.body_frame, bg="green")
        self.body_content.pack(fill='both', expand= True,padx=10, pady=10)
        landing = Landing(self.body_content, self)
        landing.pack()
    
    def new_content_frame(self):
        if self.body_content:
            self.body_content.destroy()
        self.body_content = tk.Frame(self.body_frame, bg="green")
        self.body_content.pack(fill='both', expand= True,padx=10, pady=10)


    def load_content(self, new_content:tk.Frame):
        self.new_content_frame()
        if new_content == "Landing":
            landing = Landing(self.body_content, self)
            landing.pack()
        elif new_content == "NewPost":
            new_post = NewPost(self.body_content, self)
            new_post.pack()
  
        self.body_content.pack(fill='both', expand= True,padx=10, pady=10)
        pass
