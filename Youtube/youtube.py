# ©️ Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ | @ftmdeveloperz | @ftmbotzx | ғᴛᴍ ᴛᴜʙᴇғᴇᴛᴄʜ

# [⚠️ Do not remove credits ⚠️] :- https://t.me/ftmdeveloperz

import os
import logging
import asyncio
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Youtube.config import Config
from Youtube.forcesub import handle_force_subscribe

youtube_dl_username = None  
youtube_dl_password = None 

@Client.on_message(filters.regex(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'))
async def process_youtube_link(client, message):
    if Config.CHANNEL:
        fsub = await handle_force_subscribe(client, message)
        if fsub == 400:
            return
    youtube_link = message.text
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Best Video", callback_data=f"download|best_video|{youtube_link}")],
        [InlineKeyboardButton("🎶 Best Audio", callback_data=f"download|best_audio|{youtube_link}")],
        [InlineKeyboardButton("🔹 144p", callback_data=f"download|144p|{youtube_link}"), InlineKeyboardButton("🔹 240p", callback_data=f"download|240p|{youtube_link}")],
        [InlineKeyboardButton("🔹 360p", callback_data=f"download|360p|{youtube_link}"), InlineKeyboardButton("🔹 480p", callback_data=f"download|480p|{youtube_link}")],
        [InlineKeyboardButton("🔹 540p", callback_data=f"download|540p|{youtube_link}"), InlineKeyboardButton("🔹 720p", callback_data=f"download|720p|{youtube_link}")],
        [InlineKeyboardButton("🔸 1080p", callback_data=f"download|1080p|{youtube_link}"), InlineKeyboardButton("🔸 2K", callback_data=f"download|2k|{youtube_link}")],
        [InlineKeyboardButton("🔺 4K", callback_data=f"download|4k|{youtube_link}"), InlineKeyboardButton("📂 3GP", callback_data=f"download|3gp|{youtube_link}")],
        [InlineKeyboardButton("🎵 32kbps", callback_data=f"download|32kbps|{youtube_link}"), InlineKeyboardButton("🎵 64kbps", callback_data=f"download|64kbps|{youtube_link}")],
        [InlineKeyboardButton("🎵 128kbps", callback_data=f"download|128kbps|{youtube_link}"), InlineKeyboardButton("🎵 192kbps", callback_data=f"download|192kbps|{youtube_link}")]
    ])
    
    await message.reply_text("🔍 **Select a Format to Download**", reply_markup=keyboard)

@Client.on_callback_query(filters.regex(r'^download\|'))
async def handle_download_button(client, callback_query):
    quality, youtube_link = callback_query.data.split('|')[1:]
    
    quality_format = {
        'best_video': 'bestvideo+bestaudio/best',
        'best_audio': 'bestaudio/best',
        '144p': 'bestvideo[height<=144]+bestaudio/best[height<=144]',
        '240p': 'bestvideo[height<=240]+bestaudio/best[height<=240]',
        '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        '540p': 'bestvideo[height<=540]+bestaudio/best[height<=540]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '2k': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
        '4k': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
        '3gp': '3gp',
        '32kbps': 'bestaudio[abr<=32]',
        '64kbps': 'bestaudio[abr<=64]',
        '128kbps': 'bestaudio[abr<=128]',
        '192kbps': 'bestaudio[abr<=192]'
    }.get(quality, 'best')

    try:
        downloading_msg = await callback_query.message.reply_text("📥 **Downloading Video...**")

        ydl_opts = {
            'format': quality_format,
            'outtmpl': 'downloaded_video_%(id)s.%(ext)s',
            'progress_hooks': [lambda d: print(d['status'])],
            'cookiefile': 'cookies.txt'
        }

        if Config.HTTP_PROXY:
            ydl_opts['proxy'] = Config.HTTP_PROXY
        if youtube_dl_username:
            ydl_opts['username'] = youtube_dl_username
        if youtube_dl_password:
            ydl_opts['password'] = youtube_dl_password

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_link, download=False)
            title = info_dict.get('title', 'YouTube Video')

            ydl.download([youtube_link])
            uploading_msg = await callback_query.message.reply_text("📤 **Uploading Video...**")
            video_filename = f"downloaded_video_{info_dict['id']}.mp4"

            await client.send_video(callback_query.message.chat.id, video=open(video_filename, 'rb'), caption=f"🎬 **{title}**")

            await downloading_msg.delete()
            await uploading_msg.delete()

            await callback_query.message.reply_text("✅ **Successfully Uploaded!**")

    except Exception as e:
        logging.exception("Error processing YouTube link: %s", e)
        await callback_query.message.reply_text("❌ **Error: Failed to process the YouTube link. Please try again later.**")
