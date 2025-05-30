import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app.gui.components.scroll_frame import ScrollFrame
from app.gui.components.post import Post
from app.util.controller import HtmlController, JsonController

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
            try:
                title = post.find("h1",attrs={"data-type": "title"}).text
            except:
                title = ""
            try:
                img_src = post.find("img", attrs={"data-type": "media"})["src"]
            except:
                img_src = ""
            try:
                caption = post.find(attrs={"data-type": "caption"}).text
            except:
                caption = ""
            post = Post(self.inner_scroll_frame, title, img_src, caption, 1)
            post.pack(padx=20, pady=20)
