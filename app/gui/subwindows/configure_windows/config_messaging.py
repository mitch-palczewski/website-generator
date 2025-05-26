import tkinter as tk
from tkinter import font, ttk
from tkinter.messagebox import askyesno
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app.util.model_controller import Controller, HtmlController
from app.util.controller import JsonController
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]

LBL_TEXT = (
    "This is an Eperimental feature that utilizes"
    "\nhttps://formsubmit.co/ infrustructure."
    "\n\n **WARNING** This features may expose your Email "
    "\n\nTo Activate your formsubmit account send yourself a message, \nin your email "
    "(could be in spam) activate your \naccount and repalce your email with the provided \n"
    "hashed value.\nSomething like 8e2398w9435df1f75b6fc3fb137d2c63")


class ConfigMessaging(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        FONT_MD = font.Font(family="Helvetica", size=14, weight="bold")
        #GROUPER FRAMES
        main_frame = tk.Frame(self, bg=C1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.pack(fill='both', expand=True)

        left_frame = tk.Frame(main_frame,bg=C1)
        left_frame.grid(column=0, row=0, sticky=tk.NSEW)
        right_frame = tk.Frame(main_frame, bg=C1 )
        right_frame.grid(column=1, row=0, sticky=tk.NSEW)

        messaging_frame = MessagingSettings(left_frame)
        messaging_frame.pack()

        lbl = tk.Label(right_frame, bg="white",justify='left',text=LBL_TEXT, font=FONT_MD)
        lbl.pack( fill='x', padx=10, pady=10)
        
        
class MessagingSettings(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config(bg=C1)
        FONT_SM = font.Font(family="Helvetica", size=10, weight="bold")
        FONT_MD = font.Font(family="Helvetica", size=15, weight="bold")
        FONT_LG = font.Font(family="Helvetica", size=15, weight="bold")
        self.enable_messaging_btn = tk.Button(self, text="Enable Messaging", command=self.enable_messaging, font=FONT_LG)
        self.disable_messaging_btn = tk.Button(self, text="Disable Messaging", command=self.disable_messaging, font=FONT_LG)
        
        #ENABLED MESSEGING FRAME
        self.body = tk.Frame(self, bg=C1)
        self.body.columnconfigure(0,weight=1)
        self.body.columnconfigure(1,weight=1)
        self.body.columnconfigure(2,weight=1)
        self.body.pack()
        lbl = tk.Label(self.body, text="Email:   ", font=FONT_MD)
        lbl.grid(column=0,row=0)
        self.text_field = ttk.Entry(
            master=self.body, 
            font=FONT_MD,
            width= 38,
            state="disabled")
        self.text_field.grid(column=1, row=0, columnspan=2, pady=5)
        self.edit_btn = tk.Button(self.body, text="Edit", font=FONT_SM, command=self.edit)
        self.edit_btn.grid(column=1, row=1, padx=5, sticky=tk.EW)  
        self.update_btn = tk.Button(self.body, text="Update", font=FONT_SM, command=self.update)
        self.cancel_btn = tk.Button(self.body, text="Cancel", font=FONT_SM, command=self.cancel)

        #INIT
        self.config_data = Controller.get_config_data()
        if self.config_data["post_messaging"]:
            self.enable_messaging()
        else:
            self.disable_messaging()

    def enable_messaging(self):
        self.load_config_email()
        self.enable_messaging_btn.pack_forget()
        self.disable_messaging_btn.pack(pady=10, padx=10)
        self.body.pack()
        HtmlController.insert_message_popup()
        HtmlController.unhide_message_btn()
        
    def disable_messaging(self):
        self.disable_messaging_btn.pack_forget()
        self.body.pack_forget()
        self.enable_messaging_btn.pack(pady=10, padx=10)
        HtmlController.delete_message_popup()
        HtmlController.hide_message_btn()

    def edit(self):
        self.edit_btn.pack_forget()
        self.update_btn.grid(column=1, row=1, sticky=tk.EW, padx=5)
        self.cancel_btn.grid(column=2, row=1, sticky=tk.EW, padx=5)
        self.text_field.config(state="normal")

    def update(self):
        new_email = self.text_field.get()
        self.config_data = Controller.get_config_data()
        self.email = self.config_data["email"]
        self.update_btn.grid_forget()
        self.cancel_btn.grid_forget()
        self.edit_btn.grid(column=1, row=1, padx=5, sticky=tk.EW)  
        self.text_field.config(state="disabled")
        if new_email == self.email:
            return
        if askyesno(title="Change Email", message=f"Are you sure you want to replace {self.email} with {new_email}"):
            Controller.update_email(new_email)
            HtmlController.update_email()
        self.load_config_email()

    def cancel(self):
        self.update_btn.grid_forget()
        self.cancel_btn.grid_forget()
        self.edit_btn.grid(column=1, row=1, padx=5, sticky=tk.EW)  
        self.text_field.config(state="disabled")
        self.load_config_email()
    
    def load_config_email(self):
        self.config_data = Controller.get_config_data()
        self.email = self.config_data["email"]
        self.text_field.config(state="normal")
        self.text_field.delete(0, tk.END)
        self.text_field.insert(0, self.email)
        self.text_field.config(state="disabled")
