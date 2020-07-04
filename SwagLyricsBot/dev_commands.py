import os
import time
from datetime import timedelta
from random import getrandbits

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
            description=f"Running on a dedicated server with {total_ram}GB RAM \n provided by RandomGhost#0666.")
        embed.add_field(name="**__General Info__**", inline=False, value="\u200b")
        embed.add_field(name="Latency", value=f"{self.bot.latency*1000:.03f}ms")
        embed.add_field(name="Guild Count", value=f"{len(self.bot.guilds):,}")
        embed.add_field(name="User Count", value=f"{len(self.bot.users):,}")
        embed.add_field(name="**__Technical Info__**", inline=False, value="\u200b")
        embed.add_field(name="System CPU Usage", value=f"{psutil.cpu_percent():.02f}%")
        embed.add_field(name="System RAM Usage",
                        value=f"{psutil.virtual_memory().used/1048576:.02f} MB")
        embed.add_field(name="System Uptime",
                        value=f'{timedelta(seconds=int(time.time() - psutil.boot_time()))}')
        embed.add_field(name="Bot CPU Usage", value=f"{process.cpu_percent():.02f}%")
        embed.add_field(name="Bot RAM Usage", value=f"{process.memory_info().rss / 1048576:.02f} MB")
        embed.add_field(name="Bot Uptime",
                        value=f'{timedelta(seconds=int(time.time() - process.create_time()))}')
        embed.set_footer(
            text=f"Made by {app_info.owner} • clash#1337",
            icon_url=[app_info.owner.avatar_url_as(size=128), self.bot.get_user(512708394994368548).avatar_url_as(
                size=128)][rb(1)])  # randomize clash or flabbet avatar
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        Checks bot latency.
        """
        await ctx.send(f"Pong! {self.bot.latency * 1000:.03f}ms")
