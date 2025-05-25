# Button to get image from file system 

import tkinter as tk
from tkinter import filedialog as fd, font
from tkinter.messagebox import showinfo
import os
from PIL import Image, ImageTk

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from util.controller import JsonController
MAX_IMG_HEIGHT = 600
MAX_IMG_WIDTH = 700
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]

class MediaList(tk.Frame):
    def __init__(self, container:tk.Frame, media: list, tk_images:list):
        super().__init__(container)
        self.media = media
        self.tk_images = tk_images
        self.config(bg="white")
        self.media_content = tk.Frame(self, bg="white", width=MAX_IMG_WIDTH+20)
        self.media_content.pack(fill='both',padx=10, pady=10)

    def update(self):
        self.media_content.destroy()
        self.media_content = tk.Frame(self, bg="white", width=MAX_IMG_WIDTH+20)
        self.media_content.pack(fill='both', padx=10, pady=10)
        for index, m in enumerate(self.media):
            #lbl = tk.Label(self.media_content, text=m, bg="white")
            #lbl.pack()
            img_group = tk.Frame(self.media_content, bg="white")
            img_group.columnconfigure(0, weight=4)
            img_group.columnconfigure(1, weight=1)
            img_group.pack(fill='x', expand=True)
            lbl = tk.Label(img_group,  image=self.tk_images[index], bg="white")
            lbl.grid(column=0, row=0)
            x_btn = tk.Button(
                img_group, 
                text="x", 
                command= lambda idx=index: self.remove_media_element(idx),
                bg=C4)
            x_btn.grid(column=1, row=0, sticky=tk.E, padx=3)
        
    
    def remove_media_element(self, index):
        del self.media[index]
        del self.tk_images[index]
        self.update()
    

class GetMediaBtn(tk.Frame):
    def __init__(self, container:tk.Frame, media:list, tk_images:list, MediaList: MediaList, max_items: int):
        super().__init__(container)
        self.media = media
        self.tk_images = tk_images
        self.MediaList = MediaList
        self.max_items = max_items
        FONT_SM = font.Font(family="Helvetica", size=10)
        btn = tk.Button(self,
                        text= "Upload Image",
                        command=  self.get_media
                        ,bg=C4
                        ,font=FONT_SM
                        )
        btn.pack(fill="x")
    
    def get_media(self):
        if len(self.media) >= self.max_items:
            showinfo(title="Media Maxed",
                     message=f"Max of {self.max_items} Images")
            return
        filetypes = (
            ('PNG', '*.png'),
        )
        file_path = fd.askopenfilename(
            title="media upload",
            initialdir=os.path.expanduser("~"),
            filetypes=filetypes
        )
        if file_path:
            self.media.append(file_path)
            self.tk_images.append(path_to_tk_image(file_path))
            self.MediaList.update()
    

def path_to_tk_image(file_path):
    img = Image.open(file_path)
    original_width, original_height = img.size
    scaling_factor = MAX_IMG_HEIGHT / original_height
    new_width = int(original_width * scaling_factor)
    resized_image = img.resize((new_width, MAX_IMG_HEIGHT), Image.LANCZOS)
    img.thumbnail((MAX_IMG_WIDTH, MAX_IMG_HEIGHT), Image.LANCZOS)

    photo = ImageTk.PhotoImage(img)
    return photo


        