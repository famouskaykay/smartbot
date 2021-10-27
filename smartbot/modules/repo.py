import os
from pyrogram import Client, filters
from pyrogram.types import *

from smartbot.config import get_str_key
from smartbot import pbot

REPO_TEXT = "xkaykay v2.0 is not open source join support for updates. powered by @famouskaykay3 "
  
BUTTONS = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("💠 Repository for xkaykay v1💠", url=f"https://github.com/famousaykay/raiya"),
        InlineKeyboardButton("💠support group💠", url=f"https://t.me/KayAspirerProject"),
      ]]
    )
  
  
@pbot.on_message(filters.command(["repo"]))
async def repo(pbot, update):
    await update.reply_text(
        text=REPO_TEXT,
        reply_markup=BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )
