import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

class NewPost(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        self.content_frame = tk.Frame(self, bg="red")
        self.content_frame.pack(fill='both', expand= True,padx=10, pady=10)
        landing_btn = tk.Button(self.content_frame, text="landing", command=lambda: main_window.load_content("Landing", self))
        landing_btn.pack()
        lbl = tk.Label(self.content_frame, text= "NEW POST PAGE")
        lbl.pack()
        pass