#!/usr/bin/env python

from credentials import *
from content import Content
import argparse
import io
import os
import praw
import json
import time
import csv

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

    content_rows = []

    for counter, submission in enumerate(hot_python):

        # check whether the post has image preview or not
        try:
            preview = json.dumps(submission.preview)
        except (TypeError, AttributeError):
            print str(counter) + ', Preview not found. '
            print '----------------------'
            continue

        # do not crawl the stickied posts
        # since they are just for subreddit rule explanation
        if not submission.stickied:

            # download the images which have more than 1k upvote
            if submission.ups > min_upvote:

                image_url = get_original_image_url(preview)

                # create content object
                content = Content(submission.id, submission.subreddit_name_prefixed, submission.title,
                                  submission.ups, submission.created_utc, time.time(), image_url)

                # save contents
                content_rows.append([content.id, content.subreddit, content.upvote, content.title,
                                     content.content_created_utc, content.content_retrieved_utc, content.preview_image_url])

                content.download_image(subreddit_folder_path)

                print str(counter)
                print 'Title: ' + content.title
                print 'Ups: ' + str(content.upvote)
                print 'Content created: ' + content.content_created_utc
                content.print_creation_time()
                print '----------------------'

    # save collected data to csv
    with open(subreddit_name + '_contents.csv', 'w') as csvfile:
        label_row = ['id', 'subreddit', 'upvote', 'title',
                     'created_utc', 'retrieved_utc', 'image_url', '']
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(label_row)
        writer.writerows(content_rows)


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
