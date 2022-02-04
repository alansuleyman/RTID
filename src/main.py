"""Entry point of the RTID application."""

import argparse
import config
from rtid import RTID, RTIDConfig


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subreddit_name",
        type=str,
        dest="subreddit_name",
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
    rtid_config = RTIDConfig(args.subreddit_name, args.post_limit, args.min_upvote)
    rtid = RTID(rtid_config)
    rtid.run()
