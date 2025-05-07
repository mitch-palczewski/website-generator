import tkinter as tk
from tkinter import font
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

BUTTON_WIDTH = 30
BUTTON_HEIGHT = 3
BUTTON_PADDING = 15



class Landing(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        self.content_frame = tk.Frame(self, bg="red")
        self.content_frame.pack( expand=True,padx=10, pady=10)
        BUTTON_FONT = font.Font(family="Helvetica", size=20, weight="bold")

        new_post_btn = tk.Button(
            self.content_frame, 
            text="New Post", 
            command=lambda: main_window.load_content("NewPost"),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font= BUTTON_FONT
        )
        new_post_btn.pack(padx=BUTTON_PADDING, pady=BUTTON_PADDING)

        configure_post_btn = tk.Button(
            self.content_frame,
            text="Configure Website",
            command=lambda: main_window.load_content("ConfigureWebsite"),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font=BUTTON_FONT
        )
        configure_post_btn.pack(padx=BUTTON_PADDING, pady=BUTTON_PADDING)

        edit_post_btn = tk.Button(
            self.content_frame,
            text="Edit Posts",
            command=lambda: main_window.load_content("EditPosts"),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font=BUTTON_FONT
        )
        edit_post_btn.pack(padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        pass