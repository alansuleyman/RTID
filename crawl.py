

import praw
from credentials import *
import json
import sys
import urllib


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


def get_top_resolution_image_url(content):
    images = get_content(content)
    resolutions_list = images['resolutions']
    top_resolution = resolutions_list[-1]
    top_resolution_url = top_resolution['url']
    return top_resolution_url


def download_image(id, image_url):
    folder_name = './images/'
    image_name = id + '.jpg'
    try:
        print 'Downloading image...'
        urllib.urlretrieve(image_url, folder_name + image_name)
    except IOError, err:
        print err
        sys.exit()


def main():

    reddit = praw.Reddit(client_id=APP_CLIENT_ID,
                         client_secret=APP_CLIENT_SECRET,
                         username=REDDIT_USERNAME,
                         password=REDDIT_PW,
                         user_agent=APP_NAME
                         )

    subreddit = reddit.subreddit('malelivingspace')

    set_limit = 10

    hot_python = subreddit.hot(limit=set_limit)

    for counter, submission in enumerate(hot_python):
        if counter == 0:
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

        image_url = get_top_resolution_image_url(preview_dumped)
        print 'image_url: ' + image_url

        download_image(str(submission.id), image_url)

        print '----------------------'


if __name__ == "__main__":
    main()
