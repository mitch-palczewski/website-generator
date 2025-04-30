import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from gui.subwindows import Landing

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Website Generator")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width-200}x{screen_height-200}+5+5")
        self.resizable(True, True)
        self.config(bg="blue")

        self.content_frame = tk.Frame(self, bg="green")
        self.content_frame.pack(fill='both', expand= True,padx=10, pady=10)

       

        


    
    def load_content(self, content:tk.Frame):
        self.content_frame.pack_forget()
        content(self.content_frame)
        self.content_frame.pack(fill='both', expand= True,padx=10, pady=10)
        pass
