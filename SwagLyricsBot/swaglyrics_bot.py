import aiohttp
import env_file
from discord import Activity, ActivityType
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


async def run():
    """
    Bot setup
    """
    async with aiohttp.ClientSession() as session:
        token = env_file.get()
        bot.add_cog(DevCommands(bot))
        bot.add_cog(GeneralCommands(bot, session))
        bot.add_cog(LinksCommands(bot))
        if "DBL_TOKEN" in token:
            bot.add_cog(TopGG(bot, token["DBL_TOKEN"]))
        if "WEBHOOK_URL" in token:
            logs.webhook_url = token["WEBHOOK_URL"]
        if "WEBHOOK_ERROR_SUPERVISOR_ID" in token:
            logs.error_supervisor = token["WEBHOOK_ERROR_SUPERVISOR_ID"]
        await bot.start(token["BOT_TOKEN"])
