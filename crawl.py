#!/usr/bin/env python

from credentials import *
from content import Content
import argparse
import io
import os
import praw
from prawcore import NotFound
import json
import time
import csv
import sys
import urllib
from multiprocessing import Pool

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
MAIN_IMAGE_OUTPUT_DIR = os.path.join(SCRIPT_PATH, 'images')
MAIN_CSV_OUTPUT_DIR = os.path.join(SCRIPT_PATH, 'csv')

# globals
DEFAULT_SUBREDDIT = 'all'
DEFAULT_POST_LIMIT = 10
DEFAULT_MIN_UPVOTE = 1000
DEFAULT_NUM_OF_THREAD = 1

image_subreddit_folder_path = ''


def download_images_using_thread(urls_list):

    global image_subreddit_folder_path

    image_format = urls_list[0].split(
        "?")[0][::-1].split('.')[0][::-1]

    image_name = urls_list[1] + '.' + image_format

    image_path = image_subreddit_folder_path + '/' + image_name

    # time.sleep(1)

    # if the image exist, do not download the image
    if os.path.isfile(image_path):
        print 'Image already exists.'
        pass
    else:
        # image does not exist, download it
        try:
            print str(os.getpid()) + ' working on ' + \
                image_name + ' downloading image...'
            urllib.urlretrieve(urls_list[0], image_path)
            print str(os.getpid()) + ' downloaded ' + \
                image_name + "!!!!!!!!!"

        except IOError, err:
            print err


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


def check_subreddit_exists(reddit, sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists


def main(subreddit_name, post_limit, min_upvote, thread_count):

    reddit = praw.Reddit(client_id=APP_CLIENT_ID,
                         client_secret=APP_CLIENT_SECRET,
                         username=REDDIT_USERNAME,
                         password=REDDIT_PW,
                         user_agent=APP_NAME
                         )

    sub_exist = check_subreddit_exists(reddit, subreddit_name)

    if not sub_exist:
        print 'r/' + subreddit_name + ' doesn\'t exist.'
        sys.exit()

    global image_subreddit_folder_path
    image_subreddit_folder_path = MAIN_IMAGE_OUTPUT_DIR + '/' + subreddit_name

    # if the subreddit image folder does not exist, create it
    if not os.path.exists(image_subreddit_folder_path):
        os.makedirs(image_subreddit_folder_path)

    csv_subreddit_folder_path = MAIN_CSV_OUTPUT_DIR + '/' + subreddit_name

    # if the subreddit csv folder does not exist, create it
    if not os.path.exists(csv_subreddit_folder_path):
        os.makedirs(csv_subreddit_folder_path)

    subreddit = reddit.subreddit(subreddit_name)

    hot_python = subreddit.hot(limit=post_limit)

    content_rows = []
    url_list = []

    start = time.time()
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
                # urls array keeps the image url and the image id
                urls = []

                image_url = get_original_image_url(preview)

                # create content object
                content = Content(submission.id, submission.subreddit_name_prefixed, submission.title,
                                  submission.ups, submission.created_utc, time.time(), image_url)

                # save contents
                content_rows.append([content.id, content.subreddit, content.upvote, content.title,
                                     content.content_created_utc, content.content_retrieved_utc, content.preview_image_url])

                # content.download_image(image_subreddit_folder_path)

                print str(counter)
                print 'Title: ' + content.title
                print 'Ups: ' + str(content.upvote)
                print 'Content created: ' + content.content_created_utc
                content.print_creation_time()
                print '----------------------'

                # Create url array which contains image url, image id and image's subreddit
                urls.append(content.preview_image_url)
                urls.append(str(content.id))
            url_list.append(urls)
    print 'Using ' + str(thread_count) + ' thread.'
    pool = Pool(processes=thread_count)
    pool.map(download_images_using_thread, url_list)

    end = time.time()

    print 'Downloading took ' + str(int(end - start)) + ' seconds.'

    # save collected data to csv
    with open(csv_subreddit_folder_path + '/' + subreddit_name + '_contents.csv', 'w') as csvfile:
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
    parser.add_argument('--thread', type=int, dest='thread_count',
                        default=DEFAULT_NUM_OF_THREAD,
                        help='Number of threads to use for downloading images.')

    args = parser.parse_args()
    main(args.subreddit_name, args.post_limit,
         args.min_upvote, args.thread_count)
