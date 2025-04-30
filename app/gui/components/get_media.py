# Button to get image from file system 

import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

class MediaList(tk.Frame):
    def __init__(self, container:tk.Frame, media: list):
        super().__init__(container)
        self.media = media
        self.media_content = tk.Frame(self, bg="maroon")
        self.media_content.pack(fill='both', expand= True,padx=10, pady=10)

    def update(self):
        self.media_content.destroy()
        self.media_content = tk.Frame(self, bg="maroon")
        self.media_content.pack(fill='both', expand= True,padx=10, pady=10)
        for index, m in enumerate(self.media):
            lbl = tk.Label(self.media_content, text=m)
            lbl.pack()
            x_btn = tk.Button(self.media_content, text="x", command= lambda idx=index: self.remove_media_element(idx))
            x_btn.pack()
        
    
    def remove_media_element(self, index):
        del self.media[index]
        self.update()
    

class GetMediaBtn(tk.Frame):
    def __init__(self, container:tk.Frame, media:list, media_list: MediaList, max_items: int):
        super().__init__(container)
        self.media = media
        self.media_list = media_list
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
        filename = fd.askopenfilename(
            title="media upload",
            initialdir=os.path.expanduser("~"),
            filetypes=filetypes
        )
        if filename:
            self.media.append(filename)
            self.media_list.update()
    



        