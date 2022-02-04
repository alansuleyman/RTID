import praw
import urllib.parse

REDDIT_URL = "https://www.reddit.com"

class ContentInfo:
	def __init__(self, submission):
		super().__init__()
		self.submission = submission
		self.id = self.submission.id
		self.permalink = self.submission.permalink # path without reddit url
		self.post_url = urllib.parse.urljoin(REDDIT_URL, self.permalink) 
		self.content_url = self.submission.url
		self.subreddit_name = self.submission.subreddit_name_prefixed.split("/")[1]
		self.title = self.submission.title
		self.title_to_underscore = self.post_url.split("/")[-2]
		self.ups = self.submission.ups
	
	def print_content_info(self):
		print(f"[content_info]\n"
					f"id: {self.id}\n"
					f"permalink: {self.permalink}\n"
					f"post_url: {self.post_url}\n"
					f"content_url: {self.content_url}\n"
					f"subreddit_name: {self.subreddit_name}\n"
					f"title: {self.title}\n"
					f"title_to_underscore: {self.title_to_underscore}\n"
					f"ups: {self.ups}\n"
		)
