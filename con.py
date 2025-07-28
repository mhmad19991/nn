import time, redis, os, json, re, requests, asyncio 
from pyrogram import *
from config import *

import asyncio
import logging
import os
import time

from pyrogram import Client, filters


StartTime = time.time()
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("fallenlogs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

LOGGER = logging.getLogger("cv7bfd")


app = Client(f'{Dev_Zaid}r3d', 21079596, 'a9d1ebbcfe46988d32445256019e926e',
  bot_token=token,
    plugins={"root": "Plugins"},
  )

  
