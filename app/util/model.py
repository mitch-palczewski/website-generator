import json
CONFIG_JSON_PATH = "app\config\config.json"

class Model:
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