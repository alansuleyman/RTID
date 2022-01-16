from utils import *
import secret
import praw
import sys

class RTID(Logger):
	def __init__(self, rtid_config):
		super().__init__()
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


		sub_exist = check_subreddit_exists(self.subreddit, self.config["subreddit"])

		if not sub_exist:
			print(f"r/{self.config['subreddit']} does not exist.")
			sys.exit(1)
		

	def run(self):
		pass
