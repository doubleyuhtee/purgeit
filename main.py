import praw
from dotenv import load_dotenv
import os


load_dotenv()

username = os.getenv('REDDITUSERNAME')

deletepass = os.getenv('RUN_DELETE', "false").lower() in ('true', "t")
use_troll_user_agent = os.getenv('FUCKWITHTHEMABIT', "false").lower() in ('true', "t")
user_agent = "test" if use_troll_user_agent else f"Praw:Purgeit:v0.0.1 (as /u/{username})"

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    password=os.getenv("PASSWORD"),
    user_agent=user_agent,
    username=username,
)

if __name__ == '__main__':
    print(f"Running as {user_agent}")
    if deletepass:
        print("Any comments with '#' for content will be deleted.")
    else:
        print("clearing comments")
    for c in reddit.redditor(username).comments.new(limit=None):
        if not c.body == "#":
            print(c.body)
            c.edit('#')
        else:
            print(".", end="")
            if deletepass:
                print("oops")
                # c.delete()