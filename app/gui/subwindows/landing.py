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
        BUTTON_FONT = font.Font(family="Helvetica", size=20, weight="bold")

        #GROUPER
        self.body = tk.Frame(self, bg="red")
        self.body.pack( expand=True,padx=10, pady=10)
        
        #BODY
        new_post_btn = tk.Button(
            self.body, 
            text="New Post", 
            command=lambda: main_window.load_content("NewPost"),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font= BUTTON_FONT
        )
        new_post_btn.pack(padx=BUTTON_PADDING, pady=BUTTON_PADDING)

        configure_post_btn = tk.Button(
            self.body,
            text="Configure Website",
            command=lambda: main_window.load_content("ConfigureWebsite"),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font=BUTTON_FONT
        )
        configure_post_btn.pack(padx=BUTTON_PADDING, pady=BUTTON_PADDING)

        edit_post_btn = tk.Button(
            self.body,
            text="Edit Posts",
            command=lambda: main_window.load_content("EditPosts"),
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font=BUTTON_FONT
        )
        edit_post_btn.pack(padx=BUTTON_PADDING, pady=BUTTON_PADDING)

        base_link = BaseLink(self.body)
        base_link.pack()
        pass

class BaseLink(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        FONT = font.Font(family="Helvetica", size=20, weight="bold")
        self.base_link_var = tk.StringVar()

        #GROUPER
        self.body = tk.Frame(self)
        self.body.columnconfigure(0,weight=1)
        self.body.columnconfigure(1, weight=1)
        self.body.columnconfigure(2, weight=1)
        self.body.columnconfigure(3, weight=1)
        self.body.pack()

        #BODY
        self.lbl = tk.Label(self.body, text="Base Link:", font=FONT)
        self.lbl.grid(column=0, row=0)

        self.text_field = tk.Text(
            master=self.body, 
            width= 30,
            height= 1,
            wrap="word",
            font=FONT,
            padx=2,
            pady=2,
            state="disabled")
        self.text_field.grid(column=1,row=0)

        self.edit_btn = tk.Button(self.body, text="Edit", font=FONT,command= self.edit)
        self.edit_btn.grid(column=2,row=0)

        self.update_btn = tk.Button(self.body, text="Update", font=FONT, command=self.update)
        self.cancel_btn = tk.Button(self.body, text="Cancel", font=FONT, command=self.cancel)

    def edit(self):
        self.edit_btn.grid_forget()
        self.update_btn.grid(column=2, row=0)
        self.cancel_btn.grid(column=3, row=0)
        pass


    def update(self):
        self.update_btn.grid_forget()
        self.cancel_btn.grid_forget()
        self.edit_btn.grid(column=2, row=0)
        pass

    def cancel(self):
        self.update_btn.grid_forget()
        self.cancel_btn.grid_forget()
        self.edit_btn.grid(column=2, row=0)





    def switch_edit_update(self):
        if self.btn_state == "edit":
            self.btn_state == "update"
        elif self.btn_state == "update":
            #update json
            self.btn_state == "edit"
        self.edit_update()
    
    def edit_update(self):
        if self.btn_state == "edit":
            self.text_field.config(state="disabled")
            self.edit_update_btn.config(text="Edit")
            self.cancel_btn.grid_forget()
            pass
        elif self.btn_state == "update":
            self.text_field.config(state="normal")
            self.edit_update_btn.config(text="Update")
            self.cancel_btn.grid(column=3,row=0)
            pass
