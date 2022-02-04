from utils import *
from rtid_out_info import RtidOutInfo
from rtid_config import RTIDConfig
from content_manager import ContentManager 
from datetime import datetime
from os import path, makedirs
import json
import praw
import secret
import sys

class RTID(Logger):
	def __init__(self, rtid_config: RTIDConfig):
		super().__init__()
		self.rtid_config = rtid_config
		self.reddit = None
		self.subreddit_instance = None
		self.init()
		self.rtid_out_info = RtidOutInfo(self.rtid_config.subreddit_name)
		self.content_manager = ContentManager(self.subreddit_instance, self.rtid_config)

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
			subreddits = self.reddit.subreddits
		except Exception as e:
			print(e)
			sys.exit(1)

		self.subreddit_instance = self.reddit.subreddit(self.rtid_config.subreddit_name)
		sub_exist = check_subreddit_exists(subreddits, self.rtid_config.subreddit_name)

		if not sub_exist:
			print(f"r/{self.rtid_config.subreddit_name} does not exist.")
			sys.exit(1)

	def run(self):
		hot_submission_contents = self.content_manager.get_hot_submission_contents()
		for content in hot_submission_contents:
			content.print_content_info()

		
		print("Finished...")
