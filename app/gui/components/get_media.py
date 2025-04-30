# Button to get image from file system 

import tkinter as tk
from tkinter import filedialog as fd
import os
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

class MediaList(tk.Frame):
    def __init__(self, container:tk.Frame, media):
        super().__init__(container)
        self.media = media
        self.media_content = tk.Frame(self, bg="maroon")
        self.media_content.pack(fill='both', expand= True,padx=10, pady=10)

    def update(self):
        self.media_content.destroy()
        self.media_content = tk.Frame(self, bg="maroon")
        self.media_content.pack(fill='both', expand= True,padx=10, pady=10)
        for m in self.media:
            lbl = tk.Label(self.media_content, text=m)
            lbl.pack()
    

class GetMediaBtn(tk.Frame):
    def __init__(self, container:tk.Frame, media:list, media_list: MediaList):
        super().__init__(container)
        self.media = media
        self.media_list = media_list
        btn = tk.Button(self,
                        text= "Upload Image",
                        command=  self.get_media
                        )
        btn.pack()
    
    def get_media(self):
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
    



        