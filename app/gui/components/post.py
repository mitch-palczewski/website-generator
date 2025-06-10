import tkinter as tk
from tkinter.messagebox import askyesno
from bs4 import BeautifulSoup as bs 
import os
from PIL import Image, ImageTk


from app.util.controller import HtmlController, PostController, JsonController, Controller

colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]

class Post(tk.Frame):
    def __init__(self, container, id, title, image, caption, span, parent):
        super().__init__(container)
        self.title = title 
        self.caption = caption 
        self.id = id
        self.parent = parent
        self.config(border=2, relief="solid", bg=C1)
        main_frame = tk.Frame(self, bg=C1)
        main_frame.pack(expand=True, fill='both')
        footer = tk.Frame(self, bg=C1)
        footer.columnconfigure(0, weight=1)
        footer.columnconfigure(1, weight=1)
        footer.columnconfigure(2, weight=1)
        footer.pack(expand=True, fill= 'x', padx=5, pady=5)

        #MAIN_FRAME
        self.title_text = tk.Text(main_frame, height=1, width=40*span)
        self.title_text.pack(expand=True, padx=5, pady=5)
        if image and os.path.exists(image):
            tk_image = open_image_as_tk_image(image, 300)
            self.image_lbl = tk.Label(main_frame, image=tk_image)
            self.image_reference = tk_image  # Keep a reference!
            self.image_lbl.pack(pady=10, expand=True)
        self.caption_text = tk.Text(main_frame, height= 8, width=40*span)
        self.caption_text.pack(expand=True, padx=5, pady=5)

        #FOOTER
        self.edit_btn = tk.Button(footer, command=self.on_edit, text="Edit", bg=C4)
        self.edit_btn.grid(column=0, row=0)

        self.cancel_btn = tk.Button(footer, command=self.on_cancel, text="Cancel", bg=C4)
        self.save_btn = tk.Button(footer, command=self.on_save, text="Save", bg=C4)
        self.delete_btn = tk.Button(footer, command=self.on_delete, text="Delete", bg=C4)

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
        self.title_text.config(state="disabled")
        self.caption_text.config(state="disabled")
        
    def on_save(self):
        self.title = self.title_text.get("1.0", tk.END)
        self.caption = self.caption_text.get("1.0", tk.END)
        self.on_cancel()
        PostController.update_post(self.id, self.title, self.caption)
        Controller.push_to_git()

    def on_delete(self):
        answer = askyesno(f"Delete Post ID {self.id}", message="Deleting Post can not be undone \n confirm deletion")
        if answer:
            PostController.delete_post(self.id)
            self.parent.reset_scrollframe()

def replace_text(text_field: tk.Text, new_text:str):
    text_field.delete('1.0', tk.END)
    text_field.insert('1.0', chars=new_text)

def set_post_title(post:bs, title:str):
    title_tag = post.find("h1", attrs={"data-type":"title"})
    title_tag.text = title

def open_image_as_tk_image(image, max_height_width):
    pil_image = Image.open(image)
    if pil_image.height >= pil_image.width:
        aspect_ratio = pil_image.width / pil_image.height
        height = max_height_width
        width = int(max_height_width * aspect_ratio)
    else:
        aspect_ratio = pil_image.height / pil_image.width
        width = max_height_width 
        height = int(width * aspect_ratio)
    pil_image = pil_image.resize((width,height), Image.Resampling.NEAREST)
    tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image