import os
import sys



CONFIG_JSON_PATH = "config\config.json"
HTML_VALIDATION_PATH = "config\html_validation.json"
POSTS_JSON_PATH = "posts.json"
MESSAGE_HTML = "html_components\communicate\message.html"
HTML_POST_FOLDER = "html_components\post"
HTML_HEADER_FOLDER = "html_components\header"
HTML_FOOTER_FOLDER = "html_components\footer"
HTML_WEBPAGE_PATH = "index.html"
ASSET_FOLDER_PATH = "assets"

from app.util.model import FileModel, JsonModel, HtmlModel

def get_app_root():
    if getattr(sys, 'frozen', False):
        app_root = os.path.dirname(sys.executable)
    else:
        app_root = os.path.dirname(os.path.abspath(__file__)) 
    return app_root

def get_parent_dir():
    app_root = get_app_root()
    app_parent_dir = os.path.dirname(app_root)
    return app_parent_dir

def get_bundled_dir():
    if getattr(sys, 'frozen', False):
        app_root = sys._MEIPASS
    else:
        app_root = os.path.abspath(".")
    return app_root

def get_resource_paths():
    app_root = get_app_root()
    app_parent_dir = get_parent_dir()
    bundled_dir = get_bundled_dir()

    config_folder = os.path.join(bundled_dir, "config")
    html_components_folder = os.path.join(app_parent_dir, "html_components")
    backup_index_html = HtmlModel.open_html(os.path.join(html_components_folder, "webpage", "index.html"))
    assets_folder = os.path.join(app_parent_dir, "assets")

    config_json_path = os.path.join(config_folder, "config.json")
    html_validation_path = os.path.join(bundled_dir, "config", "html_validation.json")
    posts_json_path = os.path.join(app_parent_dir, "posts.json")
    message_html = os.path.join(html_components_folder, "communicate", "message.html")
    html_post_folder = os.path.join(html_components_folder, "post")
    html_header_folder = os.path.join(html_components_folder, "header")
    html_footer_folder = os.path.join(html_components_folder, "footer")
    html_webpage = os.path.join(app_parent_dir, "index.html")


    JsonModel.make_json_file_if_new(posts_json_path, {})
    HtmlModel.make_html_file_if_new(html_webpage, backup_index_html)
    FileModel.make_folder_if_new(html_components_folder)
    FileModel.make_folder_if_new(html_post_folder)
    FileModel.make_folder_if_new(html_header_folder)
    FileModel.make_folder_if_new(html_footer_folder)
    FileModel.make_folder_if_new(assets_folder)

    resource_paths = {
        "config_json": config_json_path,
        "html_validation": html_validation_path,
        "posts_json": posts_json_path,
        "message_html": message_html,
        "html_post_folder": html_post_folder,
        "html_header_folder": html_header_folder,
        "html_footer_folder": html_footer_folder,
        "html_webpage": html_webpage,
        "assets_folder": "assets"
    }

    return resource_paths







@staticmethod
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)





