from datetime import datetime
from os import path, makedirs
from pathlib import Path
from utils import *

class RtidOutInfo(Logger):
	def __init__(self, subreddit_name: str):
		super().__init__()
		self.subreddit_name = subreddit_name
		self.current_dir = path.dirname(path.abspath(__file__))
		self.download_dir_name = "out"
		self.download_dir_path = path.join(Path(self.current_dir).parent.absolute(), self.download_dir_name)
		self.subreddit_download_path = None
		self.CreateSubredditDownloadDir()

	def CreateSubredditDownloadDir(self):
		now = datetime.now()
		date_string = now.strftime("%d_%m_%Y")
		self.subreddit_download_path = path.join(self.download_dir_path, "RTID_Downloads", self.subreddit_name, date_string)

		try:
			makedirs(self.subreddit_download_path, exist_ok=False)
			self.log.info(f"Directory {self.subreddit_download_path} has been created")
		except OSError:
			self.log.info(f"Directory {self.subreddit_download_path} could not be created")
