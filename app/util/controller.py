from datetime import date
from bs4 import BeautifulSoup as bs
import os
import time
import json
import glob

CONFIG_JSON_PATH = "app\config\config.json"
HTML_VALIDATION_PATH = "app\config\html_validation.json"
POSTS_JSON_PATH = "posts.json"
MESSAGE_HTML = "html_components\communicate\message.html"
HTML_POST_FOLDER = "html_components\post"
HTML_HEADER_FOLDER = "html_components\header"
HTML_FOOTER_FOLDER = "html_components\footer"
HTML_WEBPAGE_PATH = "index.html"
ASSET_FOLDER_PATH = "assets"

from util.model import Model, HtmlModel, StringModel, JsonModel, FileModel
from util.serve_localhost import start_server
from tkinter.messagebox import showwarning, showinfo

class Controller:
    def get_todays_date()->str:
        unformatted_date:date = date.today()
        today_date: str = unformatted_date.strftime("%m-%d-%Y")
        return today_date
    
    def get_unique_id(dict_key_ids: list):
        highest_id = 0
        for id in dict_key_ids:
            id_int = int(id)
            if id_int > highest_id:
                highest_id = id_int
        new_id = highest_id + 1
        return f"{new_id:06d}" 
    
    def web_page_change():
        start_server()
    
class StringController:
    def format_media_link(base_link:str, media_path:str) -> str:
        """
        Encodes a media element for URL use
        """
        asset_folder_path_slash = ASSET_FOLDER_PATH
        if not asset_folder_path_slash.endswith("/"):
            asset_folder_path_slash += "/"
        if not base_link.endswith("/"):
            base_link = base_link + "/" 
        if media_path.startswith(ASSET_FOLDER_PATH):
            relative_path = media_path[len(asset_folder_path_slash):]
            encoded_relative_path = Model.encode_path(relative_path)
            return base_link + asset_folder_path_slash + encoded_relative_path
        else:
            encoded_relative_path = Model.encode_path(media_path)
            return base_link + encoded_relative_path
    
    def format_string_for_html(string:str):
        string = string.replace("\\", "\\\\")  
        string = string.replace("'", "\\'")
        return string

class JsonController:
    def get_posts_data() -> dict:
        posts_data:dict = JsonModel.open_json(POSTS_JSON_PATH)
        return posts_data
    
    def get_config_data(key:str = None) -> dict:
        """
        if key = None returns all data
        """
        config_data:dict = JsonModel.open_json(CONFIG_JSON_PATH)
        if not key:
            return config_data
        if not key in config_data.keys():
            ValueError(f"Key: {key} not in config.json. Config Json Keys: {config_data.keys()}")
        return config_data[key]
    
    def get_post_component_basename():
        """
        Retuns the basename of the post component in config.json
        """
        post_component_path = JsonController.get_config_data("post_component")
        post_component = os.path.basename(post_component_path)
        return post_component

    def get_html_validation() -> dict:
        html_validation = JsonModel.open_json(HTML_VALIDATION_PATH)
        return html_validation
    
    def set_post_component(path = None, basename=None):
        if not path and not basename:
            ValueError("Error need to set post_component by path or basename")
        if basename:
            path = FileController.get_post_component_path(basename)
        JsonController.set_config_data("post_component", path)
        
    def set_config_data(key:str, data):
        config_data:dict = JsonController.get_config_data()
        if not key in config_data.keys():
            ValueError(f"Key: {key} not in config.json. Config Json Keys: {config_data.keys()}")
        config_data[key] = data
        JsonModel.write_json_file(CONFIG_JSON_PATH, config_data)
    
    def append_posts_data(post: dict, post_id):
        posts_data = JsonController.get_posts_data()
        posts_data[post_id] = post
        JsonModel.write_json_file(POSTS_JSON_PATH, posts_data)

    def update_base_link(new_base_link:str):
        old_base_link = JsonController.get_config_data("base_link")
        if new_base_link == old_base_link:
            return
        JsonController.update_posts_base_link(new_base_link)
        JsonController.set_config_data(key="base_link", data = new_base_link)

    def update_posts_base_link(new_base_link:str):
        posts_data:dict = JsonController.get_posts_data()
        for post_id, post in posts_data.items():
            new_media_link = JsonController.update_media_link(post, new_base_link)
            post["media_link"] = new_media_link
            post["base_link"] = new_base_link
        JsonModel.write_json_file(POSTS_JSON_PATH, posts_data)
    
    def update_media_link(post:dict, new_base_link:str):
        """
        Replaces Base link in posts.json {"media_link"}
        """
        base_link:str = post["base_link"]
        media_link:str = post["media_link"]
        media:str = StringModel.remove_prefix(string=media_link, prefix=base_link)
        if media.startswith("/") and new_base_link.endswith("/"):
            media = media[1:]
        if not media.startswith("/") and not new_base_link.endswith("/"):
            new_base_link += "/"
        new_media_link = new_base_link + media
        return new_media_link
    
    def update_selected_post_component(post_component_path:str):
        config_data = JsonController.get_config_data()
        config_data["post_component"] = post_component_path
        JsonModel.write_json_file(CONFIG_JSON_PATH, config_data)

    def update_tab_title(new_tab_title:str):
        if new_tab_title == "":
            print("tab title cannot be null")
            return
        config_data = JsonController.get_config_data()
        config_data["tab_title"] = new_tab_title
        JsonModel.write_json_file(CONFIG_JSON_PATH, config_data)
        HtmlController.update_tab_title()

