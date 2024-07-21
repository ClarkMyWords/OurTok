from __future__ import annotations
import discord
from discord.ext import commands
import asyncio
import yt_dlp
import logging
import os
from urllib.parse import urlparse


def from_url(url):
    ydl_format_options = {
        "format": "bestaudio/best",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
    }
    with yt_dlp.YoutubeDL(ydl_format_options) as ydl:
        info = ydl.extract_info(url)
        file = info["requested_downloads"][0]["filepath"]

    return file


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot: commands.Bot
bot = commands.Bot(intents=intents, command_prefix="<><>")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("-------------------------------------------")


@bot.event
async def on_message(msg):
    reply_content = []
    msg_parts = msg.content.split()
    for part in msg_parts:
        parsed = urlparse(part)
        if parsed.scheme != "":
            if "tiktok" in parsed.netloc and parsed.path != "":
                reply_content.append(from_url(part))

    if len(reply_content) > 0:
        for reply in reply_content:
            await msg.reply(file=discord.File(reply))
            try:
                os.remove(reply)
            except Exception as e:
                print(f"Error removing file {reply}:")
                print(f"{e}\n")


async def main():
    discord.utils.setup_logging(level=logging.INFO, root=False)

    with open("Token.txt", "r", encoding="utf-8") as fp:
        token = fp.read()

    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
