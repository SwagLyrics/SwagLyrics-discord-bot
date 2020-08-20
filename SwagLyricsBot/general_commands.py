import traceback
import typing
import discord
import re
from discord.ext import commands, tasks

from SwagLyricsBot import SpotifyClosed, LyricsError, ConsoleColors, NoActivityAccess, NotEnoughArguments
from SwagLyricsBot.logs import Log
from SwagLyricsBot.lyrics import get_lyrics


class GeneralCommands(commands.Cog, name="General"):

    def __init__(self, bot, session, current=None):
        if current is None:
            current = {}
        self.bot = bot
        self.session = session
        self.current = current

    @commands.command(name="help")
    async def help_message(self, ctx):
        """
        Sends help message
        """

        embed = discord.Embed(title="SwagLyrics Help", description="Thank you for using SwagLyrics! Here are the "
                                                                   "commands you can use:")

        embed.add_field(name="`$sl` or `$swaglyrics`", value='Automatically get lyrics for music you are currently '
                        'listening to on Spotify. Optionally, to get lyrics for a specific song, use '
                        '`$sl [song] [artist]`. \nEg. `$sl "In The End" "Linkin Park"`', inline=False)
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

    async def send_lyrics(self, ctx, song, artists, log):
        """
        Wrapper around get_lyrics to parse lyrics into embeds for discord.
        """
        lyrics = await get_lyrics(song, artists[0], self.session)
        print('got lyrics')
        await log.add_sub_log("Lyrics fetched successfully, splitting it into fields...")
        split_lyrics = self.chop_string_into_chunks(lyrics, 1024)
        print('split lyrics')
        await log.add_sub_log("Split successfully. Packing into messages...")

        artists_string = self.artists_to_string(artists)
        await self.send_chunks(ctx, split_lyrics, song, artists_string)
        await log.add_sub_log("Lyrics sent successfully.", ConsoleColors.OKGREEN)
        log.change_log_success_status(True)

    @commands.command(name="swaglyrics", aliases=["sl", "lyrics"])
    async def get_lyrics_command(self, ctx, member: typing.Optional[discord.Member], song=None, artists=None):
        """
        Gets lyrics for music you are currently listening to on Spotify.
        Song can be specified as command arguments.
        """
        log = Log(self.session)

        async def send_lyrics():
            lyrics = await get_lyrics(song, artists[0], self.session)
            await log.add_sub_log("Lyrics fetched successfully, splitting it into fields...")
            split_lyrics = self.chop_string_into_chunks(lyrics, 1024)
            await log.add_sub_log("Split successfully. Packing into messages...")

            await self.send_chunks(ctx, split_lyrics, song, artists_string)
            await log.add_sub_log("Lyrics sent successfully.", ConsoleColors.OKGREEN)
            log.change_log_success_status(True)

        try:
            await log.add_log(f"User {ctx.author} from {ctx.guild or ctx.channel} guild requested lyrics")

            if not (song or artists):
                if not member:
                    await log.add_sub_log("Song data not provided, trying to fetch it automatically...")
                    song, artists = self.get_spotify_data(ctx.author)
                if member:
                    song, artists = self.get_spotify_data(member) 
                    await log.add_sub_log(
                        f"Mentioned {member} & song data was not provided, trying to fetch it automatically..."
                    )
            elif artists is None:
                raise NotEnoughArguments("Not enough arguments! For usage, check `$help`")
            else:
                artists = list(artists)
            artists_string = self.artists_to_string(artists)
            debug_string = f"Getting lyrics for {song} by {artists_string}"
            await log.add_log(debug_string)
            await ctx.send(debug_string)

            await self.send_lyrics(ctx, song, artists, log)
        except LyricsError as ex:
            await log.add_sub_log(f"Error raised: {ex}", ConsoleColors.FAIL)
            log.change_log_success_status(None)
            await ctx.send(ex)
        except Exception as ex:
            await log.add_sub_log(f"Error: {ex}", ConsoleColors.FAIL, True)
            print(traceback.print_exception(type(ex), ex, ex.__traceback__))
            log.change_log_success_status(False)

            await ctx.send("There was an error while processing your request. Please try again in a few seconds. \n"
            "If the error persists, please shout at us at https://discord.swaglyrics.dev.")
        finally:
            await log.send_webhook()

    @tasks.loop(seconds=5)
    async def vibe_mode(self):
        """
        Loop to continuously send lyrics as song updates.
        Killed using $kill or no Spotify activity
        """
        log = Log(self.session)

        for user, info in self.current.items():
            try:
                song, artists = self.get_spotify_data(user)
                print(song, artists)
                if (song, artists) == info:
                    continue
                # song has changed
                self.current[user] = (song, artists)
                artists_string = self.artists_to_string(artists)
                debug_string = f"Getting lyrics for {song} by {artists_string}"
                await log.add_log(debug_string)
                await user.send(debug_string)

                await self.send_lyrics(user, song, artists, log)
            except LyricsError:
                print('No activity detected, stopping loop.')
                await user.send("No activity detected, killing the vibe.")
                del self.current[user]
                if not self.current:
                    print('stopping loop')
                    self.vibe_mode.cancel()

    @commands.command()
    async def vibe(self, ctx):
        """
        Starts vibe_mode loop if called in user DMs
        """
        # check if DMs
        if not ctx.guild:
            if ctx.author not in self.current.keys():
                # add current user to dict
                self.current[ctx.author] = (None, None)
                await ctx.send('one vibe mode coming right up.')
                if len(self.current) == 1:
                    self.vibe_mode.start()
            else:
                await ctx.send("you're already vibing ;)")
        else:
            # DMs only to prevent spam
            await ctx.send('$vibe in DMs only 👀')

    @commands.command()
    async def kill(self, ctx):
        if not ctx.guild:
            del self.current[ctx.author]
            print('killed vibe')
            await ctx.send('killed the vibe ✊🏻')
            if not self.current:
                print('stopping loop')
                self.vibe_mode.cancel()
        else:
            # DMs only to prevent spam
            await ctx.send('$kill in DMs only bb.')

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
