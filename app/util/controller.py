import json
import os
import re
from urllib.parse import quote
from bs4 import BeautifulSoup as bs
CONFIG_JSON_PATH = "app\config\config.json"
POSTS_JSON_PATH = "posts.json"
MESSAGE_HTML = "html_components\communicate\message.html"
HTML_FILE_PATH = "index.html"
ASSET_FOLDER_PATH = "assets"

from util.model import Model, HtmlModel, StringModel, JsonModel

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
    
    def update_media_link(post, new_base_link:str):
        base_link:str = post["base_link"]
        media_link:str = post["media_link"]
        media:str = StringModel.remove_prefix(string=media_link, prefix=base_link)
        if media.startswith("/") and new_base_link.endswith("/"):
            media = media[1:]
        if not media.startswith("/") and not new_base_link.endswith("/"):
            new_base_link += "/"
        new_media_link = new_base_link + media
        return new_media_link


class HtmlController:

    pass