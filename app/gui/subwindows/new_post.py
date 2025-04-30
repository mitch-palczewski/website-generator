import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from gui.components.get_media_btn import GetMediaBtn

class NewPost(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        self.main_frame = tk.Frame(self, bg="red")
        self.main_frame.pack(fill='both', expand= True,padx=10, pady=10)
        landing_btn = tk.Button(self.main_frame, text="landing", command=lambda: main_window.load_content("Landing"))
        landing_btn.pack()
        lbl = tk.Label(self.main_frame, text= "NEW POST PAGE")
        lbl.pack()
        get_media_btn = GetMediaBtn(self.main_frame)
        get_media_btn.pack()
        pass

