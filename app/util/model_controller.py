import json
import re
from urllib.parse import quote
from bs4 import BeautifulSoup as bs
CONFIG_JSON_PATH = "app\config\config.json"
POSTS_JSON_PATH = "posts.json"
MESSAGE_HTML = "html_components\communicate\message.html"
HTML_FILE_PATH = "index.html"

class Model:
    #JSON
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
    
    #STRING
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
    
   
    

class Controller: 
    def get_config_data() -> dict:
        config_data:dict = Model.open_json(CONFIG_JSON_PATH)
        return config_data
    
    def get_posts_data() -> dict:
        posts_data:dict = Model.open_json(POSTS_JSON_PATH)
        return posts_data
    
    def update_base_link(new_base_link:str):
        config_data = Controller.get_config_data()
        if new_base_link == config_data["base_link"]:
            return
        config_data["base_link"] = new_base_link
        Model.write_json_file(CONFIG_JSON_PATH, config_data)
        posts_data:dict = Controller.get_posts_data()
        for post_id, post in posts_data.items():
            base_link = post["base_link"]
            media_link = post["media_link"]
            media = Model.remove_prefix(media_link, base_link)
            new_media_link = Controller.format_media_link(new_base_link, media)
            post["media_link"] = new_media_link
            post["base_link"] = new_base_link
        Model.write_json_file(POSTS_JSON_PATH, posts_data)
    
    def update_email(new_email):
        config_data = Controller.get_config_data()
        if new_email == config_data["email"]:
            return
        if Model.is_email(new_email):
            config_data["email"] = new_email
            Model.write_json_file(CONFIG_JSON_PATH, config_data)
            return
        if Model.is_hashed_email(new_email):
            config_data["email"] = new_email
            Model.write_json_file(CONFIG_JSON_PATH, config_data)
            return
        

    def format_media_link(base_link:str, media_path:str) -> str:
        if not base_link.endswith("/"):
            base_link = base_link + "/" 
        media_path = quote(media_path, safe=":/?&=") 
        media_link:str = base_link + media_path
        return media_link

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

class HtmlController:

    #MESSAGING
    def insert_message_popup():
        config_data = Controller.get_config_data()
        email = config_data["email"]
        if not email:
            print("Messaging HTML will not be inserted untill an Email is attached")
            return
        html_webpage:bs = HtmlModel.open_html(HTML_FILE_PATH)
        if not html_webpage:
            raise ValueError("Error: HTML webpage not found in file system.")
        message_popup_tag:bs = html_webpage.find("div", id="message_popup")
        if message_popup_tag:
            return
        message_html:bs = HtmlModel.open_html(MESSAGE_HTML)
        if not message_html:
            raise ValueError("Error: message html not found in file system.")
        footer_tag:bs = html_webpage.find("footer")
        if not footer_tag:
            raise ValueError("Error: No element with id 'footer' found.")
        footer_tag.insert_after(message_html)
        HtmlModel.write_html_file(HTML_FILE_PATH, html_webpage)
    
    def delete_message_popup():
        html_webpage:bs = HtmlModel.open_html(HTML_FILE_PATH)
        if not html_webpage:
            raise ValueError("Error: HTML webpage not found in file system.")
        message_popup_tag:bs = html_webpage.find("div", id="message_popup")
        if message_popup_tag:  
            message_popup_tag.decompose()
            HtmlModel.write_html_file(HTML_FILE_PATH, html_webpage)
    
    def hide_message_btn():
        html_webpage:bs = HtmlModel.open_html(HTML_FILE_PATH)
        if not html_webpage:
            raise ValueError("Error: HTML webpage not found in file system.")
        message_btns = html_webpage.find_all("button", id="message_btn")
        for message_btn in message_btns:
            class_list = message_btn.get("class", [])
            class_list.append(" hidden")
            message_btn["class"] = class_list
        HtmlModel.write_html_file(HTML_FILE_PATH, html_webpage)
    
    def unhide_message_btn():
        html_webpage:bs = HtmlModel.open_html(HTML_FILE_PATH)
        if not html_webpage:
            raise ValueError("Error: HTML webpage not found in file system.")
        message_btns = html_webpage.find_all("button", id="message_btn")
        for message_btn in message_btns:
            class_list = message_btn.get("class", [])
            if (len(class_list) != 0 and "hidden" in class_list):
                class_list = class_list.remove("hidden")
                message_btn["class"] = class_list
        HtmlModel.write_html_file(HTML_FILE_PATH, html_webpage)
    
    def config_message_email():
        config_data = Controller.get_config_data()
        email = config_data["email"]
        if not email:
            print("Email = None")
            return
        message_html:bs = HtmlModel.open_html(MESSAGE_HTML)
        if not message_html:
            raise ValueError("Error: message html not found in file system.")
        message_form_tag = message_html.find("form", id="message_form")
        if not message_form_tag:
            raise ValueError("Error: No element with id 'message_form' found.")
        form_submit_link = "https://formsubmit.co/" + email
        message_form_tag["action"] = form_submit_link
        HtmlModel.write_html_file(MESSAGE_HTML, message_html)
