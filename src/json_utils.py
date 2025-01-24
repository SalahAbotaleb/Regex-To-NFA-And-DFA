import json


class JsonUtils:
    def save_dict_to_file(data: dict, file_name: str) -> None:
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

    def get_dict_from_file(file_name: str) -> dict:
        with open(file_name, "r") as file:
            return json.load(file)
