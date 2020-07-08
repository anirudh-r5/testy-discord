import os
from discord.ext import tasks,commands
import praw
from datetime import datetime, timedelta

from dotenv import load_dotenv

class Redditor(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        load_dotenv()
        self.reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                                client_secret=os.getenv('REDDIT_API_KEY'),
                                user_agent=os.getenv('USER_AGENT'))
        self.sentpost = False
        self.start_time = datetime.now()
        self.f1memes.start()

    @tasks.loop(minutes=15)
    async def f1memes(self):
        prev = self.start_time
        now = datetime.now()
        print(f'At {datetime.now()}, {now-prev} time has passed')
        if now - prev >= timedelta(hours=6,minutes=0,seconds=0):
                for submission in self.reddit.subreddit("formuladank").top('day', limit = 5):
                    print(submission.url)
                    self.start_time = datetime.now()
            
# for submission in reddit.subreddit("all").hot(limit=5):
#     print(submission.url)

def setup(bot):
    bot.add_cog(Redditor(bot))