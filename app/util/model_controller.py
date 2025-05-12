import json
import requests
from urllib.parse import quote
CONFIG_JSON_PATH = "app\config\config.json"
POSTS_JSON_PATH = "posts.json"

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
        #UPDATE posts.json

        posts_data:dict = Controller.get_posts_data()
        for post_id, post in posts_data.items():
            base_link = post["base_link"]
            media_link = post["media_link"]
            media = Model.remove_prefix(media_link, base_link)
            new_media_link = Controller.format_media_link(new_base_link, media)
            post["media_link"] = new_media_link
            post["base_link"] = new_base_link
        Model.write_json_file(POSTS_JSON_PATH, posts_data)

    def format_media_link(base_link:str, media_path:str) -> str:
        if not base_link.endswith("/"):
            base_link = base_link + "/" 
        media_path = quote(media_path, safe=":/?&=") 
        media_link:str = base_link + media_path
        return media_link
