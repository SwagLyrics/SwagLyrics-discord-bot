from discord.ext import commands


class LinksCommands(commands.Cog, name="Links"):

    @commands.command(name="github")
    async def github(self, ctx):
        await ctx.send("Catch! https://github.com/SwagLyrics/SwagLyrics-discord-bot")

    @commands.command(name="topgg", aliases=["vote", "invite"])
    async def github(self, ctx):
        await ctx.send("Don't forget to vote :) https://top.gg/bot/660170175517032448")
