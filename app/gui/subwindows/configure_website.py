import tkinter as tk
from tkinter import font
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from gui.subwindows.configure_windows.config_messaging import ConfigMessaging
from gui.subwindows.configure_windows.general_config import GeneralConfig
from gui.subwindows.configure_windows.config_post import ConfigPost
from gui.subwindows.configure_windows.config_header import ConfigHeader
from gui.subwindows.configure_windows.config_footer import ConfigFooter

from util.controller import JsonController
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]
C5 = colors["c5"]


class ConfigureWebsite(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        FONT_SM = font.Font(family="Helvetica", size=10)

        #GROUPER FRAMES
        main_frame = tk.Frame(self, bg=C1)
        main_frame.pack(fill='both')

        #HEADER
        header_frame = tk.Frame(main_frame, bg=C1)
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=1)
        header_frame.columnconfigure(3, weight=1)
        header_frame.columnconfigure(4, weight=1)
        header_frame.pack(fill="x", expand=True)
        btn_padx = 10
        btn_pady = 10
        self.general_config_btn = tk.Button(
            header_frame, 
            text="General Configuration", 
            command=lambda:self.load_content("GeneralConfig"),
            bg="white",
            font=FONT_SM
        )
        self.general_config_btn.grid(column=0, row=0, sticky=tk.EW, padx=btn_padx, pady=btn_pady)
        self.config_messaging_btn = tk.Button(
            header_frame, 
            text="Configure Messaging", 
            command=lambda:self.load_content("ConfigMessaging"),
            bg="white",
            font=FONT_SM
        )
        self.config_messaging_btn.grid(column=1, row=0, sticky=tk.EW, padx=btn_padx, pady=btn_pady)   
        self.config_post_btn = tk.Button(
            header_frame, 
            text="Configure Post", 
            command=lambda:self.load_content("ConfigPost"),
            bg="white",
            font=FONT_SM
        )
        self.config_post_btn.grid(column=2, row=0, sticky=tk.EW, padx=btn_padx, pady=btn_pady)
        self.config_header_btn = tk.Button(
            header_frame, 
            text="Configure Header", 
            command=lambda:self.load_content("ConfigHeader"),
            bg="white",
            font=FONT_SM
        )
        self.config_header_btn.grid(column=3, row=0, sticky=tk.EW, padx=btn_padx, pady=btn_pady)
        self.config_footer_btn = tk.Button(
            header_frame, 
            text="Configure Footer", 
            command=lambda:self.load_content("ConfigFooter"),
            bg="white",
            font=FONT_SM
        )
        self.config_footer_btn.grid(column=4, row=0, sticky=tk.EW, padx=btn_padx, pady=btn_pady)
        
        #BODY
        self.body_frame = tk.Frame(self, bg=C1)
        self.body_frame.pack(fill='both', expand= True)
        self.body_content = None


        self.load_content("GeneralConfig")

    def set_btns_color(self, color):
        self.general_config_btn.config(bg=color)
        self.config_messaging_btn.config(bg=color)
        self.config_post_btn.config(bg=color)
        self.config_header_btn.config(bg=color)
        self.config_footer_btn.config(bg=color)
        
    def new_content_frame(self):
        if self.body_content:
            self.body_content.destroy()
        self.body_content = tk.Frame(self.body_frame, bg=C1)
        self.body_content.pack(fill='both', expand= True)

    def load_content(self, content:str):
        """
        Accepts content: "GeneralConfig", "ConfigMessaging", "ConfigPost"
        """
        self.set_btns_color(C5)
        self.new_content_frame()
        if content == "ConfigMessaging":
            config_messaging = ConfigMessaging(self.body_content)
            config_messaging.pack(fill='both', expand= True)
            self.config_messaging_btn.config(bg=C4)
            return
        if content == "GeneralConfig":
            general_config = GeneralConfig(self.body_content)
            general_config.pack(fill='both', expand= True)
            self.general_config_btn.config(bg=C4)
            return
        if content == "ConfigPost":
            config_post = ConfigPost(self.body_content)
            config_post.pack(fill='both', expand= True)
            self.config_post_btn.config(bg=C4)
            return
        if content == "ConfigHeader":
            config_header = ConfigHeader(self.body_content)
            config_header.pack(fill='both', expand= True)
            self.config_header_btn.config(bg=C4)
            return
        if content == "ConfigFooter":
            config_footer = ConfigFooter(self.body_content)
            config_footer.pack(fill='both', expand= True)
            self.config_footer_btn.config(bg=C4)
            return
        print(f"{content} is not set up")
        