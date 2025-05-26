import json
import os
import re
import shutil
import sys
import tkinter as tk
from tkinter import filedialog
from urllib.parse import quote
from bs4 import BeautifulSoup as bs

class Model:
     def encode_path(path:str):
        """
        Encodes a path for URL use
        """
        segments = path.split('/')
        encoded_segments = [quote(segment, safe="") for segment in segments]
        encoded_path = "/".join(encoded_segments)
        return encoded_path
     
     def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

class StringModel:
    def remove_prefix(string:str, prefix:str):
        if string.startswith(prefix):
            return string[len(prefix):] 
        return string

    def is_email(string:str) -> bool:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, string))

    def is_hashed_email(string:str) -> bool:
        hashed = False
        pattern = r'[a-zA-Z0-9]'
        if (re.match(pattern, string) and len(string) > 15):
            hashed = True
        return hashed

            
    

class JsonModel:
    def open_json(json_file_path:str):
        json_file_path = Model.resource_path(json_file_path)
        try:
            with open(json_file_path, "r") as json_file:
                json_data = json.load(json_file)
        except:
            json_data = {}
        return json_data

    def write_json_file(json_file_path, data):
        json_file_path = Model.resource_path(json_file_path)
        with open(json_file_path, "w") as file:
            json.dump(data, file, indent=4)

class HtmlModel:
    def open_html(html_file_path:str) -> bs:
        html_file_path = Model.resource_path(html_file_path)
        with open(html_file_path, "r", encoding="utf-8") as file:
            html_file_soup = bs(file, "html.parser")
        if not html_file_soup:
            raise ValueError(f"Error: file not found {html_file_path}")   
        return html_file_soup

    def write_html_file(html_file_path:str, html:bs) -> None:
        html_file_path = Model.resource_path(html_file_path)
        html=html.prettify()
        with open(html_file_path, "w", encoding="utf-8") as file:
            file.write(str(html))
        pass

    def format_html(html) -> str:
        if type(html) != bs:
            html = bs(html, "html.parser")
        html=html.prettify()
        return html
    
    def save_html_file(html, inital_directory, type):
        file_path = filedialog.asksaveasfilename(
            initialdir=inital_directory,
            defaultextension=".html", 
            filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")],
            title=f"Save {type} HTML File As"
        )
        if file_path:
            with open(file_path, 'w') as file:
                file.write(html)
            print(f"File saved to: {file_path}")
        return file_path

class TkModel:
    def clear_frame(frame:tk.Frame):
        for widget in frame.winfo_children():
            widget.destroy()

class FileModel:
    def move_media_to_folder(media:str, folder_path:str) -> str:
        folder_path = Model.resource_path(folder_path)
        shutil.copy(media, folder_path)
        file_name = os.path.basename(media)
        new_path = os.path.join(folder_path, file_name)
        return new_path