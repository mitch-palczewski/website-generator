import tkinter as tk


class Post(tk.Frame):
    def __init__(self, container, title, image, caption, span):
        super().__init__(container)
        main_frame = tk.Frame(self)
        main_frame.pack()
        footer = tk.Frame(self)
        footer.columnconfigure(0, weight=1)
        footer.columnconfigure(1, weight=1)
        footer.columnconfigure(2, weight=1)
        footer.pack(expand=True, fill= 'x')

        #MAIN_FRAME
        self.title_text = tk.Text(main_frame, height=3)
        self.title_text.pack()
        #self.image_lbl = tk.Label(main_frame, image=image)
        #self.image_lbl.pack()
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
        self.config(state="disabled")
        self.config(state="disabled")
        
    def on_save(self):
        pass

    def on_delete(self):
        pass