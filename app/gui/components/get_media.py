# Button to get image from file system 

import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
from PIL import Image, ImageTk

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

class MediaList(tk.Frame):
    def __init__(self, container:tk.Frame, media: list, tk_images:list):
        super().__init__(container)
        self.media = media
        self.tk_images = tk_images
        self.media_content = tk.Frame(self, bg="maroon")
        self.media_content.pack(fill='both', expand= True,padx=10, pady=10)

    def update(self):
        self.media_content.destroy()
        self.media_content = tk.Frame(self, bg="maroon")
        self.media_content.pack(fill='both', expand= True,padx=10, pady=10)
        for index, m in enumerate(self.media):
            lbl = tk.Label(self.media_content, text=m)
            lbl.pack()
            lbl = tk.Label(self.media_content,  image=self.tk_images[index])
            lbl.pack()
            x_btn = tk.Button(self.media_content, text="x", command= lambda idx=index: self.remove_media_element(idx))
            x_btn.pack()
        
    
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
        btn = tk.Button(self,
                        text= "Upload Image",
                        command=  self.get_media
                        )
        btn.pack()
    
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
    img = img.resize((600, 400), Image.NEAREST)
    photo = ImageTk.PhotoImage(img)
    return photo


        