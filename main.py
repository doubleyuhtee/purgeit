import json
import time

import praw
from dotenv import load_dotenv
import os

load_dotenv()

delete_age = (int)(os.getenv('PRESERVE_EDIT_DAYS', 90)) * 60 * 60 * 24
use_troll_user_agent = os.getenv('FUCKWITHTHEMABIT', "false").lower() in ('true', "t")


if __name__ == '__main__':
    creds_mode = os.getenv('CREDS_MODE')
    creds_list = [
        {
            "username": os.getenv('REDDITUSERNAME'),
            "password": os.getenv("PASSWORD"),
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET")
        }
    ] if creds_mode == "env" else json.loads(open(creds_mode).read())

    for c in creds_list:
        username = c["username"]
        user_agent = "test" if use_troll_user_agent else f"Praw:Purgeit:v0.0.1 (as /u/{username})"

        reddit = praw.Reddit(
            client_id=c["client_id"],
            client_secret=c["client_secret"],
            password=c["password"],
            user_agent=user_agent,
            username=username,
        )
        print(f"Running as {user_agent}")
        print("clearing comments")
        for s in reddit.redditor(username).submissions.new():
            print(s.title)
            s.delete()
        stuffdeleted = True
        while stuffdeleted:
            print("")
            stuffdeleted = False
            for c in reddit.redditor(username).comments.new(limit=None):
                if not c.body == "#":
                    print(c.body)
                    if "purgeit" not in c.body and "!save" not in c.body:
                        stuffdeleted = True
                        c.edit('#')
                else:
                    if c.edited:
                        if c.edited < time.time() - delete_age:
                            print("x", end="", flush=True)
                            stuffdeleted = True
                            c.delete()
                        else:
                            print(".", end="", flush=True)
                    else:
                        print(",", end="", flush=True)
        print("")
