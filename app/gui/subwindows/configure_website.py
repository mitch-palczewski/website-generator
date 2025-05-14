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

from gui.subwindows.configure_windows.config_messaging import ConfigMessaging
from gui.subwindows.configure_windows.general_config import GeneralConfig
class ConfigureWebsite(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)

        #GROUPER FRAMES
        main_frame = tk.Frame(self, bg="red")
        main_frame.pack(fill='both')

        #HEADER
        header_frame = tk.Frame(main_frame, bg="green")
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=1)
        header_frame.columnconfigure(3, weight=1)
        header_frame.columnconfigure(4, weight=1)
        header_frame.pack(fill="x", expand=True)
        btn_padx = 10
        btn_pady = 5
        general_config_btn = tk.Button(
            header_frame, 
            text="General Configuration", 
            command=lambda:self.load_content("GeneralConfig")
        )
        general_config_btn.grid(column=0, row=0, sticky=tk.EW, padx=btn_padx, pady=btn_pady)
        config_messaging_btn = tk.Button(
            header_frame, 
            text="Configure Messaging", 
            command=lambda:self.load_content("ConfigMessaging")
        )
        config_messaging_btn.grid(column=1, row=0, sticky=tk.EW, padx=btn_padx, pady=btn_pady)   
        config_post_btn = tk.Button(
            header_frame, 
            text="Configure Post", 
            command=lambda:self.load_content("ConfigurePost")
        )
        config_post_btn.grid(column=2, row=0, sticky=tk.EW, padx=btn_padx, pady=btn_pady)
        config_header_btn = tk.Button(
            header_frame, 
            text="Configure Header", 
            command=lambda:self.load_content("ConfigureHeader")
        )
        config_header_btn.grid(column=3, row=0, sticky=tk.EW, padx=btn_padx, pady=btn_pady)
        config_footer_btn = tk.Button(
            header_frame, 
            text="Configure Footer", 
            command=lambda:self.load_content("ConfigureFooter")
        )
        config_footer_btn.grid(column=4, row=0, sticky=tk.EW, padx=btn_padx, pady=btn_pady)
        
        #BODY
        self.body_frame = tk.Frame(self, bg="brown")
        self.body_frame.pack(fill='both', expand= True,padx=10, pady=10)
        self.body_content = None


        self.load_content("GeneralConfig")

        
    def new_content_frame(self):
        if self.body_content:
            self.body_content.destroy()
        self.body_content = tk.Frame(self.body_frame, bg="green")
        self.body_content.pack(fill='both', expand= True,padx=10, pady=10)

    def load_content(self, content:str):
        """
        Accepts content: "GeneralConfig", "ConfigMessaging", 
        """
        self.new_content_frame()
        if content == "ConfigMessaging":
            config_messaging = ConfigMessaging(self.body_content)
            config_messaging.pack(fill='both', expand= True)
        if content == "GeneralConfig":
            general_config = GeneralConfig(self.body_content)
            general_config.pack(fill='both', expand= True)

        