from content_info import ContentInfo
import json
import praw
from os import path
from rtid_config import RTIDConfig
from utils import *
import urllib.request

class ContentManager(Logger):
	def __init__(self, subreddit_instance, rtid_config: RTIDConfig):
		super().__init__()
		self.subreddit_instance = subreddit_instance
		self.rtid_config = rtid_config

	def get_hot_submission_contents(self):
		# Get the hot submissions which have more than given minimum number of upvote
		# to filter and given number of posts to look
		def get_preview(submission) -> str:
			# check whether the post has image preview or not
			preview = None
			try:
				preview = json.dumps(submission.preview)
			except (TypeError, AttributeError):
				self.log.warning("Preview not found, skipping current post...")
			return preview

		hot_submission_contents = []
		hot_submissions = self.subreddit_instance.hot(limit=self.rtid_config.post_limit)
		for submission in hot_submissions:
			# Skip the stickied posts since they are mostly just for subreddit rule explanation
			if submission.stickied:
				self.log.info("Skipping stickied post...")
				continue
			
			if get_preview(submission) is None:
				continue

			if submission.ups > self.rtid_config.min_upvote:
				content_info = ContentInfo(submission=submission)
				hot_submission_contents.append(content_info)
				
		return hot_submission_contents

	def download_img(self, img_download_path: str, img_url: str):

		# if the image exist, do not download the image
		if path.isfile(img_download_path):
			self.log.info(f"Image name {img_download_path} already exists.")
		else:
			try:
				# image does not exist, download it
				urllib.request.urlretrieve(img_url, img_download_path)
			except IOError as err:
				self.log.error(err)
