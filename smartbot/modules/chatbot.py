from motor import motor_asyncio
from odmantic import AIOEngine
from pymongo import MongoClient
import re
import aiohttp
import requests
import asyncio
import os

from pyrogram import filters
from time import time
from smartbot import pbot as bot
from smartbot import SUPPORT_CHAT

MONGO_URL = os.environ.get('MONGO_DB_URI')
MONGO_DB =  'CHATBOT'
mongodb = MongoClient(MONGO_URL)["CHATBOT"]


kukidb = mongodb['CHATS']


async def is_kuki(chat_id: int) -> bool:
    ai = await kukidb.find_one({"chat_id": chat_id})
    if not ai:
        return False
    return True


async def set_kuki(chat_id: int):
    kukichat = await is_kuki(chat_id)
    if kukichat:
        return
    return await kukidb.insert_one({"chat_id": chat_id})


async def rm_kuki(chat_id: int):
    kukichat = await is_kuki(chat_id)
    if not kukichat:
        return
    return await kukidb.delete_one({"chat_id": chat_id})


BOT_ID = os.environ.get('BOT_ID')

@bot.on_message(
    filters.command(["addchat", f"addchat@xkaykaybot"])
)
async def addchat(_, message):
    chatk = message.chat.id
    await set_kuki(chatk)
    await message.reply_text(
        f"Enabled Chatbot"
        )

    
@bot.on_message(
    filters.command(["rmchat", f"rmchat@xkaykay"])
)
async def addchat(_, message):
    chatk = message.chat.id
    await rm_kuki(chatk)
    await message.reply_text(
        f"Disable Chatbot"
        )

@bot.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited
    & ~filters.via_bot
    & ~filters.forwarded,
    group=2,
)
async def kuki(_, message):
    try:
        chatk = message.chat.id
        if not await is_kuki(chatk):
            return
        if not message.reply_to_message:
            return
        try:
            moe = message.reply_to_message.from_user.id
        except:
            return
        if moe != BOT_ID:
            return
        text = message.text
        Kuki = requests.get(f"https://www.kukiapi.xyz/api/apikey=KUKIwrLK87gL6/kuki/moezilla/message={text}").json()
        kay = f"{Kuki['reply']}"
        if "xkaykay" in text or "kakay" in text or "kay" in text:
            await bot.send_chat_action(message.chat.id, "typing")
        
        await message.reply_text(kay)
    
    except Exception as e:
        await bot.send_message(SUPPORT_CHAT, f"error in chatbot api:\n\n{e}")
