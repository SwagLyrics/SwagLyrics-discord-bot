import re

import discord
import env_file
from discord.ext import commands
from swaglyrics import cli as swaglyrics

bot = commands.Bot(command_prefix="$")


def get_spotify_data(user):
    return user.activity.title, user.activity.artist


@bot.command(name='swaglyrics')
async def get_lyrics(ctx):
    try:
        song, artist = get_spotify_data(ctx.author)
        debug_string = "Getting lyrics for {} - {}".format(song, artist)
        print(debug_string)
        await ctx.send(debug_string)
        lyrics = swaglyrics.get_lyrics(song, artist)
        splitted_lyrics = chop_string_into_chunks(lyrics, 1024)
        embed = discord.Embed()
        embed.title = "Lyrics for {} - {}".format(song, artist)
        for chunk in splitted_lyrics:
            embed.add_field(name=u"\u200C", value=chunk, inline=False)
        await ctx.send(embed=embed)
    except AttributeError:
        await ctx.send("You are not listening to anything or Spotify is not connected to discord! \n "
                       "Make sure you have enabled status in Settings -> Connections -> Spotify -> Display "
                       "Spotify as your status")
    except TypeError:
        await ctx.send("Lyrics for {} - {} not found in genius database.".format(song, artist))


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


async def on_ready():
    print("Bot is up and running. Waiting for actions.")


def run():
    token = env_file.get()
    bot.add_listener(on_ready)
    bot.run(token["BOT_TOKEN"])
