import tkinter as tk
import shutil
import os
from bs4 import BeautifulSoup as bs
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from util.model import Model
from config import CONFIG_JSON_PATH

class GeneralConfiguration(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        #GROUPER FRAMES
        main_frame = tk.Frame(self, bg="red")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.pack(fill='both')
        left_frame = tk.Frame(main_frame )
        left_frame.grid(column=0, row=0)
        
        messaging_frame = ConfigureMessaging(left_frame)
        messaging_frame.pack()
        
        


class ConfigureMessaging(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config_data = Model.open_json(CONFIG_JSON_PATH)
        self.messaging = self.config_data["post_messaging"]

        self.messaging_toggle = tk.Button(self, command=self.toggle_message)
        self.messaging_toggle.pack()

        self.set_messaging_toggle()
    
    def toggle_message(self):
        if self.messaging:
            self.messaging = False
        else: 
            self.messaging = True
        self.config_data["post_messaging"] = self.messaging
        Model.write_json_file(CONFIG_JSON_PATH, self.config_data)
        self.set_messaging_toggle()
        pass

    def set_messaging_toggle(self):
        if self.messaging:
            self.messaging_toggle.config(text="Disable Messaging",
                                         bg="#72c5c0")
        else: 
            self.messaging_toggle.config(text="Enable Messaging",
                                         bg="grey")
        self.messaging_toggle.pack()
