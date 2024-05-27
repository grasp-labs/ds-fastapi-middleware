import os
import pathlib
import yaml


def load_config():
    root = pathlib.Path(__file__).parents[2]
    file_name = os.getenv("DS_CONFIG_FILE", "default_config.yml")
    file_path = os.path.join(root, file_name)
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


config = load_config()
