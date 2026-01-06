import os

class Config(object):
     
    API_ID = int(os.getenv("API_ID", 22141398))
    API_HASH = os.getenv("API_HASH", '0c8f8bd171e05e42d6f6e5a6f4305389')
    BOT_TOKEN = os.getenv("BOT_TOKEN", '8341015170:AAHm5nUw8snd1MVXN3fRzw-7zHtZvBjrd6o') 
    #Add your channel id. For force Subscribe.
    CHANNEL = os.environ.get("CHANNEL", "-1002087228619")
    #Skip or add your proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = ''
