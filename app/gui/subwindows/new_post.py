import tkinter as tk
import shutil
import os
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

class NewPost(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        self.main_frame = tk.Frame(self, bg="red")
        self.main_frame.pack(fill='both', expand= True,padx=10, pady=10)
        landing_btn = tk.Button(self.main_frame, text="landing", command=lambda: main_window.load_content("Landing"))
        landing_btn.pack()
        lbl = tk.Label(self.main_frame, text= "NEW POST PAGE")
        lbl.pack()

        self.media = []
        self.tk_images = []

        media_list= MediaList(self.main_frame, self.media, self.tk_images)
        media_list.pack(side="left")
        get_media_btn = GetMediaBtn(self.main_frame, self.media, self.tk_images, media_list, max_items=MAX_MEDIA_ITEMS)
        get_media_btn.pack()
        self.text_field = TextField(self.main_frame)
        self.text_field.pack()

        build_post_btn = tk.Button(self.main_frame, text="Build Post", command=self.build_post)
        build_post_btn.pack(side="right")
        pass


    def build_post(self):
        text = self.text_field.get_text()
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
        
        if len(local_media_paths == 1):
            self.build_single_media_html(local_media_paths, text)
        else:
            print("Posts with multiple media elements not supported at this time.")
    
    def build_single_media_html(self, media_paths, text):
        pass