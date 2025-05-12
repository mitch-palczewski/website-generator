import tkinter as tk
import re
from bs4 import BeautifulSoup as bs
from tkinter import font, ttk
from tkinter.messagebox import showinfo, askyesno
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from util.model_controller import Controller
from config import CONFIG_JSON_PATH
from gui.components.text_field import TextField

class GeneralConfiguration(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        #GROUPER FRAMES
        main_frame = tk.Frame(self, bg="red")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.pack(fill='both')

        left_frame = tk.Frame(main_frame,bg="yellow")
        left_frame.grid(column=0, row=0, sticky=tk.NSEW)
        right_frame = tk.Frame(main_frame )
        right_frame.grid(column=1, row=0, sticky=tk.NSEW)

        messaging_frame = ConfigureMessaging(left_frame)
        messaging_frame.pack()
        
        





class ConfigureMessaging(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        FONT_SM = font.Font(family="Helvetica", size=10, weight="bold")
        FONT_MD = font.Font(family="Helvetica", size=15, weight="bold")
        FONT_LG = font.Font(family="Helvetica", size=15, weight="bold")
        self.enable_messaging_btn = tk.Button(self, text="Enable Messaging", command=self.enable_messaging, font=FONT_LG)
        self.disable_messaging_btn = tk.Button(self, text="Disable Messaging", command=self.disable_messaging, font=FONT_LG)
        
        #ENABLED MESSING FRAME
        self.body = tk.Frame(self)
        self.body.columnconfigure(0,weight=1)
        self.body.columnconfigure(1,weight=1)
        self.body.columnconfigure(2,weight=1)
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
        self.disable_messaging_btn.pack(pady=10)
        self.body.pack()
        
    def disable_messaging(self):
        self.disable_messaging_btn.pack_forget()
        self.body.pack_forget()
        self.enable_messaging_btn.pack(pady=10)

    def edit(self):
        self.edit_btn.pack_forget()
        self.update_btn.grid(column=1, row=1, sticky=tk.EW, padx=5)
        self.cancel_btn.grid(column=2, row=1, sticky=tk.EW, padx=5)
        self.text_field.config(state="normal")

    def update(self):
        new_email = self.text_field.get()
        if askyesno(title="Change Email", message=f"Are you sure you want to replace {self.email} with {new_email}"):
            Controller.update_base_link(new_email)
        self.update_btn.grid_forget()
        self.cancel_btn.grid_forget()
        self.edit_btn.grid(column=1, row=1, padx=5, sticky=tk.EW)  
        self.text_field.config(state="disabled")
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
        
   


class EditMessaging(tk.Frame):
    def __init__(self, container, config_data):
        super().__init__(container)
        self.config_data = config_data

        #Grouper Frame
        self.body = tk.Frame(container)
        self.body.columnconfigure(0,weight=1)
        self.body.columnconfigure(1, weight=1)
        self.body.columnconfigure(2, weight=1)
        self.body.pack()

        self.email_lbl = tk.Label(self.body, text="Email: ")
        self.email_lbl.grid(column=0, row=0)

        self.email_field = TextField(self.body,1)
        self.email_field.grid(column=1,row=0)
        self.init_email_field()

        self.update_btn = tk.Button(self.body, text= "Update", command=self.update_email)
        self.update_btn.grid(column=2, row=0)


    
    def init_email_field(self):
        email = self.config_data["email"]
        if email:
            self.email_field.set_text(email)
        pass

    def update_email(self):
        new_email = self.email_field.get_text()
        if is_email(new_email):
            EmailValidation(self, new_email)
        elif is_hashed_email(new_email):
            pass
        else:
            showinfo(title="Error", message="Error input email or hashed email.")
        pass

class EmailValidation():
    def __init__(self, master, new_email):
        new_window = tk.Toplevel(master)
        new_window.title("New Window")
        new_window.geometry("300x600")
        label = tk.Label(new_window, text=f"You entered: {new_email}. \n Activate Your Account \n You will have recieved a email from FormSubmit. \"Action Required: Activate FormSubmit\" \n Replace Email with radom-like string and update.")
        label.pack(padx=20, pady=20)
        new_window.grab_set()
        

def is_email(string:str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, string))

def is_hashed_email(string:str) -> bool:
    hashed = False
    pattern = r'[a-zA-Z0-9]'
    if (re.match(pattern, string) and len(string) > 30 and len(string) < 34):
        hashed = True
    return hashed