import discord
import env_file
from discord import Spotify
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands.help import MinimalHelpCommand
from swaglyrics import cli as swaglyrics

from SwaglyricsBot import LyricsNotFound, SpotifyClosed, LyricsError
from SwaglyricsBot.dev_commands import DevCommands

bot = commands.Bot(command_prefix="$", help_command=MinimalHelpCommand())


def get_spotify_data(user):
    """
    Reads data from discord spotify activity.
    """
    spotify_activity = [activity for activity in user.activities if isinstance(activity, Spotify)]
    if len(spotify_activity) == 0:
        raise SpotifyClosed()
    return spotify_activity[0].title, spotify_activity[0].artists


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong {bot.latency * 1000:.03f} ms")


@bot.command(name="swaglyrics")
async def get_lyrics_command(ctx, song=None, artists=None):
    """
    Main command, get's lyrics, chops it into pieces and generates embed,
    that will be sent to discord.
    """
    try:
        if song is None and artists is None:
            song, artists = get_spotify_data(ctx.author)
        else:
            tmp = artists
            artists = list()
            artists.append(tmp)
        artists_string = artists_to_string(artists)
        debug_string = "Getting lyrics for {} by {}".format(song, artists_string)
        print("User: {}".format(ctx.author), debug_string)
        await ctx.send(debug_string)
        lyrics = get_lyrics(song, artists[0])
        splitted_lyrics = chop_string_into_chunks(lyrics, 1024)
        embed = discord.Embed()
        embed.title = "{} by {}".format(song, artists_string)
        for chunk in splitted_lyrics:
            embed.add_field(name=u"\u200C", value=chunk, inline=False)
        await ctx.send(embed=embed)
    except LyricsError as ex:
        await ctx.send(ex)


def artists_to_string(artists):
    """
    List of artists into human friendly string
    """
    if len(artists) == 0:
        return ""
    str1 = artists[0]
    for artist in artists:
        if artist == str1:
            continue
        str1 += ", " + artist
    return str1


def get_lyrics(song, artist):
    lyrics = swaglyrics.get_lyrics(song, artist)
    if lyrics is None:
        raise LyricsNotFound("Lyrics for {} - {} not found in genius database.".format(song, artist))
    return lyrics


def chop_string_into_chunks(string, chunk_size):
    """
    Chops lyrics into chunks no longer than 1024 characters.
    Discord embed section can't be longer than that.
    To avoid breaks mid word, it chops to first gap between lyrics sections
    """
    chunk = ""
    chunks = list()
    last_char = None
    for char in string:
        if len(chunk) + 150 > chunk_size and char == "\n" or (last_char == "\n" and char == "\n"):
            chunks.append(chunk)
            chunk = ""
        chunk += char
        last_char = char
    chunks.append(chunk)
    return chunks


@bot.event
async def on_ready():
    print("Bot is up and running. Waiting for actions.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("{}. Use $help for commands.".format(error))


def run():
    token = env_file.get()
    bot.add_cog(DevCommands(bot))
    bot.run(token["BOT_TOKEN"])
