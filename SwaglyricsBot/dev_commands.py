import os
import time
from datetime import timedelta

import discord
import psutil as psutil
from discord.ext import commands


class DevCommands(commands.Cog, name="Dev"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats")
    async def view_stats(self, ctx):
        """
        Returns bot statistics and technical data.
        """
        app_info = await self.bot.application_info()
        process = psutil.Process(os.getpid())
        total_ram = (psutil.virtual_memory().total >> 30) + 1
        embed = discord.Embed(
            title="Bot Stats",
            description="Running on a dedicated server with {}GB RAM.".format(total_ram))
        embed.add_field(name="**__General Info__**", inline=False, value="\u200b")
        embed.add_field(
            name="Owner",
            value=f"{app_info.owner.name}#{app_info.owner.discriminator}")
        embed.add_field(name="Latency", value=f"{self.bot.latency*1000:.03f} ms")
        embed.add_field(name="Guild Count", value=f"{len(self.bot.guilds):,}")
        embed.add_field(name="User Count", value=f"{len(self.bot.users):,}")
        embed.add_field(name="**__Technical Info__**", inline=False, value="\u200b")
        embed.add_field(name="System CPU Usage", value=f"{psutil.cpu_percent():.02f}%")
        embed.add_field(name="System RAM Usage",
                        value=f"{psutil.virtual_memory().used/1048576:.02f} MB")
        embed.add_field(name="System Uptime",
                        value=str(timedelta(seconds=int(time.time()-psutil.boot_time()))))
        embed.add_field(name="Bot CPU Usage", value=f"{process.cpu_percent():.02f}%")
        embed.add_field(name="Bot RAM Usage", value=f"{process.memory_info().rss/1048576:.02f} MB")
        embed.add_field(name="Bot Uptime",
                        value=str(timedelta(seconds=int(time.time()-process.create_time()))))
        embed.set_footer(
            text=f"Made by {app_info.owner.name}#{app_info.owner.discriminator}",
            icon_url=app_info.owner.avatar_url_as(size=128))
        await ctx.send(embed=embed)
