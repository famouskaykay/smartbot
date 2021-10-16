from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from smartbot import pbot
from pyrogram import filters
import requests
from helpers import call_back_in_filter


@pbot.on_callback_query(call_back_in_filter('meme'))
def callback_meme(_,query):
    if query.data.split(":")[1] == "next":
        query.message.delete()
        res = requests.get('https://nksamamemeapi.pythonanywhere.com').json()
        img = res['image']
        title = res['title']
        pbot.send_photo(query.message.chat.id , img , caption=title , reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Next" , callback_data="meme:next")],
        ]))

        
@pbot.on_message(filters.command('getmeme'))
def rmeme(_,message):
    res = requests.get('https://nksamamemeapi.pythonanywhere.com').json()
    img = res['image']
    title = res['title']
    pbot.send_photo(message.chat.id , img , caption=title , reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Next" , callback_data="meme:next")]
    ]))


__help__ = """
/getmeme to get memes from reddit
"""

__mod_name__ = "memes"
