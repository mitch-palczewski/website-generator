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
    def __init__(self, container, main_window):
        super().__init__(container)

        #GROUPER FRAMES
        self.main_frame = tk.Frame(self, bg="purple")
        self.main_frame.pack(fill='both')
        self.scroll_frame = ScrollFrame(self.main_frame, 900, 900)
        self.scroll_frame.pack(expand=True, fill='both')
        self.inner_scroll_frame = self.scroll_frame.inner_frame
        self.init_scrollframe()

    def init_scrollframe(self):
        webpage_html = HtmlController.get_webpage_html()
        posts = webpage_html.find_all("div", attrs={"data-type": "post"})
        for post in posts:
            self.get_post_attributes(post)

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
            id:str = post["data-post_id"]
            id = id.strip()
        except:
            id = ""
            print("Error did not find post id")
        print(f"{title}  {img_src}  {caption}  {id}")
        post_frame = Post(self.inner_scroll_frame, id, title, img_src, caption, 1)
        post_frame.pack(padx=20, pady=20)
        pass