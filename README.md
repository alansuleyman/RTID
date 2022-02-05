# RTID : Reddit Top Images Downloader

RTID, an acronym for "Reddit Top Images Downloader", is a python script for downloading top images from Reddit's subreddits by using PRAW ("Python Reddit API Wrapper").

## Synopsis
```
python3 src/main.py [options] 
```

## Installation

Install packages by running `pip3 install -r .\requirements.txt`

## Components

- [PRAW](https://github.com/praw-dev/praw): PRAW, an acronym for "Python Reddit API Wrapper", is a python package that allows for simple access to Reddit's API. PRAW aims to be easy to use and internally follows all of [Reddit's API rules](https://github.com/reddit-archive/reddit/wiki/API).

## Quickstart

You need to have credentials to be able to use Reddit api. For instructions on setting Reddit to authenticate on non-reddit websites and applications, check [Reddit OAuth2](https://github.com/reddit-archive/reddit/wiki/oauth2).

Set the following variables as environment variable in order to use RTID:
```
REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET
REDDIT_USERNAME
REDDIT_PASSWORD
REDDIT_USER_AGENT
```

## Description

[src/main.py] Main script for executing the program.
Example run:
Without parameters:
```
python3 main.py
```

With parameters:
```
python3 main.py --subreddit_name witcher --post_limit 60 --min_upvote 1500
```

Script will create folder named `RTID_Downloads` and create folder with given subreddit name. Then download images to here.
When the script is completed, the images will be saved in `./RTID_Downloads/<SUBREDDIT_NAME>/<CURRENT_DATE>` 

## Options
- `--help` Print help message.

- `--subreddit_name` Which subreddit to get images. Default is _art_ subreddit.

- `--post_limit` Number of post submissions to look up. Default is _10_.

- `--min_upvote` Minimum number of upvote to filter. Default is _1000_ upvotes.

