import re

import discord
import env_file
from discord.ext import commands
from swaglyrics import cli as swaglyrics

from text2png import text2png

bot = commands.Bot(command_prefix="$")


def get_spotify_data(user):
    return user.activity.artist, user.activity.title


@bot.command(name='swaglyrics')
async def get_lyrics(ctx):
    song, artist = get_spotify_data(ctx.author)
    lyrics = swaglyrics.get_lyrics(song, artist)
    splitted_lyrics = chop_string_into_chunks(lyrics, 1024)
    embed = discord.Embed()
    embed.title = "Lyrics for {} - {}".format(song, artist)
    for chunk in splitted_lyrics:
        embed.add_field(name=u"\u200C", value=chunk, inline=False)
    await ctx.send(embed=embed)


def chop_string_into_chunks(string, chunk_size):
    chunk = ""
    chunks = list()
    last_char = None
    for char in string:
        if len(chunk) + 50 > chunk_size and char == "\n" or last_char == "\n" and char == "\n":
            chunks.append(chunk)
            chunk = ""
        chunk += char
        last_char = char
    chunks.append(chunk)
    return chunks


def remove_titles(lyrics, titles):
    titles = re.findall(r'\[(.*)\]', lyrics)
    for title in titles:
        lyrics = lyrics.replace("[{}]".format(title), "")
    return lyrics


token = env_file.get()
bot.run(token["BOT_TOKEN"])
