import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

class Landing(tk.Frame):
    def __init__(self, container, main_window):
        super().__init__(container)
        self.content_frame = tk.Frame(self, bg="red")
        self.content_frame.pack(fill='both', expand= True,padx=10, pady=10)

        new_post_btn = tk.Button(
            self.content_frame, 
            text="New Post", 
            command=lambda: main_window.load_content("NewPost")
        )
        new_post_btn.pack()

        configure_post_btn = tk.Button(
            self.content_frame,
            text="Configure Post",
            command=lambda: main_window.load_content("ConfigurePost")
        )
        configure_post_btn.pack()
        pass