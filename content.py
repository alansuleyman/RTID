import datetime
import time


class Content:
    def __init__(self, id, subreddit, title, upvote, content_created_utc, content_retrieved_utc, preview_image_url):
        self.id = id
        self.subreddit = subreddit
        self.title = title
        self.upvote = upvote
        self.content_created_utc = content_created_utc
        self.content_retrieved_utc = content_retrieved_utc
        self.preview_image_url = preview_image_url
        self.convert_timestamp_to_utc()

    def timestamp_to_utc(self):
        return time.ctime(self.content_retrieved_utc)

    def convert_timestamp_to_utc(self):
        self.content_created_utc = time.ctime(self.content_created_utc)
        self.content_retrieved_utc = time.ctime(self.content_retrieved_utc)
