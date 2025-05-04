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
MESSAGE_HTML = "html_components\communicate\message.html"
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
        body_left_frame = tk.Frame(self.body_frame)
        body_left_frame.grid(column=0, row=0, sticky=tk.N)
        media_list= MediaList(
            body_left_frame, 
            self.media, 
            self.tk_images)
        get_media_btn = GetMediaBtn(
            body_left_frame, 
            self.media, 
            self.tk_images, 
            media_list, 
            max_items=MAX_MEDIA_ITEMS)
        get_media_btn.pack(pady=10)
        media_list.pack()

            #BODY RIGHT
                #TITLE ENTRY
        body_right_frame = tk.Frame(self.body_frame)
        body_right_frame.columnconfigure(0, weight=1)
        body_right_frame.columnconfigure(1, weight=3)
        body_right_frame.grid(column=1, row=0)

        title_field_label = tk.Label(body_right_frame, text = "Title:")
        title_field_label.grid(column=0, row=0, sticky=tk.E)
        self.title_field = TextField(body_right_frame, 1)
        self.title_field.grid(column=1,row=0, sticky=tk.N)

                #CAPTION ENTRY
        caption_field_label = tk.Label(body_right_frame, text = "Caption:")
        caption_field_label.grid(column=0, row=1, sticky=tk.NE, pady=30)
        self.caption_field = TextField(body_right_frame, 8)
        self.caption_field.grid(column=1,row=1, sticky=tk.N,pady=30)

        #Footer
        build_post_btn = tk.Button(self.main_frame, text="Build Post", command=self.build_post)
        build_post_btn.pack(side="right")
        pass

    def build_post(self):
        caption:str = self.caption_field.get_text()
        post_date:str = get_date()
        local_media_paths = []

        if len(self.media) == 0 and caption == "":
            #Build out if text is blank
            print("Upload Media or Text")
            return
        
        for media in self.media:
            new_path:str = move_media_to_folder(media, ASSET_FOLDER_PATH)
            local_media_paths.append(new_path)
        
        #IF post is single image
        if len(local_media_paths) == 1:
            self.build_single_media_html(local_media_paths, caption, post_date)
            self.main_window.load_content("Landing")
        #IF post is text only 
        elif len(local_media_paths) == 0: 
            print("Text only Posts not supported at this time")
        else:
            print("Posts with multiple media or video elements not supported at this time.") 
    

    def build_single_media_html(self, media_paths: list, caption:str, post_date:str):
        html_webpage: bs = open_html(HTML_FILE_PATH)
        if not html_webpage:
            raise ValueError("Error: HTML webpage not found in file system.")
        posts_div_tag = html_webpage.find("div", id="posts")
        if not posts_div_tag:
            raise ValueError("Error: No element with id 'posts' found.")
        config_data: dict = open_json(CONFIG_JSON_PATH)
        post_html: bs = open_html(config_data["post_component"])
        post_commenting:bool = config_data["post_commenting"]
        post_messaging:bool = config_data["post_messaging"]
        email:str = config_data["email"]
        post_html = self.configure_content(post_html, media_paths[0], caption, post_date)
        if post_messaging:
            post_html = self.configure_messaging(post_html, email)
        posts_div_tag.insert(0, post_html)     
        write_html_file(HTML_FILE_PATH, html_webpage)
    
    def configure_messaging(self, post_html:bs, email:str):
        message_html:bs = open_html(MESSAGE_HTML)
        if not message_html:
            raise ValueError("Error: message html not found.")
        message_form_tag = message_html.find("form", id="message_form")
        if not message_form_tag:
            raise ValueError("Error: id = message_form not found in message form html")
        message_div_tag = post_html.find("div", id="message_div")
        if not message_div_tag:
            raise ValueError("Error: id = message_div not found in post html.")
        formsubmit_link = "https://formsubmit.co/" + email
        message_form_tag["action"] = formsubmit_link
        message_div_tag.insert(0,message_form_tag)
        return post_html

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
        if not h6_tag:
            raise ValueError("Error: No <h6> tag found for date element.")
        if h6_tag:
            h6_tag.insert(0,post_date)
        
        #Inserts Title
        title = self.title_field.get_text()
        h1_tag = post_html.find("h1", id="title")
        if not h1_tag:
            h1_tag = post_html.find("h6")
        if not h1_tag:
            raise ValueError("Error: No <h6> tag found for date element.")
        if h1_tag:
            h1_tag.insert(0,title)

        
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