import re

import discord
import env_file
from discord import Spotify
from discord.ext import commands
from discord.ext.commands.help import MinimalHelpCommand
from swaglyrics import cli as swaglyrics
from SwaglyricsBot import LyricsNotFound, SpotifyClosed, LyricsError

bot = commands.Bot(command_prefix="$", help_command=MinimalHelpCommand())


def get_spotify_data(user):
    spotify_activity = [activity for activity in user.activities if isinstance(activity, Spotify)]
    if len(spotify_activity) == 0:
        raise SpotifyClosed()
    return spotify_activity[0].title, spotify_activity[0].artist


@bot.command(name='swaglyrics')
async def get_lyrics_command(ctx, song=None, artist=None):
    try:
        if song is None and artist is None:
            song, artist = get_spotify_data(ctx.author)
        debug_string = "Getting lyrics for {} - {}".format(song, artist)
        print(debug_string)
        await ctx.send(debug_string)
        lyrics = get_lyrics(song, artist)
        splitted_lyrics = chop_string_into_chunks(lyrics, 1024)
        embed = discord.Embed()
        embed.title = "Lyrics for {} - {}".format(song, artist)
        for chunk in splitted_lyrics:
            embed.add_field(name=u"\u200C", value=chunk, inline=False)
        await ctx.send(embed=embed)
    except LyricsError as ex:
        await ctx.send(ex)


def get_lyrics(song, artist):
    lyrics = swaglyrics.get_lyrics(song, artist)
    if lyrics is None:
        raise LyricsNotFound("Lyrics for {} - {} not found in genius database.".format(song, artist))
    return lyrics


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

