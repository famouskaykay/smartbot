from pyrogram import filters , Client
from smartbot import pbot as bot
from pymongo import MongoClient 
from smartbot import MONGO_DB_URI as db_url

users_db = MongoClient(db_url)['users']
col = users_db['USER']

grps = users_db['GROUPS']


@bot.on_message(filters.command("stats"))
def stats(_,message):
  users = col.find({})
  mfs = []
  for x in users:
    mfs.append(x['user_id'])
    
  total = len(mfs)
  
  grp = grps.find({})
  grps_ = []
  for x in grp:
    grps_.append(x['chat_id'])
    
  total_ = len(grps_)
  
  bot.send_message(message.chat.id , f"Total Users: {total}\nTotal Groups: {total_}")
  
__help__ = """
@famouskaykay3
 ❍ /stats 

"""


__mod_name__ = "stats"
