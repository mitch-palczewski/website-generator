import json
import os
import re
from urllib.parse import quote
from bs4 import BeautifulSoup as bs
CONFIG_JSON_PATH = "app\config\config.json"
HTML_VALIDATION_PATH = "app\config\html_validation.json"
POSTS_JSON_PATH = "posts.json"
MESSAGE_HTML = "html_components\communicate\message.html"
HTML_POST_FOLDER = "html_components\post"
HTML_HEADER_FOLDER = "html_components\header"
HTML_FOOTER_FOLDER = "html_components\footer"
HTML_WEBPAGE_PATH = "index.html"
ASSET_FOLDER_PATH = "assets"

from util.model import Model, HtmlModel, StringModel, JsonModel
from tkinter.messagebox import showwarning
from tkinter import filedialog

class Controller:
    pass
    

class StringController:
    pass

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

    def get_html_validation() -> dict:
        html_validation = JsonModel.open_json(HTML_VALIDATION_PATH)
        return html_validation
        
    def set_config_data(key:str, data):
        config_data:dict = JsonController.get_config_data()
        if not key in config_data.keys():
            ValueError(f"Key: {key} not in config.json. Config Json Keys: {config_data.keys()}")
        config_data[key] = data
        JsonModel.write_json_file(CONFIG_JSON_PATH, config_data)

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


class HtmlController:
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
            HtmlModel.save_html_file(html, HTML_POST_FOLDER, component_type)
            return
        if component_type == "header":
            HtmlModel.save_html_file(html, HTML_HEADER_FOLDER, component_type)
            return
        if component_type == "footer":
            HtmlModel.save_html_file(html, HTML_FOOTER_FOLDER, component_type)
            return
    
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
        html_webpage:bs = HtmlModel.open_html(HTML_WEBPAGE_PATH)
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
        pass