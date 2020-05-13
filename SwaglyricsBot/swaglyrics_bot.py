import discord
import env_file
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands.help import MinimalHelpCommand

from SwaglyricsBot import logs
from SwaglyricsBot.dev_commands import DevCommands
from SwaglyricsBot.general_commands import GeneralCommands
from SwaglyricsBot.links_commands import LinksCommands
from SwaglyricsBot.topGG import TopGG

bot = commands.Bot(command_prefix="$", help_command=MinimalHelpCommand())


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
    await bot.change_presence(activity=discord.Activity(name="you type $sl", type=3), status=discord.Status.online)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("{}. Use $help for commands.".format(error))


def run():
    """
    Bot setup
    """
    token = env_file.get()
    bot.add_cog(DevCommands(bot))
    bot.add_cog(GeneralCommands(bot))
    bot.add_cog(LinksCommands(bot))
    if 'DBL_TOKEN' in token:
        bot.add_cog(TopGG(bot, token['DBL_TOKEN']))
    if 'WEBHOOK_URL' in token:
        logs.webhook_url = token['WEBHOOK_URL']
    if 'WEBHOOK_ERROR_SUPERVISOR_ID' in token:
        logs.error_supervisor = token['WEBHOOK_ERROR_SUPERVISOR_ID']
    bot.run(token["BOT_TOKEN"])
