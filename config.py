import redis, re
from os import getenv
from dotenv import load_dotenv
from ESLAM import *
load_dotenv()

DURATION_LIMIT = 99999999

token = "7534360763:AAHge7fGmbGIX4O5vt34Xjmi0BKJZ1Z5lM0" # ضع هنا التوكن


Dev_Zaid = token.split(':')[0]

sudo_id = 6593071692 # ضع ايديهك

r = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)



fallendb = {}

from kvsqlite.sync import Client as DB
ytdb = DB('ytdb.sqlite')
sounddb = DB('sounddb.sqlite')
wsdb = DB('wsdb.sqlite')
