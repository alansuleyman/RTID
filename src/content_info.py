from enum import Enum
import json
import praw
from utils import *
import urllib.parse

REDDIT_URL = "https://www.reddit.com"
REDDIT_IMG_CONTENT_BASE_URL = "https://i.redd.it"
REDDIT_VIDEO_CONTENT_BASE_URL = "https://v.redd.it"
REDDIT_PREVIEW_CONTENT_BASE_URL = "https://preview.redd.it/"

class ContentType(Enum):
	IMAGE = 1
	VIDEO = 2
	OTHER = 3

class ContentInfo(Logger):
	def __init__(self, submission):
		super().__init__()
		self.submission = submission
		self.id = self.submission.id
		self.permalink = self.submission.permalink # path without reddit url
		self.post_url = urllib.parse.urljoin(REDDIT_URL, self.permalink) 
		self.content_url = self.submission.url
		self.content_format = None
		self.title_to_underscore = self.post_url.split("/")[-2]
		self.content_full_name = None
		self.subreddit_name = self.submission.subreddit_name_prefixed.split("/")[1]
		self.title = self.submission.title
		self.score = self.submission.score
		self.content_type = self.get_content_type()

		if self.content_type == ContentType.IMAGE:
			self.content_format = self.content_url.split(".")[-1]
			self.content_full_name = self.title_to_underscore + "." + self.content_format


	def get_content_type(self):
		if (REDDIT_IMG_CONTENT_BASE_URL in self.content_url) or (REDDIT_PREVIEW_CONTENT_BASE_URL in self.content_url):
			return ContentType.IMAGE
		elif REDDIT_VIDEO_CONTENT_BASE_URL in self.content_url:
			return ContentType.VIDEO
		else:
			return ContentType.OTHER
	
	def print_content_info(self):
		print(f"[content_info]\n"
					f"id: {self.id}\n"
					f"permalink: {self.permalink}\n"
					f"post_url: {self.post_url}\n"
					f"content_url: {self.content_url}\n"
					f"content_format: {self.content_format}\n"
					f"title_to_underscore: {self.title_to_underscore}\n"
					f"content_full_name: {self.content_full_name}\n"
					f"subreddit_name: {self.subreddit_name}\n"
					f"title: {self.title}\n"
					f"score: {self.score}\n"
		)
