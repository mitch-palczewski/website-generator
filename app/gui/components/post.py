import tkinter as tk
from bs4 import BeautifulSoup as bs 
import os
from PIL import Image, ImageTk


from app.util.controller import HtmlController

class Post(tk.Frame):
    def __init__(self, container, id, title, image, caption, span):
        super().__init__(container)
        self.title = title 
        self.caption = caption 
        main_frame = tk.Frame(self)
        main_frame.pack()
        footer = tk.Frame(self)
        footer.columnconfigure(0, weight=1)
        footer.columnconfigure(1, weight=1)
        footer.columnconfigure(2, weight=1)
        footer.pack(expand=True, fill= 'x')

        #MAIN_FRAME
        self.title_text = tk.Text(main_frame, height=1)
        self.title_text.pack()
        if image and os.path.exists(image):
            tk_image = open_image_as_tk_image(image, 300)
            self.image_lbl = tk.Label(main_frame, image=tk_image)
            self.image_reference = tk_image  # Keep a reference!
            self.image_lbl.pack()
        self.caption_text = tk.Text(main_frame, height= 8)
        self.caption_text.pack()

        #FOOTER
        #Edit -> cancel save delete 
        self.edit_btn = tk.Button(footer, command=self.on_edit, text="Edit")
        self.edit_btn.grid(column=0, row=0)

        self.cancel_btn = tk.Button(footer, command=self.on_cancel, text="Cancel")
        self.save_btn = tk.Button(footer, command=self.on_save, text="Save")
        self.delete_btn = tk.Button(footer, command=self.on_delete, text="Delete")

        self.init_post(title, caption, span)

    def init_post(self, title, caption, span):
        self.title_text.insert(index='1.0', chars= title)
        self.title_text.config(state="disabled")
        self.caption_text.insert(index='1.0', chars=caption)
        self.caption_text.config(state="disabled")

    def on_edit(self):
        self.edit_btn.grid_forget()
        self.cancel_btn.grid(column=0, row=0)
        self.save_btn.grid(column=1, row=0)
        self.delete_btn.grid(column=2, row=0)
        self.title_text.config(state="normal")
        self.caption_text.config(state="normal")
        
    def on_cancel(self):
        self.cancel_btn.grid_forget()
        self.save_btn.grid_forget()
        self.delete_btn.grid_forget()
        self.edit_btn.grid(column=0, row=0)
        replace_text(self.title_text, self.title)
        replace_text(self.caption_text, self.caption)
        self.config(state="disabled")
        self.config(state="disabled")
        
    def on_save(self):
        self.title = self.title_text.get("1.0", tk.END)
        self.caption = self.caption_text.get("1.0", tk.END)
        

    def on_delete(self):
        pass

def replace_text(text_field: tk.Text, new_text:str):
    text_field.delete('1.0', tk.END)
    text_field.insert('1.0', chars=new_text)

def get_post_by_id(id):
    webpage_html = HtmlController.get_webpage_html()
    post = webpage_html.find("div", attrs={"data-post_id": id})
    if not post:
        print(f"WARNING could not get post with id = {id}")
    return post

def set_post_title(post:bs, title:str):
    title_tag = post.find("h1", attrs={"data-type":"title"})
    title_tag.text = title

def open_image_as_tk_image(image, height):
    pil_image = Image.open(image)
    aspect_ratio = pil_image.width / pil_image.height
    width = int(height * aspect_ratio)
    pil_image = pil_image.resize((width,height), Image.Resampling.NEAREST)
    tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image