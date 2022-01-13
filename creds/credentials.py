import toml
from os import path, makedirs
import pathlib


class Credentials:
    def __init__(self):
        self.data = ""
        self.toml_data = toml.load(
            path.join(pathlib.Path(__file__).parent.resolve(), "credentials.toml")
        )
        self.creds = self.toml_data["creds"]
        self.app_client_id = self.creds["APP_CLIENT_ID"]
        self.app_client_secret = self.creds["APP_CLIENT_SECRET"]
        self.reddit_username = self.creds["REDDIT_USERNAME"]
        self.reddit_pw = self.creds["REDDIT_PW"]
        self.app_name = self.creds["APP_NAME"]
