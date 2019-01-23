# RTID : Reddit Top Images Downloader

RTID, an acronym for "Reddit Top Images Downloader", is a python script for downloading top images from Reddit's subreddits by using PRAW ("Python Reddit API Wrapper").

## Installation

First you need to install PRAW in order to use RTID. The recommended way to install PRAW is via [pip](https://pypi.python.org/pypi/pip).

## Included Components

- [PRAW](https://github.com/praw-dev/praw): PRAW, an acronym for "Python Reddit API Wrapper", is a python package that allows for simple access to Reddit's API. PRAW aims to be easy to use and internally follows all of [Reddit's API rules](https://github.com/reddit-archive/reddit/wiki/API).

## Quickstart

You need to have credentials to be able to use Reddit api. For instructions on setting Reddit to authenticate on non-reddit websites and applications, check [Reddit OAuth2](https://github.com/reddit-archive/reddit/wiki/oauth2).

You can instantiate an instance of PRAW like so:

```python
import praw
reddit = praw.Reddit(client_id='CLIENT_ID', client_secret="CLIENT_SECRET",
                     password='PASSWORD', user_agent='USERAGENT',
                     username='USERNAME')
```

## Compile Instructions

[crawl.py](https://github.com/alansuleyman/RTID/blob/master/crawl.py) is the main script for executing the program. Flags for this script are:

- `--subreddit` for specifying which subreddit to get images. Default is _art_ subreddit.

- `--post-limit` for specifying the number of posts to crawl. Default is _10_.

- `--min-upvote` for specifying which contents should be crawled by applying minimum upvote threshold. This should be increased if you want to get more upvoted contents. Default is _1000_ upvotes.

- `--thread` controls the number of processes to be used when compiling. You’ll want to set this value to the number of processors/cores on your machine. For example, if you have 8 core processor, set it _8_. If the value is higher, it takes less time to download images. Default is _1_ which means the program only uses single core.

To run the script, you can simply do:

```
python crawl.py --subreddit witcher --post-limit 60 --min-upvote 1500 --thread 8
```

When the script is completed, the images will be saved in `./images/<your subreddit input>/` and a csv file will be saved as `./csv/<your subreddit input>/<your subreddit input>_contents.csv`

Csv file stores the followings:

- image id,
- subreddit name,
- title of the post,
- post upvote,
- post creation date,
- image download date,
- url of the preview image
