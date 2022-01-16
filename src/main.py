"""Entry point of the RTID application."""

import argparse
import config
from rtid import RTID


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subreddit",
        type=str,
        dest="subreddit",
        default=config.DEFAULT_SUBREDDIT,
        help="Which subreddit to look",
    )
    parser.add_argument(
        "--post_limit",
        type=int,
        dest="post_limit",
        default=config.DEFAULT_POST_LIMIT,
        help="Number of posts to look.",
    )
    parser.add_argument(
        "--min_upvote",
        type=int,
        dest="min_upvote",
        default=config.DEFAULT_MIN_UPVOTE,
        help="Minimum number of upvote to filter.",
    )

    args = parser.parse_args()
    rtid_config = {
        "subreddit": args.subreddit,
        "post_limit": args.post_limit,
        "min_upvote": args.min_upvote,
    }
    rtid = RTID(rtid_config)
