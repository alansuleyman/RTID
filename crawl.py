#!/usr/bin/env python

from creds.credentials import Credentials
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
MAIN_IMAGE_OUTPUT_DIR = os.path.join(SCRIPT_PATH, "images")
MAIN_CSV_OUTPUT_DIR = os.path.join(SCRIPT_PATH, "csv")

# globals
DEFAULT_SUBREDDIT = "art"
DEFAULT_POST_LIMIT = 10
DEFAULT_MIN_UPVOTE = 1000
DEFAULT_NUM_OF_THREAD = 1

image_subreddit_folder_path = ""


def download_images(urls_list):

    global image_subreddit_folder_path

    # get the format of the image. E.g. jpg, png etc.
    image_format = urls_list[0].split("?")[0][::-1].split(".")[0][::-1]

    # image name is image's id + image format. E.g aiw966.jpg
    image_name = urls_list[1] + "." + image_format

    # folder where the image will be saved.
    # Images will be saved under input subreddit folder
    image_path = image_subreddit_folder_path + "/" + image_name

    # if the image exist, do not download the image
    if os.path.isfile(image_path):
        print("Image already exists.")
        pass
    else:
        try:
            # image does not exist, download it
            urllib.urlretrieve(urls_list[0], image_path)

        except IOError as err:
            print(err)


def get_content(content):
    json_tree = json.loads(content)
    images_list = json_tree["images"]
    images = images_list[0]
    return images


def get_original_image_url(content):
    images = get_content(content)
    source_list = images["source"]
    image_url_decode = json.dumps(source_list)
    image_url_tree = json.loads(image_url_decode)
    image_url = image_url_tree["url"]
    return image_url


# TODO use this function on later features


def get_top_resolution_image_url(content, image_quality):
    images = get_content(content)
    resolutions_list = images["resolutions"]
    top_resolution = resolutions_list[image_quality]
    top_resolution_url = top_resolution["url"]
    return top_resolution_url


# check whether input subreddit exist or not


def check_subreddit_exists(reddit, sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists


def write_to_csv(csvname, row_list):

    # if file does not exist, create it and set the field names
    if not os.path.exists(csvname):
        fields = [
            "id",
            "subreddit",
            "upvote",
            "title",
            "created_utc",
            "retrieved_utc",
            "image_url",
            "",
        ]
        with open(csvname, "a") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(fields)

    with open(csvname, "r") as csvfile:
        # read the file into a variable
        s = csvfile.read()

        # check to see if each list item is in the file, if not save it
        missing = []
        for row in row_list:
            if row[0] not in s:
                missing.append(row)

    # Write the missing rows to the file
    if missing:
        print("Missing rows exist.")
        with open(csvname, "a+") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerows(missing)


def main(subreddit_name, post_limit, min_upvote, thread_count):
    credentials = Credentials()

    reddit = praw.Reddit(
        client_id=credentials.app_client_id,
        client_secret=credentials.app_client_secret,
        username=credentials.reddit_username,
        password=credentials.reddit_pw,
        user_agent=credentials.app_name,
    )

    sub_exist = check_subreddit_exists(reddit, subreddit_name)

    if not sub_exist:
        print("r/{subreddit_name} does not exist.")
        sys.exit()

    global image_subreddit_folder_path
    image_subreddit_folder_path = os.path.join(MAIN_IMAGE_OUTPUT_DIR, subreddit_name)

    # if the subreddit image folder does not exist, create it
    if not os.path.exists(image_subreddit_folder_path):
        os.makedirs(image_subreddit_folder_path)

    csv_subreddit_folder_path = os.path.join(MAIN_CSV_OUTPUT_DIR, subreddit_name)

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
            print(f"{counter} , Preview not found")
            print("----------------------")
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
                content = Content(
                    submission.id,
                    submission.subreddit_name_prefixed,
                    submission.title,
                    submission.ups,
                    submission.created_utc,
                    time.time(),
                    image_url,
                )

                # save contents
                content_rows.append(
                    [
                        content.id,
                        content.subreddit,
                        content.upvote,
                        content.title,
                        content.content_created_utc,
                        content.content_retrieved_utc,
                        content.preview_image_url,
                    ]
                )

                # content.download_image(image_subreddit_folder_path)

                print(counter)
                print(f"Title: {content.title}")
                print(f"Upvotes: {content.upvote}")
                print(f"Content creation time: {content.content_created_utc}")
                content.print_creation_time()
                print("----------------------")

                # Create url array which contains image url, image id
                urls.append(content.preview_image_url)
                urls.append(str(content.id))
                url_list.append(urls)

    print(f"Using {thread_count} thread.")
    # create pool with the thread_count process
    pool = Pool(processes=thread_count)

    # perform download_images function on each url_list array content
    pool.map(download_images, url_list)

    elapsed_time_sec = time.time() - start

    print(f"Took {int(elapsed_time_sec)} seconds.")

    csv_name = os.path.join(csv_subreddit_folder_path, subreddit_name, "_contents.csv")
    write_to_csv(csv_name, content_rows)

    """ # save collected data to csv
    with open(csv_subreddit_folder_path + '/' + subreddit_name + '_contents.csv', 'w') as csvfile:
        label_row = ['id', 'subreddit', 'upvote', 'title',
                     'created_utc', 'retrieved_utc', 'image_url', '']
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(label_row)
        writer.writerows(content_rows) """


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subreddit",
        type=str,
        dest="subreddit_name",
        default=DEFAULT_SUBREDDIT,
        help="Which subreddit to crawl",
    )
    parser.add_argument(
        "--post_limit",
        type=int,
        dest="post_limit",
        default=DEFAULT_POST_LIMIT,
        help="Number of posts to crawl.",
    )
    parser.add_argument(
        "--min_upvote",
        type=int,
        dest="min_upvote",
        default=DEFAULT_MIN_UPVOTE,
        help="Minimum number of upvote to filter.",
    )
    parser.add_argument(
        "--thread",
        type=int,
        dest="thread_count",
        default=DEFAULT_NUM_OF_THREAD,
        help="Number of threads to use for downloading images.",
    )

    args = parser.parse_args()
    main(args.subreddit_name, args.post_limit, args.min_upvote, args.thread_count)
