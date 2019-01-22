
#!/usr/bin/env python

import argparse
import io
import os
import praw
from credentials import *
import json
import sys
import urllib


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

# Default path.
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_PATH, 'images')

# Default image quality which is source
DEFAULT_IMAGE_QUALITY = 6


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


def download_image(id, image_url, image_quality):
    image_name = id + '_' + str(image_quality) + '.jpg'

    if not os.path.exists(DEFAULT_OUTPUT_DIR):
        os.makedirs(DEFAULT_OUTPUT_DIR)

    path = DEFAULT_OUTPUT_DIR + '/' + image_name

    try:
        print 'Downloading image...'
        urllib.urlretrieve(image_url, path)
    except IOError, err:
        print err
        sys.exit()


def main(image_quality):

    reddit = praw.Reddit(client_id=APP_CLIENT_ID,
                         client_secret=APP_CLIENT_SECRET,
                         username=REDDIT_USERNAME,
                         password=REDDIT_PW,
                         user_agent=APP_NAME
                         )

    subreddit = reddit.subreddit('malelivingspace')

    set_limit = 2

    hot_python = subreddit.hot(limit=set_limit)

    for submission in hot_python:
        if submission.stickied:
            # do not crawl the stickied posts
            # since they are just for subreddit rule explanation
            continue
        """ print 'downs: ' + str(submission.downs)
        print 'title: ' + submission.title
        print 'likes: ' + str(submission.likes)
        # print 'media: ' + submission.media
        print 'score: ' + str(submission.score)
        print 'ups: ' + str(submission.ups)
        print 'upvote: ' + str(submission.upvote)
        print 'view_count: ' + str(submission.view_count) """

        print 'title: ' + submission.title

        preview_dumped = json.dumps(submission.preview)

        if image_quality == DEFAULT_IMAGE_QUALITY:
            image_url = get_original_image_url(preview_dumped)
        elif image_quality >= 0 and image_quality <= 5:
            image_url = get_top_resolution_image_url(
                preview_dumped, image_quality)
        else:
            print 'Invalid image quality. Please try between 0 and 5. Or leave it blank for source quality.'
            sys.exit()

        print 'image_url: ' + image_url

        download_image(str(submission.id), image_url, image_quality)

        print '----------------------'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-quality', type=int, dest='image_quality',
                        default=DEFAULT_IMAGE_QUALITY,
                        help='Image download quality. Default quality is the source quality. '
                             'It can be changed between 0 and 5. '
                             '0 is the least quality and 4 is the top quality.')

    args = parser.parse_args()
    main(args.image_quality)
