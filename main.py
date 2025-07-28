import time, redis, os, json, re, requests, asyncio 
from pyrogram import *
import redis, re
from config import *
from con import *
from pyrogram.types import *


print('''
Loading…
█▒▒▒▒▒▒▒▒▒''')
print('\n\n')




if not r.get(f'{Dev_Zaid}botowner'):
    owner_id = int(sudo_id)
    r.set(f'{Dev_Zaid}botowner', owner_id)
    r.set(f'{Dev_Zaid}dev-eslam', 6593071692)
else:
    owner_id = int(r.get(f'{Dev_Zaid}botowner'))
print('''
10% 
███▒▒▒▒▒▒▒ ''')


print('''
30% 
█████▒▒▒▒▒ ''')

print('''
50% 
███████▒▒▒ ''')

if not r.get(f'{Dev_Zaid}:botkey'):
    r.set(f'{Dev_Zaid}:botkey', '⇜')

if not r.get(f'{Dev_Zaid}:botphpv'):
    r.set(f'{Dev_Zaid}:botphpv', 'https://t.me/Ids_Holder/4')

if not r.get(f'{Dev_Zaid}botname'):
    r.set(f'{Dev_Zaid}botname', 'سيد')

if not r.get(f'{Dev_Zaid}botchannel'):
    r.set(f'{Dev_Zaid}botname', 'BeroBots')

def Find(text):
  m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
  url = re.findall(m,text)  
  return [x[0] for x in url]
  
# @app.on_message(filters.group & filters.regex("^انستا "), group=-1)
# async def instaDownlo(c,m):
#   if not r.get(f'{m.chat.id}:disableINSTA:{Dev_Zaid}') and Find(m.text):
#     url = Find(m.text)[0]
#     rep = await m.reply("...")
#     await m.reply_chat_action(enums.ChatAction.TYPING)
#     msg = await userbot.send_message("instasavegrambot", url)
#     await rep.edit("Wait ...")
#     await asyncio.sleep(20)
#     await m.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
#     msg = await userbot.get_messages("instasavegrambot",msg.id+1)
#     await rep.delete()
#     if msg.media_group_id:
#        r.set("media:insta", f"{m.chat.id}&&&{m.id}", ex=10)
#        msg = await userbot.copy_media_group("iwwbot", "instasavegrambot",msg.id)
#     else:
#        msg = await msg.download("./")
#        try:
#           return await m.reply_video(msg)
#        except:
#           pass
#        try:
#           return await m.reply_animation(msg)
#        except:
#           pass
       
#        try:
#           return await m.reply_photo(msg)
#        except:
#           pass
       
#        try:
#           return await m.reply_document(msg)
#        except:
#           pass
#        os.remove(msg)
    
     
# @app.on_message(filters.private & filters.user(1920230442))
# async def mediagCopy(c,m):
#    if r.get("media:insta") and m.media_group_id:
#       chat_id = r.get("media:insta").split("&&&")[0]
#       id = r.get("media:insta").split("&&&")[1]
#       await c.copy_media_group(int(chat_id), m.from_user.id, m.id,reply_to_message_id=int(id))
#       r.delete("media:insta")
      

print('''

 ____        _   _       ____       _____        _    
/ ___|  ___ | | | |_ __ / ___|___  | ____|_   __/ \   
\___ \ / _ \| | | | '__| |   / _ \ |  _| \ \ / / _ \  
 ___) | (_) | |_| | |  | |__|  __/ | |___ \ V / ___ \ 
|____/ \___/ \___/|_|   \____\___| |_____| \_/_/   \_\

                                                      ''')

app.start()


if int(r.get(f'{Dev_Zaid}dev-eslam')):
  id = int(r.get(f'{Dev_Zaid}botowner'))
  get = app.get_chat(id)
  reply_markup= InlineKeyboardMarkup (
       [[InlineKeyboardButton (get.first_name, user_id=id)]]
     )
app.send_message(int(r.get(f'{Dev_Zaid}botowner')), """𝐒𝐎𝐔𝐑𝐂𝐄 𝐄𝐕𝐀 𝐈𝐒 𝐖𝐎𝐑𝐊𝐈𝐍𝐆 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘 ✔️\n𝐂𝐇 𝐒𝐎𝐔𝐑𝐂𝐄: @BeroBots\n𝐃𝐄𝐕: @aSBSsSa""")

idle()
  
