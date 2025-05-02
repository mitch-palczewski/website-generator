import tkinter as tk
import shutil
import os
from bs4 import BeautifulSoup as bs
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from gui.components.get_media import GetMediaBtn, MediaList
from gui.components.text_field import TextField

ASSET_FOLDER_PATH = "assets"
MAX_MEDIA_ITEMS = 1
HTML_FILE = "index.html"
HTML_CONTENT = """
        <div class="bg-gray-200 p-2 rounded shadow">
          <img
            alt="Photo 1"
            class="w-full h-auto object-cover rounded"
            src="https://via.placeholder.com/400"
        />
        <p></p>
        </div>
"""

class NewPost(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        self.main_window = main_window
        self.media = []
        self.tk_images = []

        #GROUPER FRAMES
        self.main_frame = tk.Frame(self, bg="red")
        self.main_frame.pack(fill='both')
        self.header_frame = tk.Frame(self.main_frame)
        self.header_frame.pack(fill='x',padx=10, pady=10)
        self.body_frame = tk.Frame(self.main_frame)
        self.body_frame.columnconfigure(0, weight=1)
        self.body_frame.columnconfigure(1, weight=1)
        self.body_frame.pack(fill='both', expand= True, padx=10, pady=10)

        #HEADER
        landing_btn = tk.Button(self.header_frame, text="Landing Page", command=lambda: main_window.load_content("Landing"))
        landing_btn.pack(side="right")
        lbl = tk.Label(self.header_frame, text= "NEW POST PAGE")
        lbl.pack()

        
        #BODY
            #BODY LEFT
        media_list= MediaList(self.body_frame, self.media, self.tk_images)
        media_list.grid(column=0,row=1, sticky=tk.NS)
        get_media_btn = GetMediaBtn(self.body_frame, self.media, self.tk_images, media_list, max_items=MAX_MEDIA_ITEMS)
        get_media_btn.grid(column=0,row=0, sticky=tk.N)

            #BODY RIGHT
        text_field_label = tk.Label(self.body_frame, text = "Post Text")
        text_field_label.grid(column=1, row=0, sticky=tk.N)
        self.text_field = TextField(self.body_frame)
        self.text_field.grid(column=1,row=1, sticky=tk.N)

        build_post_btn = tk.Button(self.main_frame, text="Build Post", command=self.build_post)
        build_post_btn.pack(side="right")
        pass


    def build_post(self):
        text = self.text_field.get_text()
        print(text)
        if len(self.media) == 0 and text == "":
            #Build out if text is blank
            print("Upload Media or Text")
            return
        print("Building Post")
        local_media_paths = []
        for media in self.media:
            shutil.copy(media, ASSET_FOLDER_PATH)
            file_name = os.path.basename(media)
            new_path = os.path.join(ASSET_FOLDER_PATH, file_name)
            local_media_paths.append(new_path)
        
        if len(local_media_paths) == 1:
            self.build_single_media_html(local_media_paths, text)
            print("Post With Single Media Built")
            self.main_window.load_content("Landing")
        elif len(local_media_paths) == 0: 
            print("Text only Posts not supported at this time")
        else:
            print("Posts with multiple media elements not supported at this time.")
    


    def build_single_media_html(self, media_paths: list, text:str):
        with open(HTML_FILE, "r", encoding="utf-8") as file:
            html_file_soup = bs(file, "html.parser")
        posts_div = html_file_soup.find("div", id="posts")
        if posts_div:
            html_content = bs(HTML_CONTENT, "html.parser")
            html_content = self.configure_content(html_content, media_paths[0], text)
            posts_div.insert(0, html_content)
        else:
            raise ValueError("Error: No element with id 'posts' found.")

        with open(HTML_FILE, "w", encoding="utf-8") as file:
            file.write(str(html_file_soup))
            pass



    def configure_content(self, html_content:bs, image:str, text:str):
        first_p = html_content.find("p")
        if first_p:
            first_p.insert(0,text)
        first_img = html_content.find("img")
        if  first_img:
            first_img["src"] = image
        return html_content