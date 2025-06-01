import tkinter as tk
from bs4 import BeautifulSoup as bs
import os

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app.gui.components.scroll_frame import ScrollFrame
from app.gui.components.post import Post
from app.util.controller import HtmlController, JsonController
from app.config import get_app_root

class EditPosts(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        grid_cols = JsonController.get_config_data("grid_cols")
        self.lg_grid_cols:int = int(grid_cols["lg"])
        self.row = 0
        self.col = 0 

        #GROUPER FRAMES
        self.main_frame = tk.Frame(self, bg="purple")
        self.main_frame.pack(fill='both')
        scroll_frame = ScrollFrame(self.main_frame, 900, 900)
        scroll_frame.pack(expand=True, fill='both')
        inner_scroll_frame = scroll_frame.inner_frame
        self.post_grid = tk.Frame(inner_scroll_frame)
        for col in range(self.lg_grid_cols):
            self.post_grid.columnconfigure(col, weight=1)
        self.post_grid.pack()
        self.init_scrollframe()

    def init_scrollframe(self):
        webpage_html = HtmlController.get_webpage_html()
        posts = webpage_html.find_all("div", attrs={"data-type": "post"})
        for post in posts:
            self.get_next_row_column()
            self.get_post_attributes(post)

    def reset_scrollframe(self):
        for widget in self.post_grid.winfo_children():
            widget.destroy()
        self.init_scrollframe()

    def get_post_attributes(self, post: bs):
        try:
            title:str = post.find("h1",attrs={"data-type": "title"}).text
            title = title.strip()
        except:
            title = ""
        try:
            img_src:str = post.find("img", attrs={"data-type": "media"})["src"]
            img_src = os.path.join(get_app_root(), img_src)
        except:
            img_src = None
        try:
            caption:str = post.find(attrs={"data-type": "caption"}).text
            caption = caption.strip()
        except:
            caption = ""
        try: 
            post_tag = post.find("div", attrs={"data-type": "post"})
            
            for post_class in post_tag.get('class', []):
                if post_class.startswith('lg:grid-col-'):
                    span = int(post_class.split('-')[-1])
        except:
            span = 1
        try:
            id:str = post["data-post_id"]
            id = id.strip()
        except:
            id = ""
            return
        post_frame = Post(self.post_grid, id, title, img_src, caption, span, self)
        post_frame.grid(column= self.col, row=self.row, padx=20, pady=20)
        pass

    def get_next_row_column(self):
        self.col += 1 
        if self.col > self.lg_grid_cols or self.col > 2:
            self.col = 0 
            self.row += 1
        