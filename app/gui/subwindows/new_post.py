import tkinter as tk
from bs4 import BeautifulSoup as bs
from datetime import datetime

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from gui.components.get_media import GetMediaBtn, MediaList
from gui.components.text_field import TextField
from util.controller import JsonController, HtmlController, FileController, Controller, StringController

MAX_MEDIA_ITEMS = 1


class NewPost(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        self.main_window:tk.Frame = main_window
        self.media = []
        self.tk_images = []

        #GROUPER FRAMES
        self.main_frame = tk.Frame(self, bg="red")
        self.main_frame.pack(fill='both')
        self.body_frame = tk.Frame(self.main_frame)
        self.body_frame.columnconfigure(0, weight=1)
        self.body_frame.columnconfigure(1, weight=1)
        self.body_frame.pack(fill='both', expand= True, padx=10, pady=10)
       
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
        body_right_frame = tk.Frame(self.body_frame)
        body_right_frame.columnconfigure(0, weight=1)
        body_right_frame.columnconfigure(1, weight=3)
        body_right_frame.grid(column=1, row=0)

        title_field_label = tk.Label(body_right_frame, text = "Title:")
        title_field_label.grid(column=0, row=0, sticky=tk.E)
        self.title_field = TextField(body_right_frame, 1)
        self.title_field.grid(column=1,row=0, sticky=tk.N)

        caption_field_label = tk.Label(body_right_frame, text = "Caption:")
        caption_field_label.grid(column=0, row=1, sticky=tk.NE, pady=30)
        self.caption_field = TextField(body_right_frame, field_height=30)
        self.caption_field.grid(column=1,row=1, sticky=tk.N,pady=30)

        #Footer
        build_post_btn = tk.Button(self.main_frame, text="Build Post", command=self.build_post)
        build_post_btn.pack(side="right")
    
    def get_caption_text(self)->str:
        caption = self.caption_field.get_text()
        if caption.endswith("\n"):
            caption = caption[:-1]
        return caption
    
    def get_title_text(self)->str:
        title = self.title_field.get_text()
        if title.endswith("\n"):
            title = title[:-1]
        return title

    def build_post(self):
        caption:str = self.get_caption_text()
        local_media_paths:list = FileController.add_media_to_assets_folder(self.media)
        if len(local_media_paths) == 0 and caption == "":
            #Build out if text is blank
            print("Upload Media or Text")
            return
        
        #IF post is single image
        if len(local_media_paths) == 1:
            self.build_single_media_post(local_media_paths[0], caption)
            self.main_window.load_content("Landing")
        #IF post is text only 
        elif len(local_media_paths) == 0: 
            print("Text only Posts not supported at this time")
        else:
            print("Posts with multiple media or video elements not supported at this time.") 
    

    def build_single_media_post(self, media:str, caption:str):
        html_webpage: bs = HtmlController.get_webpage_html()
        posts_div_tag = html_webpage.find("div", id="posts")
        if not posts_div_tag:
            raise ValueError("Error: No element with id 'posts' found.")
        
        config_data: dict = JsonController.get_config_data()
        base_link = config_data["base_link"]
        posts_data:dict = JsonController.get_posts_data()
        post_html: bs = HtmlController.get_post_component()
        post_messaging:bool = config_data["post_messaging"]
        title = self.get_title_text()
        media_link = StringController.format_media_link(base_link, media)
        new_post_id = Controller.get_unique_id(posts_data.keys())

        insert_post_id(post_html, new_post_id)
        insert_date(post_html)
        insert_title(post_html, title)
        insert_image(post_html, media)
        insert_caption(post_html, caption)
        insert_message_btn(post_messaging, post_html, title, media_link, caption)
        posts_div_tag.insert(0, post_html)     
        HtmlController.set_webpage_html(html_webpage)

        json_post_entry = {
            "date": str(datetime.now()),
            "title": title,
            "media_link": media_link,
            "caption": caption,
            "base_link": base_link 
        }
        JsonController.append_posts_data(post=json_post_entry, post_id= new_post_id)


        
def insert_post_id(post_html: bs, new_post_id):
    post_div_tag = post_html.find("div", id="post_id")
    if not post_div_tag:
        post_div_tag = post_html.find("div")
    if not post_div_tag:
        raise ValueError("Error: No <div> tag found for new_post_id element.")
    if post_div_tag:
        post_div_tag["id"] = new_post_id

def insert_date(post_html:bs):
    post_date:str = Controller.get_todays_date()
    h6_tag = post_html.find("h6", id="date")
    if not h6_tag:
        h6_tag = post_html.find("h6")
    if not h6_tag:
        raise ValueError("Error: No <h6> tag found for date element.")
    if h6_tag:
        h6_tag.insert(0,post_date)

def insert_title(post_html:bs, title:str):
    h1_tag = post_html.find("h1", id="title")
    if not h1_tag:
        h1_tag = post_html.find("h6")
    if not h1_tag:
        raise ValueError("Error: No <h6> tag found for date element.")
    if h1_tag:
        h1_tag.insert(0,title)

def insert_image(post_html:bs, image:str):
    img_tag = post_html.find("img", id="media")
    if not img_tag:
        img_tag = post_html.find("img")
    if not img_tag:
        raise ValueError("Error: No <img> tag found for media element.")
    if img_tag:
        img_tag["src"] = image

def insert_caption(post_html:bs, caption:str):
    p_tag = post_html.find("p", id="caption")
    if not p_tag:
        p_tag = post_html.find("p")
    if not p_tag:
        raise ValueError("Error: No <p> tag found for caption element.")
    if p_tag:
        p_tag.insert(0,caption)

def insert_message_btn(post_messaging:bool, post_html:bs, title:str, media_link:str, caption:str):
    message_btn_tag = post_html.find("button", id="message_btn")
    if not message_btn_tag:
        raise ValueError("Error: No <button id=message_btn> tag found.")
    if not post_messaging:
        message_btn_tag.decompose()
        return
    onclick_value = "openMessageFrom('{}','{}', '{}')".format(title, media_link, caption)
    message_btn_tag["onclick"] = onclick_value
    message_btn_tag['onclick'] = message_btn_tag['onclick'].replace('\n', '')


def get_unique_id(dict_key_ids: list):
    highest_id = 0
    for id in dict_key_ids:
        id_int = int(id)
        if id_int > highest_id:
            highest_id = id_int
    new_id = highest_id + 1
    return f"{new_id:06d}" 
            