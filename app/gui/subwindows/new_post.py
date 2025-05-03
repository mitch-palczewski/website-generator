import tkinter as tk
import shutil
import os
import json
from bs4 import BeautifulSoup as bs
from datetime import date

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from gui.components.get_media import GetMediaBtn, MediaList
from gui.components.text_field import TextField

CONFIG_JSON_PATH = "app\config\config.json"
ASSET_FOLDER_PATH = "assets"
MAX_MEDIA_ITEMS = 1
HTML_FILE_PATH = "index.html"

class NewPost(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        self.main_window:tk.Frame = main_window
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
        landing_btn = tk.Button(
            self.header_frame, 
            text="Landing Page", 
            command=lambda: main_window.load_content("Landing"))
        landing_btn.pack(side="right")
        lbl = tk.Label(self.header_frame, text= "NEW POST PAGE")
        lbl.pack()

        
        #BODY
            #BODY LEFT
        media_list= MediaList(
            self.body_frame, 
            self.media, 
            self.tk_images)
        media_list.grid(column=0,row=1, sticky=tk.NS)
        get_media_btn = GetMediaBtn(
            self.body_frame, 
            self.media, 
            self.tk_images, 
            media_list, 
            max_items=MAX_MEDIA_ITEMS)
        get_media_btn.grid(column=0,row=0, sticky=tk.N)

            #BODY RIGHT
        text_field_label = tk.Label(self.body_frame, text = "Post Text")
        text_field_label.grid(column=1, row=0, sticky=tk.N)
        self.text_field = TextField(self.body_frame)
        self.text_field.grid(column=1,row=1, sticky=tk.N)

        #Footer
        build_post_btn = tk.Button(self.main_frame, text="Build Post", command=self.build_post)
        build_post_btn.pack(side="right")
        pass

    def build_post(self):
        caption:str = self.text_field.get_text()
        post_date:str = get_date()
        local_media_paths = []
        
        if len(self.media) == 0 and caption == "":
            #Build out if text is blank
            print("Upload Media or Text")
            return
        for media in self.media:
            new_path:str = move_media_to_folder(media, ASSET_FOLDER_PATH)
            local_media_paths.append(new_path)
        
        if len(local_media_paths) == 1:
            self.build_single_media_html(local_media_paths, caption, post_date)
            self.main_window.load_content("Landing")
        elif len(local_media_paths) == 0: 
            print("Text only Posts not supported at this time")
        else:
            print("Posts with multiple media elements not supported at this time.") 

    def build_single_media_html(self, media_paths: list, caption:str, post_date:str):
        html_webpage: bs = open_html(HTML_FILE_PATH)
        posts_div_tag = html_webpage.find("div", id="posts")
        if posts_div_tag:
            config_data: dict = open_json(CONFIG_JSON_PATH)
            post_html: bs = open_html(config_data["post_component"])
            post_html = self.configure_content(post_html, media_paths[0], caption, post_date)
            posts_div_tag.insert(0, post_html)
        else:
            raise ValueError("Error: No element with id 'posts' found.")
        write_html_file(HTML_FILE_PATH, html_webpage)

    def configure_content(self, post_html:bs, image:str, caption:str, post_date:str) -> bs: 
        """
        Edits the inserts data into the HTML component 
        """
        #Inserts Caption
        p_tag = post_html.find("p", id="caption")
        if not p_tag:
            p_tag = post_html.find("p")
        if not p_tag:
            raise ValueError("Error: No <p> tag found for caption element.")
        if p_tag:
            p_tag.insert(0,caption)
        
        #Inserts Image
        img_tag = post_html.find("img", id="media")
        if not img_tag:
            img_tag = post_html.find("img")
        if not img_tag:
            raise ValueError("Error: No <img> tag found for media element.")
        if img_tag:
            img_tag["src"] = image

        #Inserts Date
        h6_tag = post_html.find("h6", id="date")
        if not h6_tag:
            h6_tag = post_html.find("h6")
        if not img_tag:
            raise ValueError("Error: No <h6> tag found for date element.")
        if h6_tag:
            h6_tag.insert(0,post_date)
        
        return post_html

def open_html(html_file_path:str) -> bs:
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_file_soup = bs(file, "html.parser")
    return html_file_soup

def open_json(json_file_path:str) -> dict:
    with open(json_file_path, "r") as json_file:
        json_data: dict = json.load(json_file)
    return json_data

def write_html_file(html_file_path:str, html:bs) -> None:
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(str(html))

def move_media_to_folder(media:str, folder:str) -> str:
    shutil.copy(media, folder)
    file_name = os.path.basename(media)
    new_path = os.path.join(folder, file_name)
    return new_path

def get_date() -> str:
    unformatted_date:date = date.today()
    today_date: str = unformatted_date.strftime("%m-%d-%Y")
    return today_date