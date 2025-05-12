import tkinter as tk
import re
from bs4 import BeautifulSoup as bs
from tkinter.messagebox import showinfo, askokcancel
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from util.model import Model
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
        left_frame = tk.Frame(main_frame )
        left_frame.grid(column=0, row=0, sticky=tk.NSEW)
        
        messaging_frame = ConfigureMessaging(left_frame)
        messaging_frame.pack(pady=10)
        
        


class ConfigureMessaging(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.config_data = Model.open_json(CONFIG_JSON_PATH)
        self.messaging = self.config_data["post_messaging"]

        self.body = tk.Frame(self)
        self.body.pack()

        self.messaging_toggle = tk.Button(self.body, command=self.toggle_message)
        self.messaging_toggle.pack()

        self.edit_messaging = None

        self.set_messaging_toggle()
    
    def toggle_message(self):
        if self.messaging:
            self.messaging = False
        else: 
            self.messaging = True
        self.config_data["post_messaging"] = self.messaging
        Model.write_json_file(CONFIG_JSON_PATH, self.config_data)
        self.set_messaging_toggle()


    def set_messaging_toggle(self):
        if self.messaging:
            self.messaging_toggle.config(text="Disable Messaging",
                                         bg="#72c5c0")
            self.edit_messaging_group = tk.Frame(self.body)
            self.edit_messaging_group.pack()
            self.edit_messaging = EditMessaging(self.edit_messaging_group, self.config_data)
            self.edit_messaging.pack()
        else: 
            self.messaging_toggle.config(text="Enable Messaging",
                                         bg="grey")
            if self.edit_messaging:
                self.edit_messaging_group.pack_forget()

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