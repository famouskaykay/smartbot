from typing import Union, List

from pyrogram import filters

from os import name
from pyrogram.methods import messages
from smartbot import pbot , help_message
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton , InlineKeyboardMarkup


other_filters = filters.group & ~filters.edited & ~filters.via_bot & ~filters.forwarded
other_filters2 = filters.private & ~filters.edited & ~filters.via_bot & ~filters.forwarded


def command(commands: Union[str, List[str]]):
    return filters.command(commands)


def call_back_in_filter(data):
    return filters.create(
        lambda flt, _, query: flt.data in query.data,
        data=data
    )
