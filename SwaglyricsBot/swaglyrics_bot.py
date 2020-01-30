import discord
import env_file
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands.help import MinimalHelpCommand

from SwaglyricsBot.dev_commands import DevCommands
from SwaglyricsBot.general_commands import GeneralCommands
from SwaglyricsBot.topGG import TopGG

bot = commands.Bot(command_prefix="$", help_command=MinimalHelpCommand())


def find_mutual_guild(user_id):
    for guild in bot.guilds:
        if guild.get_member(user_id):
            return guild
    return None


@bot.event
async def on_ready():
    print("Bot is up and running. Waiting for actions.")
    await bot.change_presence(activity=discord.Activity(name="you type $swaglyrics", type=3), status=discord.Status.online)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("{}. Use $help for commands.".format(error))


def run():
    token = env_file.get()
    bot.add_cog(DevCommands(bot))
    bot.add_cog(GeneralCommands(bot))
    bot.add_cog(TopGG(bot, token['DBL_TOKEN']))
    bot.run(token["BOT_TOKEN"])
