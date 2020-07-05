import traceback

import discord
import re
from discord.ext import commands

from SwagLyricsBot import SpotifyClosed, LyricsError, ConsoleColors, NoActivityAccess, NotEnoughArguments
from SwagLyricsBot.logs import Log
from SwagLyricsBot.lyrics import get_lyrics


class GeneralCommands(commands.Cog, name="General"):

    def __init__(self, bot, session):
        self.bot = bot
        self.session = session

    @commands.command(name="help")
    async def help_message(self, ctx):
        """
        Sends help message
        """

        embed = discord.Embed(title="SwagLyrics Help", description="Thank you for using SwagLyrics! Here are the "
                                                                   "commands you can use:")

        embed.add_field(name="`$sl` or `$swaglyrics`", value='Automatically get lyrics for music you are currently '
                        'listening to on Spotify. Optionally, to get lyrics for a specific song, use '
                        '`$sl [song] [artist]`. \nE.g. `$sl "In The End" "Linkin Park"`', inline=False)
        embed.add_field(name="`$invite` or `$topgg`", value="Link to the bot's top.gg page", inline=False)
        embed.add_field(name="`$vote`", value="Link to the bot's top.gg page but nicer", inline=False)
        embed.add_field(name="`$help`", value="Show this message", inline=False)
        embed.add_field(name="`$github`", value="Link to the bot's source code", inline=False)
        embed.add_field(name="`$ping`", value="Check bot latency", inline=False)
        embed.set_footer(text="just try $sl when playing something on Spotify :P")

        await ctx.send(embed=embed)

    @staticmethod
    def get_spotify_data(user):
        from SwagLyricsBot.swaglyrics_bot import find_mutual_guild
        """
        Reads data from discord spotify activity. 
        """
        if user.dm_channel:
            print("    - Command was raised in DM, finding mutual guild with user...")
            guild = find_mutual_guild(user.id)
            if guild:
                print(f"    - User found in {guild} guild!")
                user = guild.get_member(user.id)
            else:
                print("    - User was not found in any guild.")
                raise NoActivityAccess("I can't access your Spotify data. Make sure to be a member of guild I belong "
                                       "to. Feel free to join our official server https://discord.swaglyrics.dev")

        # read spotify activity if exists
        spotify_activity = [activity for activity in user.activities if isinstance(activity, discord.Spotify)]
        if len(spotify_activity) == 0 or spotify_activity is None:
            raise SpotifyClosed()
        return spotify_activity[0].title, spotify_activity[0].artists

    @commands.command(name="swaglyrics", aliases=["sl", "lyrics"])
    async def get_lyrics_command(self, ctx, song=None, artists=None):
        """
        Gets lyrics for music you are currently listening to on Spotify.
        Song can be specified as command arguments.
        """
        log = Log()

        async def send_lyrics():
            lyrics = await get_lyrics(song, artists[0], self.session)
            await log.add_sub_log("Lyrics fetched successfully, splitting it into fields...")
            split_lyrics = self.chop_string_into_chunks(lyrics, 1024)
            await log.add_sub_log("Split successfully. Packing into messages...")

            await self.send_chunks(ctx, split_lyrics, song, artists_string)
            await log.add_sub_log(f"Lyrics sent successfully.", ConsoleColors.OKGREEN)
            log.change_log_success_status(True)

        try:

            await log.add_log(
                f"User {ctx.author} from {ctx.guild or ctx.channel} guild requested lyrics"
            )

            if not (song or artists):
                await log.add_sub_log("Song data not provided, trying to fetch it automatically...")
                song, artists = self.get_spotify_data(ctx.author)
            elif artists is None:
                raise NotEnoughArguments("Not enough arguments! For usage, check `$help`")
            else:
                tmp = artists
                artists = list()
                artists.append(tmp)
            artists_string = self.artists_to_string(artists)
            debug_string = f"Getting lyrics for {song} by {artists_string}"
            await log.add_sub_log(debug_string)
            await ctx.send(debug_string)

            await send_lyrics()
        except LyricsError as ex:
            await log.add_sub_log(f"Error raised: {ex}", ConsoleColors.FAIL)
            log.change_log_success_status(None)
            await ctx.send(ex)
        except Exception as ex:
            await log.add_sub_log(f"Error: {ex}", ConsoleColors.FAIL, True)
            print(traceback.print_exception(type(ex), ex, ex.__traceback__))
            log.change_log_success_status(False)
            await ctx.send(f"There was an error while processing your request. Please try again in a few seconds.")
        finally:
            await log.send_webhook()

    async def send_chunks(self, ctx, chunks, song, artists):
        messages = self.pack_into_messages(chunks)
        i = 0
        for message in messages:
            embed = discord.Embed()
            embed.title = f"{song} by {artists}" if i == 0 else ""
            for chunk in message:
                embed.add_field(name=u"\u200C", value=chunk, inline=False)
            await ctx.send(embed=embed)
            i += 1

    @staticmethod
    def pack_into_messages(chunks):
        """
        Splits chunks into separate messages, discord limits one message to 6000 chars.
        """
        messages = [[]]
        i = 0
        for chunk in chunks:
            # if sum of chars in message + chunk length exceeds limit
            if sum(len(j) for j in messages[i]) + len(chunk) > 6000:
                i += 1
                messages.append([])
            messages[i].append(chunk)
        return messages

    @staticmethod
    def artists_to_string(artists):
        """
        Converts list of artists into human friendly string
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
    def chop_string_into_chunks(string, chunk_size):
        """
        Chops lyrics into chunks no longer than 1024 characters.
        Discord embed section can't be longer than that.
        To avoid breaks mid word, it chops to first gap between lyrics sections.
        """
        chunk = ""
        chunks = list()
        last_char = None
        only_new_lines = r'^(\n)+$'
        for char in string:
            if len(chunk) + 150 > chunk_size and char == "\n" or (last_char == "\n" and char == "\n"):
                # In case of 3 or more newlines, and ignore chunks with only newlines
                if len(chunk) > 1 and not re.match(only_new_lines, chunk):
                    chunks.append(chunk)
                    chunk = ""
            chunk += char
            last_char = char
        chunks.append(chunk)
        return chunks
