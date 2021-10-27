
import os
from pyrogram import Client, filters
from pyrogram.types import *

from smartbot.config import get_str_key
from smartbot import pbot

TEXT = """👋 Hey there! My name is [xkaykaay v:2.00](https://t.me/xkaykayBot) ✨ - A powerful group management bot which can help you to manage your groups effectively as possible With powerful AI . 
Click `menu` button for more information.
Join my [news channel](https://t.me/KayAspirerProject) to get information on all the latest updates.  """

MENU = [
    [
        InlineKeyboardButton(
            text="↪️ Main menu ", callback_data="aboutmanu_back"),
    ],
]

@pbot.on_message(filters.command(["start"]))
async def tart(pbot, update):
    await update.reply_text(
        text=TEXT,
        reply_markup=MENU,
        disable_web_page_preview=True,
        quote=True
    ) 
