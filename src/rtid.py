from utils import *
from rtid_out_info import RtidOutInfo
from datetime import datetime
from os import path, makedirs
import praw
import secret
import sys

class RTIDConfig:
	def __init__(self, subreddit_name, post_limit, min_upvote):
		self.subreddit_name = subreddit_name
		self.post_limit = post_limit
		self.min_upvote = min_upvote

class RTID(Logger):
	def __init__(self, rtid_config: RTIDConfig):
		super().__init__()
		now = datetime.now()
		date_string = now.strftime("%d_%m_%Y_%H_%M_%S")
		self.out_dir = path.join(RtidOutInfo.OUT_DIR,"RTID_Downloads",date_string)
		try:
			makedirs(self.out_dir, exist_ok=False)
			self.log.info(f"Directory {self.out_dir} has been created")
		except OSError:
			self.log.info(f"Directory {self.out_dir} could not be created")

		
		self.config = rtid_config
		self.reddit = None
		self.subreddit = None
		self.init()

	def init(self):
		self.log.info("Starting RTID")
		self.log.info("Instantiating Reddit instance")
		
		self.reddit = praw.Reddit(
			client_id=secret.reddit_client_id,
			client_secret=secret.reddit_client_secret,
			username=secret.reddit_username,
			password=secret.reddit_password,
			user_agent=secret.reddit_user_agent,
		)

		# Subreddits is a Listing class that provides various subreddit lists
		try:
			self.subreddit = self.reddit.subreddits
		except Exception as e:
			print(e)
			sys.exit(1)

		sub_exist = check_subreddit_exists(self.subreddit, self.config.subreddit_name)

		if not sub_exist:
			print(f"r/{self.config.subreddit_name} does not exist.")
			sys.exit(1)
		

	def run(self):
		print("run...")
