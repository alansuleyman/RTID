import logging
import praw

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Logger(object):
    def __init__(self, name : str = None):
        name = self.__class__.__name__
        self.log = logging.getLogger(name)

def check_subreddit_exists(subreddits : praw.models.Subreddits, sub : str):
    exists = True
    try:
        subreddits.search_by_name(sub, exact=True)
    except Exception as e:
        print(e)
        exists = False
    return exists