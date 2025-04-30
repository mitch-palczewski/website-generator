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


class GetMediaBtn(tk.Frame):
    def __init__(self, container):
        super().__init__(container),

        btn = tk.Button(self,
                        text= "Upload Image",
                        command= self.get_media
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
   
        