import os

import aiohttp
from discord import Activity, ActivityType, AllowedMentions, Intents
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from dotenv import load_dotenv

from SwagLyricsBot import logs
from SwagLyricsBot.dev_commands import DevCommands
from SwagLyricsBot.general_commands import GeneralCommands
from SwagLyricsBot.links_commands import LinksCommands
from SwagLyricsBot.topGG import TopGG

load_dotenv()  # load env vars

intents = Intents.default()
intents.presences = True

bot = commands.Bot(
    command_prefix=when_mentioned_or("$"), help_command=None, intents=intents, allowed_mentions=AllowedMentions.none()
)


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


async def run():
    """
    Bot setup
    """
    async with aiohttp.ClientSession() as session:
        bot.add_cog(DevCommands(bot))
        bot.add_cog(GeneralCommands(bot, session))
        bot.add_cog(LinksCommands(bot))
        if os.getenv("DBL_TOKEN"):
            bot.add_cog(TopGG(bot, os.getenv("DBL_TOKEN")))
        logs.webhook_url = os.getenv("WEBHOOK_URL")  # None if not set
        logs.error_supervisor = os.getenv("WEBHOOK_ERROR_SUPERVISOR_ID")
        await bot.start(os.environ["BOT_TOKEN"])
