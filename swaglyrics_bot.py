import discord
import env_file
from discord.ext import commands
from swaglyrics import cli

from text2png import text2png

bot = commands.Bot(command_prefix="$")


@bot.command(name='swaglyrics')
async def get_lyrics(ctx, song, artist):
    lyrics = cli.get_lyrics(song, artist)
    embed = discord.Embed()
    embed.description = lyrics
    await ctx.send(embed=embed)

token = env_file.get()
bot.run(token["BOT_TOKEN"])

