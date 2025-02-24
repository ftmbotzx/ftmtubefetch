import os

class Config(object):
     
    API_ID = int(os.getenv("API_ID", 22141398))
    API_HASH = os.getenv("API_HASH", '0c8f8bd171e05e42d6f6e5a6f4305389')
    BOT_TOKEN = os.getenv("BOT_TOKEN", '8105194942:AAEG8X_NCA-bP506l2OAlMwt-sgUDWIqdl4') 
    #Add your channel id. For force Subscribe.
    CHANNEL = os.environ.get("CHANNEL", "-1002369984275")
    #Skip or add your proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = ''
