import datetime
import time
import os
import sys
import urllib
import sys

# Setting the system default encoding as utf-8, so that all strings are encoded using that.
reload(sys)
sys.setdefaultencoding('utf-8')


class Content:
    def __init__(self, id, subreddit, title, upvote, content_created_utc, content_retrieved_utc, preview_image_url):
        self.id = id
        self.subreddit = subreddit.split('/')[1]
        self.title = title
        self.upvote = upvote
        self.content_created_utc = content_created_utc
        self.content_retrieved_utc = content_retrieved_utc
        self.preview_image_url = preview_image_url
        self.content_created_utc_timestamp = content_created_utc
        self.content_retrieved_utc_timestamp = content_retrieved_utc
        self.convert_timestamp_to_utc()

    def timestamp_to_utc(self):
        return time.ctime(self.content_retrieved_utc)

    def convert_timestamp_to_utc(self):
        self.content_created_utc = time.ctime(self.content_created_utc)
        self.content_retrieved_utc = time.ctime(self.content_retrieved_utc)

    def print_creation_time(self):

        current_time = int(time.time())
        time_difference = current_time - \
            int(self.content_created_utc_timestamp)

        hours = time_difference/3600
        days = time_difference/86400
        months = time_difference/2592000

        if months == 0:
            if days == 0:
                print 'Content is created ' + str(hours) + ' hours ago.'
            else:
                print 'Content is created ' + str(days) + ' days ago.'
        else:
            print 'Content is created ' + str(months) + ' months ago.'

    def download_image(self, subreddit_folder_path):

        # Example
        # image_url = https://preview.redd.it/9xire13l90c21.jpg?auto=webp&s=5360e514e90d0910062b59020f6fdf863602255a
        # split string with '?' . Results in two strings .
        # 'https://preview.redd.it/9xire13l90c21.jpg' and 'auto=webp&s=5360e514e90d0910062b59020f6fdf863602255a'
        # take the first string since it contains the image format
        # reverse the string. Results in 'gpj.12c09l31erix9/ti.dder.weiverp//:sptth'
        # Split the string with '.'
        # Gives this array ['gpj', '12c09l31erix9/ti', 'dder', 'weiverp//:sptth']
        # Take the first index 'gpj' and reverse it 'jpg'

        image_format = self.preview_image_url.split(
            "?")[0][::-1].split('.')[0][::-1]

        image_name = self.id + '.' + image_format

        image_path = subreddit_folder_path + '/' + image_name

        # if the image exist, do not download the image
        if os.path.isfile(image_path):
            print 'Image already exists.'
            pass
        else:
            # image does not exist, download it
            try:
                print 'Downloading image...'
                urllib.urlretrieve(self.preview_image_url, image_path)
            except IOError, err:
                print err
                sys.exit()
