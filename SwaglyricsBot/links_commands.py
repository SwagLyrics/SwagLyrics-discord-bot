from discord.ext import commands


class LinksCommands(commands.Cog, name="Links"):

    @commands.command(name="github")
    async def github(self, ctx):
        """
        Sends bot github link
        """
        await ctx.send("Catch! https://github.com/SwagLyrics/SwagLyrics-discord-bot")

    @commands.command(name="topgg", aliases=["invite"])
    async def topgg(self, ctx):
        """
        Sends bot topGG link
        """
        await ctx.send("Don't forget to vote :) https://top.gg/bot/660170175517032448")

    @commands.command(name="vote")
    async def topgg(self, ctx):
        """
        Sends bot topGG link
        """
        await ctx.send("Thank you <3 https://top.gg/bot/660170175517032448")
