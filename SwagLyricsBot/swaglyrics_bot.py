import aiohttp
import env_file
from discord import Activity, ActivityType
import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from SwagLyricsBot import logs
from SwagLyricsBot.dev_commands import DevCommands
from SwagLyricsBot.general_commands import GeneralCommands
from SwagLyricsBot.links_commands import LinksCommands
from SwagLyricsBot.topGG import TopGG

bot = commands.Bot(command_prefix=when_mentioned_or("$"), help_command=None)


def find_mutual_guild(user_id):
    """
    Finds mutual guild for user and bot.
    """
    for guild in bot.guilds:
        if guild.get_member(user_id):
            return guild
    return None


@bot.event
async def on_ready():
    print("Bot is up and running. Waiting for actions.")
    await bot.change_presence(activity=Activity(type=ActivityType.watching, name="you type $sl"))


@bot.event
async def on_guild_join(guild):
    channel = guild.system_channel
    embed = discord.Embed(
        colour=0x2ecc71,
        description="""Hello, Thanks for adding SwagLyrics.
        This is an implementation of swaglyrics into a discord bot. When you listen to music on spotify, this bot will print you the lyrics. All automatic!

        If you are listining to a song on spotify, just type `$sl` and you'll automatically get the lyrics to the song.
        You can also get lyrigs by providing the song name and artist. `$sl [song] [artist]`
        Type `$help` to see all the commands you can use.
        """)
    embed.add_field(name="Useful Links", value="""Upvote **[Swaglrics](https://top.gg/bot/660170175517032448)** on Top.gg.
    Join the [Support/Development Server](https://discord.gg/j4ZMJYy)
    You can find the source code and docs on GitHub [here](https://github.com/SwagLyrics/SwagLyrics-discord-bot)
    """)
    await channel.send(embed=embed)


async def run():
    """
    Bot setup
    """
    async with aiohttp.ClientSession() as session:
        token = env_file.get()
        bot.add_cog(DevCommands(bot))
        bot.add_cog(GeneralCommands(bot, session))
        bot.add_cog(LinksCommands(bot))
        if 'DBL_TOKEN' in token:
            bot.add_cog(TopGG(bot, token['DBL_TOKEN']))
        if 'WEBHOOK_URL' in token:
            logs.webhook_url = token['WEBHOOK_URL']
        if 'WEBHOOK_ERROR_SUPERVISOR_ID' in token:
            logs.error_supervisor = token['WEBHOOK_ERROR_SUPERVISOR_ID']
        await bot.start(token['BOT_TOKEN'])
