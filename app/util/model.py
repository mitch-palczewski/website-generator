import json
import os
import re
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

class FileModel: 
    pass

class StringModel:
    def remove_prefix(string, prefix):
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
        try:
            with open(json_file_path, "r") as json_file:
                json_data = json.load(json_file)
        except:
            json_data = {}
        return json_data

    def write_json_file(json_file, data):
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)

class HtmlModel:
    def open_html(html_file_path:str) -> bs:
        with open(html_file_path, "r", encoding="utf-8") as file:
            html_file_soup = bs(file, "html.parser")
        if not html_file_soup:
            raise ValueError(f"Error: file not found {html_file_path}")   
        return html_file_soup

    def write_html_file(html_file_path:str, html:bs) -> None:
        html=html.prettify()
        with open(html_file_path, "w", encoding="utf-8") as file:
            file.write(str(html))
        pass