class HtmlController:
    def get_webpage_html()->bs:
        html_webpage:bs = HtmlModel.open_html(HTML_WEBPAGE_PATH)
        if not html_webpage:
            raise ValueError("Error: HTML webpage not found in file system.")
        return html_webpage
    
    def get_post_component()->bs:
        post_component_path = JsonController.get_config_data("post_component")
        post_html:bs = HtmlModel.open_html(post_component_path)
        return post_html
    
    def set_webpage_html(html):
        HtmlModel.write_html_file(HTML_WEBPAGE_PATH, html)

    def update_component(component_type:str, component_path:str):
        """
        component_type: "post", "header", "footer"
        """
        if component_type == "post":
            JsonController.update_selected_post_component(component_path)
            return
        if component_type == "header":
            HtmlController.update_header(component_path)
            return
        if component_type == "footer":
            HtmlController.update_footer(component_path)
            return
        raise ValueError(f"Invalid component_type {component_type}")

    def update_header(component_path):
        html_webpage:bs = HtmlController.get_webpage_html()
        new_header:bs = HtmlModel.open_html(component_path)
        new_header_tag = new_header.find("header")
        webpage_header_tag = html_webpage.find("header")
        if not webpage_header_tag:
            ValueError("Error: No <header> tag found in webpage")
        if not new_header_tag:
            webpage_header_tag.clear()
            webpage_header_tag.append(new_header)
        else:
            webpage_header_tag.replace_with(new_header)
        HtmlModel.write_html_file(HTML_WEBPAGE_PATH, html_webpage)
    
    def update_footer(component_path):
        html_webpage:bs = HtmlModel.open_html(HTML_WEBPAGE_PATH)
        new_footer:bs = HtmlModel.open_html(component_path)
        new_footer_tag = new_footer.find("footer")
        webpage_footer_tag = html_webpage.find("footer")
        if not webpage_footer_tag:
            ValueError("Error: No <header> tag found in webpage")
        if not new_footer_tag:
            webpage_footer_tag.clear()
            webpage_footer_tag.append(new_footer)
        else:
            webpage_footer_tag.replace_with(new_footer)
        HtmlModel.write_html_file(HTML_WEBPAGE_PATH, html_webpage)

    def update_tab_title():
        config_data = JsonController.get_config_data()
        tab_title = config_data["tab_title"]
        html_webpage:bs = HtmlModel.open_html(HTML_WEBPAGE_PATH)
        if not html_webpage:
            raise ValueError("Error: HTML webpage not found in file system.")
        title_tag:bs = html_webpage.find("title")
        if title_tag:
            title_tag.clear()
            title_tag.insert(0, tab_title)
        HtmlModel.write_html_file(HTML_WEBPAGE_PATH, html_webpage)
    
    def update_bg_color(color):
        html_webpage:bs = HtmlModel.open_html(HTML_WEBPAGE_PATH)
        main_tag:bs = html_webpage.find("main")
        classes = main_tag.get("class", [])
        for index, class_item in enumerate(classes):
            if class_item.startswith("bg-"):
                classes[index] = ""
        classes.append(f"bg-[{color}]")
        main_tag["class"] = classes
        HtmlController.set_webpage_html(html_webpage)
        

    def validate_html(type:str, html:str):
        valid = True
        invalid_ids = []
        html_validation = JsonController.get_html_validation()
        required_ids = html_validation[type]
        for id in required_ids:
            index = html.find(id)
            if index == -1:
                valid = False
                invalid_ids.append(id)
        if not valid:
            showwarning(title="Invalid HTML", message=f"Invalid HTML. \n Missing ids {invalid_ids}")
        return valid
    
    def save_component_file(html, component_type):
        if component_type == "post":
            file_path = HtmlModel.save_html_file(html, HTML_POST_FOLDER, component_type)
            return file_path
        if component_type == "header":
            file_path = HtmlModel.save_html_file(html, HTML_HEADER_FOLDER, component_type)
            return file_path
        if component_type == "footer":
            file_path = HtmlModel.save_html_file(html, HTML_FOOTER_FOLDER, component_type)
            return file_path
        
class FileController:
    def get_post_component_basenames()->list:
        basenames = os.listdir(HTML_POST_FOLDER)
        return basenames
    
    def get_post_component_paths() -> list:
        basenames = FileController.get_post_component_basenames()
        paths:list = []
        for basename in basenames:
            path = os.path.join(HTML_POST_FOLDER, basename)
            paths.append(path)
        return paths
    
    def get_post_component_path(basename:str):
        path:str = os.path.join(HTML_POST_FOLDER, basename)
        return path

    def add_media_to_assets_folder(file_paths:list):
        """
        Accepts a list of file paths 
        Returns a list of new paths local to the project
        """
        media_paths = []
        for element in file_paths:
            new_path:str = FileModel.move_media_to_folder(element, ASSET_FOLDER_PATH)
            media_paths.append(new_path)
        return media_paths

    