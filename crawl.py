#!/usr/bin/env python

from credentials import *
import argparse
import io
import os
import praw
import json
import sys
import urllib
import datetime
import time

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

MAIN_OUTPUT_DIR = os.path.join(SCRIPT_PATH, 'images')

DEFAULT_SUBREDDIT = 'all'

DEFAULT_POST_LIMIT = 10

DEFAULT_MIN_UPVOTE = 1000


def get_content(content):
    json_tree = json.loads(content)
    images_list = json_tree['images']
    images = images_list[0]
    return images


def get_original_image_url(content):
    images = get_content(content)
    source_list = images['source']
    image_url_decode = json.dumps(source_list)
    image_url_tree = json.loads(image_url_decode)
    image_url = image_url_tree['url']
    return image_url


def get_top_resolution_image_url(content, image_quality):
    images = get_content(content)
    resolutions_list = images['resolutions']
    top_resolution = resolutions_list[image_quality]
    top_resolution_url = top_resolution['url']
    return top_resolution_url


def download_image(id, image_url, subreddit_folder_path):

    image_format = image_url.split("?")[0][-3:]

    image_name = id + '.' + image_format

    image_path = subreddit_folder_path + '/' + image_name

    # if the image exist, do not download the image
    if os.path.isfile(image_path):
        pass
    else:
        # image does not exist, download it
        try:
            print 'Downloading image...'
            urllib.urlretrieve(image_url, image_path)
        except IOError, err:
            print err
            sys.exit()


def creation_time(created_utc):
    # ago dictionary holds the content's creation time
    ago = {}

    date = datetime.datetime.fromtimestamp(created_utc)
    ago['year'] = date.year
    ago['month'] = date.month
    ago['day'] = date.day
    ago['hour'] = date.hour
    ago['minute'] = date.minute
    ago['second'] = date.second

    current_time = int(time.time())
    hours = (current_time - created_utc)/3600
    days = (current_time - created_utc)/86400
    months = (current_time - created_utc)/2592000

    if months == 0:
        if days == 0:
            print 'Created ' + str(hours) + ' hours ago.'
        else:
            print 'Created ' + str(days) + ' days ago.'
    else:
        print 'Created ' + str(months) + ' months ago.'

    return hours


def main(subreddit_name, post_limit, min_upvote):

    # if the subreddit image folder not exist, then create it
    subreddit_folder_path = MAIN_OUTPUT_DIR + '/' + subreddit_name

    if not os.path.exists(subreddit_folder_path):
        os.makedirs(subreddit_folder_path)

    reddit = praw.Reddit(client_id=APP_CLIENT_ID,
                         client_secret=APP_CLIENT_SECRET,
                         username=REDDIT_USERNAME,
                         password=REDDIT_PW,
                         user_agent=APP_NAME
                         )

    subreddit = reddit.subreddit(subreddit_name)

    hot_python = subreddit.hot(limit=post_limit)

    for submission in hot_python:

        # check whether the post has image preview or not
        try:
            preview = json.dumps(submission.preview)
        except (TypeError, AttributeError):
            print 'Preview not found. '
            print '----------------------'
            continue

        if submission.stickied:
            # do not crawl the stickied posts
            # since they are just for subreddit rule explanation
            continue

        # download the images which have more than 1k upvote
        if submission.ups > min_upvote:

            creation_time(int(submission.created_utc))
            print 'Title: ' + submission.title
            print 'Ups: ' + str(submission.ups)

            image_url = get_original_image_url(preview)

            download_image(str(submission.id), image_url,
                           subreddit_folder_path)
            print '----------------------'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--subreddit', type=str, dest='subreddit_name',
                        default=DEFAULT_SUBREDDIT,
                        help='Which subreddit to crawl')
    parser.add_argument('--post-limit', type=int, dest='post_limit',
                        default=DEFAULT_POST_LIMIT,
                        help='Number of posts to crawl.')
    parser.add_argument('--min-upvote', type=int, dest='min_upvote',
                        default=DEFAULT_MIN_UPVOTE,
                        help='Minimum number of upvote to filter.')

    args = parser.parse_args()
    main(args.subreddit_name, args.post_limit, args.min_upvote)
