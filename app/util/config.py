import os

CONFIG_JSON_PATH = "app/config/config.json"
MESSAGE_HTML = "html_components/communicate/message.html"
ASSET_FOLDER_PATH = "assets"
HTML_FILE_PATH = "index.html"
POSTS_JSON_PATH = "posts.json"

def get_project_path():
    project_path = os.path.dirname(os.getcwd())
    return project_path

def get_app_path():
    app_path = os.path.dirname(os.path.abspath(__file__))
    return app_path