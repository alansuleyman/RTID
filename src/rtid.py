from utils import *
from rtid_out_info import RtidOutInfo
from datetime import datetime
from os import path, makedirs
import json
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
		self.config = rtid_config
		self.reddit = None
		self.subreddit_instance = None
		self.init()
		self.rtid_out_info = RtidOutInfo(self.config.subreddit_name)

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

		self.subreddit_instance = self.reddit.subreddit(self.config.subreddit_name)
		sub_exist = check_subreddit_exists(subreddits, self.config.subreddit_name)

		if not sub_exist:
			print(f"r/{self.config.subreddit_name} does not exist.")
			sys.exit(1)

	def get_preview(self, submission) -> str:
		# check whether the post has image preview or not
		preview = None
		try:
			preview = json.dumps(submission.preview)
		except (TypeError, AttributeError):
			self.log.warning("Preview not found, skipping current post...")
		return preview

	def get_preview_img(self, preview: str):
		preview_json_obj = json.loads(preview)
		imgs_list = preview_json_obj["images"]
		preview_img = imgs_list[0]
		return preview_img

	def get_original_img_url(self, preview: str) -> str:
		preview_img = self.get_preview_img(preview)
		source_list = preview_img["source"]
		img_url_decode = json.dumps(source_list)
		img_url_json_obj = json.loads(img_url_decode)
		img_url = img_url_json_obj["url"]
		return img_url

	def get_hot_submission_previews(self):
		# Get the hot submissions which have more than given minimum number of upvote
		# to filter and given number of posts to look
		hot_previews = []
		hot_submissions = self.subreddit_instance.hot(limit=self.config.post_limit)
		for submission in hot_submissions:
			# Skip the stickied posts since they are mostly just for subreddit rule explanation
			if submission.stickied:
				self.log.info("Skipping stickied post...")
				continue
			
			preview = self.get_preview(submission)
			if preview is None:
				continue

			if submission.ups > self.config.min_upvote:
				hot_previews.append(preview)
		return hot_previews

	def run(self):
		hot_previews = self.get_hot_submission_previews()
		for preview in hot_previews:
			img_url = self.get_original_img_url(preview)
			print(f"image url: {img_url}")

		
		print("run...")
