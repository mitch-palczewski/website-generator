import tkinter as tk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass



class TextField(tk.Frame):
    def __init__(self, container, field_height):
        super().__init__(container)
        self.main_frame = tk.Frame(self, bg="blue")
        self.main_frame.pack(padx=10, pady=10)
        self.text_var = tk.StringVar()
        self.text_field = tk.Text(
            master=self.main_frame, 
            width=50,
            height= field_height,
            wrap="word",
            padx=10,
            pady=4)
        self.text_field.pack()

    def get_text(self):
        raw_text = self.text_field.get("1.0", tk.END)
        return raw_text
    
    def set_text(self, text:str):
        self.text_field.insert("1.0", text)