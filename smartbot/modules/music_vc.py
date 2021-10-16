import os, asyncio, pafy, youtube_dl
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from musicplayer.kay import video_info_extract, yt_video_search, match_url, ADMINS
from smartbot import SUPPORT_CHAT
from smartbot import pbot as kaykay


group_call = GroupCallFactory(kaykay).get_group_call()
music_queue = []
vc_live = False

#plays music only in support chat
async def play_or_queue(status, data=None):
    global music_queue, group_call
    if not group_call.is_connected:
        await group_call.join(SUPPORT_CHAT)
    if status == "add":
        if len(music_queue) == 0:
            music_queue.append(data)
            if data['TYPE'] == "audio":
                await group_call.start_audio(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Playing...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}
            elif data['TYPE'] == "video":
                await group_call.start_video(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Streaming...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}
        elif len(music_queue) > 0:
            music_queue.append(data)
            return {"status":"queue", "msg":f"🚩 __Queued at {len(music_queue)-1}__"}
    elif status == "check":
        if len(music_queue) == 0:
            await group_call.stop()
            return {"status":"empty", "msg":"💬 __Queue empty. Leaving...__"}
        elif len(music_queue) > 0:
            data = music_queue[0]
            if data['TYPE'] == "audio":
                await group_call.start_audio(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Playing...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}
            elif data['TYPE'] == "video":
                await group_call.start_video(data['LOCAL_FILE'], repeat=False)
                return {"status":"play", "msg":f"🚩 __{data['VIDEO_TITLE']} is Streaming...__\n**Duration:** `{data['VIDEO_DURATION']}`", "thumb":data['THUMB_URL']}
              
              
@Client.on_message(filters.command("endvc", "x"))
async def leave_vc(client, message):
    global vc_live
    if not message.chat.id == SUPPORT_CHAT: return
    if not message.from_user.id in ADMINS: return
    await group_call.stop()
    vc_live = False
    music_queue.clear()
    await message.reply_sticker("CAADBQADCAMAAtFreFVNNKAMgNe-YwI")
    
@Client.on_message(filters.command("play", "x"))
async def play_vc(client, message):
    global vc_live
    if not message.chat.id == SUPPORT_CHAT return
    msg = await message.reply("⏳ __Please wait.__")
    if vc_live == True:
        return await msg.edit("💬 __Live or Radio Ongoing. Please stop it via `!endvc`.__")
    media = message.reply_to_message
    THUMB_URL, VIDEO_TITLE, VIDEO_DURATION = "https://appletld.com/wp-content/uploads/2020/10/E3593D8D-6F1C-4A16-B065-2154ED6B2355.png", "Music", "Not Found"
    if media and media.media:
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = await client.download_media(media)
    else:
        try: INPUT_SOURCE = message.text.split(" ", 1)[1]
        except IndexError: return await msg.edit("🔎 __Give me a URL or Search Query. Look__ `!help`")
        if ("youtube.com" in INPUT_SOURCE) or ("youtu.be" in INPUT_SOURCE):
            FINAL_URL = INPUT_SOURCE
        else:
            FINAL_URL = yt_video_search(INPUT_SOURCE)
            if FINAL_URL == 404:
                return await msg.edit("__No videos found__ 🤷‍♂️")
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE, THUMB_URL, VIDEO_TITLE, VIDEO_DURATION = video_info_extract(FINAL_URL, key="audio")
        if LOCAL_FILE == 500: return await msg.edit("__Download Error.__ 🤷‍♂️")
         
    try:
        post_data = {'LOCAL_FILE':LOCAL_FILE, 'THUMB_URL':THUMB_URL, 'VIDEO_TITLE':VIDEO_TITLE, 'VIDEO_DURATION':VIDEO_DURATION, 'TYPE':'audio'}
        resp = await play_or_queue("add", post_data)
        if resp['status'] == 'queue':
            await msg.edit(resp['msg'])
        elif resp['status'] == 'play':
            await msg.delete()
            await message.reply_photo(resp['thumb'], caption=resp['msg'])
    except Exception as e:
        await message.reply(str(e))
        return await group_call.stop()
      
      
@Client.on_message(filters.command("skip", "!"))
async def skip_vc(client, message):
    if not message.chat.id == SUPPORT_CHAT: return
    if not message.from_user.id in ADMINS: return
    if len(music_queue) == 0: return await message.reply("💬 __Nothing in queue.__")
    if group_call.is_video_running:
        await group_call.stop_media()
    elif group_call.is_audio_running:
        await group_call.stop_media()
    elif group_call.is_running:
        await group_call.stop_media()
    os.remove(music_queue[0]['LOCAL_FILE'])
    music_queue.pop(0)
    resp = await play_or_queue("check")
    if resp['status'] == 'empty':
        await message.reply(resp['msg'])
    elif resp['status'] == 'play':
        await message.reply_photo(resp['thumb'], caption=resp['msg'])
    
