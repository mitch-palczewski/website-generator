import tkinter as tk
from tkinter import ttk, font
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
CAPTION_FEILD_HEIGHT = 25
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]


class NewPost(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        FONT_SM = font.Font(family="Helvetica", size=10)
        FONT_MD = font.Font(family="Helvetica", size=14)
        FONT_LG = font.Font(family="Helvetica", size=16)
        self.main_window:tk.Frame = main_window
        self.media = []
        self.tk_images = []
        self.post_components:list = FileController.get_post_component_basenames()
        self.post_component_paths = FileController.get_post_component_paths()
        self.post_option = tk.StringVar(self)
        self.post_component_basename = JsonController.get_post_component_basename()
        self.post_component_path = JsonController.get_config_data("post_component")


        #GROUPER FRAMES
        self.config(bg=C1)
        self.main_frame = tk.Frame(self, bg=C1)
        self.main_frame.pack(fill='both', padx=10, pady=10)
        self.body_frame = tk.Frame(self.main_frame, bg=C1)
        self.body_frame.columnconfigure(0, weight=1)
        self.body_frame.columnconfigure(1, weight=1)
        self.body_frame.pack(fill='both', expand= True)
       
        #BODY
            #BODY LEFT
        body_left_frame = tk.Frame(self.body_frame, bg=C2)
        body_left_frame.grid(column=0, row=0, sticky=tk.NSEW, ipadx=5, ipady=5, padx=10,pady=10)
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
        get_media_btn.pack(padx=10, pady=10, fill="x")
        media_list.pack()

            #BODY RIGHT
        body_right_frame = tk.Frame(self.body_frame, bg=C2)
        body_right_frame.columnconfigure(0, weight=1)
        body_right_frame.columnconfigure(1, weight=3)
        body_right_frame.grid(column=1, row=0, ipadx=5, sticky=tk.NSEW, padx=10, pady=10)
        
        post_option_style = ttk.Style(self)
        post_option_style.configure('Custom.TMenubutton', font=FONT_LG, width = 25, background="white", relief = "solid", borderwith = 3, bordercolor='SystemButtonFace')
        post_option_lbl = tk.Label(body_right_frame, text="Post Component:", bg=C2, font=FONT_SM)
        post_option_lbl.grid(column=0,row=0, sticky=tk.E, pady=2)
        post_option_menu = ttk.OptionMenu(
            body_right_frame,
            self.post_option,
            self.post_component_basename,
            *self.post_components,
            command= lambda value: JsonController.set_post_component(basename=value)
        )
        post_option_menu.config(style='Custom.TMenubutton')
        post_option_menu["menu"].config(font=FONT_MD, bg="white")
        post_option_menu.grid(column=1, row=0, sticky=tk.NW, pady=10, padx=(30,0))

        title_field_label = tk.Label(body_right_frame, text = "Title:", bg=C2, font=FONT_SM)
        title_field_label.grid(column=0, row=1, sticky=tk.E)
        self.title_field = TextField(body_right_frame, 1)
        self.title_field.grid(column=1,row=1, sticky=tk.N, pady=10)

        caption_field_label = tk.Label(body_right_frame, text = "Caption:", bg=C2, font=FONT_SM)
        caption_field_label.grid(column=0, row=2, sticky=tk.NE, pady=30)
        self.caption_field = TextField(body_right_frame, field_height=CAPTION_FEILD_HEIGHT)
        self.caption_field.grid(column=1,row=2, sticky=tk.N,pady=30)

        #Footer
        footer_frame = tk.Frame(self.main_frame, bg=C1)
        footer_frame.pack(expand=True, fill='x', padx=10, pady=10)
        build_post_font = font.Font(family="Helvetica", size=15, weight="bold")
        build_post_btn = tk.Button(
            footer_frame, 
            text="Build Post", 
            command=self.build_post, 
            font=build_post_font, 
            bg=C4,
            width=20)
        build_post_btn.pack(side="right")

        column_span_lbl = tk.Label(footer_frame, text="Column Span:", bg=C1)
        column_span_lbl.pack(side="left")
        self.column_span = tk.StringVar(value=1)
        column_span_spinbox = ttk.Spinbox(footer_frame, from_=1, to=10, textvariable=self.column_span, wrap=True, width=4)
        column_span_spinbox.pack(side='left')
        
    
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

    def update_selected_post_component():
        pass

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
            self.build_text_only_post(caption)
            self.main_window.load_content("Landing")
        else:
            print("Posts with multiple media or video elements not supported at this time.") 
    
    def build_text_only_post(self, caption:str):
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
        new_post_id = Controller.get_unique_id(posts_data.keys())
        insert_post_id(post_html, new_post_id, self.column_span.get())
        insert_date(post_html)
        insert_title(post_html, title)
        delete_media(post_html)
        insert_caption(post_html, caption)
        insert_message_btn(post_messaging, post_html, title, "", caption)
        posts_div_tag.insert(0, post_html)     
        HtmlController.set_webpage_html(html_webpage)
        json_post_entry = {
            "date": str(datetime.now()),
            "title": title,
            "media_link": "",
            "caption": caption,
            "base_link": base_link 
        }
        JsonController.append_posts_data(post=json_post_entry, post_id= new_post_id)

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

        insert_post_id(post_html, new_post_id, self.column_span.get())
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


        
def insert_post_id(post_html: bs, new_post_id, column_span:str):
    column_span_class = 'col-span-' + column_span
    post_div_tag = post_html.find("div", id="post_id")
    if not post_div_tag:
        post_div_tag = post_html.find("div")
    if not post_div_tag:
        raise ValueError("Error: No <div> tag found for new_post_id element.")
    post_div_tag["id"] = new_post_id
    post_div_tag['class'].append(column_span_class)



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

def delete_media(post_html:bs):
    media_tag = post_html.find("img", id="media")
    media_tag.extract()