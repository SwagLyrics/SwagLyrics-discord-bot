import datetime

import discord
import swaglyrics.cli as swaglyrics
from discord.ext import commands

from SwaglyricsBot import SpotifyClosed, LyricsNotFound, LyricsError, ConsoleColors, NoActivityAccess


class GeneralCommands(commands.Cog, name="General"):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_spotify_data(user):
        from SwaglyricsBot.swaglyrics_bot import find_mutual_guild
        """
        Reads data from discord spotify activity.
        """
        if user.dm_channel:
            print("    - Command was raised in DM, finding mutual guild with user...")
            guild = find_mutual_guild(user.id)
            if guild:
                print("    - User found in {} guild!".format(guild))
                user = guild.get_member(user.id)
            else:
                print("    - User was not found in any guild.")
                raise NoActivityAccess("I can't access your Spotify data. Make sure to be a member of guild I belong "
                                       "to. Feel free to join our official server https://discord.gg/mJ44Bvj")

        spotify_activity = [activity for activity in user.activities if isinstance(activity, discord.Spotify)]
        if len(spotify_activity) == 0 or spotify_activity is None:
            raise SpotifyClosed()
        return spotify_activity[0].title, spotify_activity[0].artists

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        Checks bot latency.
        """
        await ctx.send(f"Pong {self.bot.latency * 1000:.03f} ms")

    @commands.command(name="swaglyrics")
    async def get_lyrics_command(self, ctx, song=None, artists=None):
        """
        Gets lyrics for music you are currently listening to on Spotify.
        Song can be specified as command arguments.
        """
        try:
            print("{}: User {} from {} guild requested lyrics".format(
                datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                ctx.author, ctx.guild if ctx.guild else ctx.channel))
            if song is None and artists is None:
                print("    - Song data not provided, trying to fetch it automatically...")
                song, artists = self.get_spotify_data(ctx.author)
            else:
                tmp = artists
                artists = list()
                artists.append(tmp)
            artists_string = self.artists_to_string(artists)
            debug_string = "Getting lyrics for {} by {}".format(song, artists_string)
            print("    - ", debug_string)
            await ctx.send(debug_string)
            lyrics = self.get_lyrics(song, artists[0])
            print("    - Lyrics fetched successfully, splitting it into fields...")
            splitted_lyrics = self.chop_string_into_chunks(lyrics, 1024)
            print("    - Splitted successfully.")
            embed = discord.Embed()
            embed.title = "{} by {}".format(song, artists_string)
            for chunk in splitted_lyrics:
                embed.add_field(name=u"\u200C", value=chunk, inline=False)
            await ctx.send(embed=embed)
            print(f"{ConsoleColors.OKGREEN}    - Lyrics sent successfully!{ConsoleColors.ENDC}")
        except LyricsError as ex:
            print(f"    - {ConsoleColors.FAIL}Error raised: {ex}{ConsoleColors.ENDC}")
            await ctx.send(ex)

    @staticmethod
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

    @staticmethod
    def get_lyrics(song, artist):
        lyrics = swaglyrics.get_lyrics(song, artist)
        if lyrics is None:
            raise LyricsNotFound("Lyrics for {} - {} not found in genius database.".format(song, artist))
        return lyrics

    @staticmethod
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
