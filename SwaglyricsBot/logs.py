import datetime

import aiohttp
from discord import Webhook, AsyncWebhookAdapter, Embed

from SwaglyricsBot import ConsoleColors

webhook_url = ''
error_supervisor = ''


class Log:

    embed = Embed()

    async def add_log(self, value):
        """
        Creates log by printing value into console and creating discord embed. Use before add_sub_log
        """
        log_string = value
        print(log_string)
        self.embed.title = log_string
        self.embed.timestamp = datetime.datetime.now()
        self.embed.description = ""

    async def add_sub_log(self, value, color=ConsoleColors.EMPTY, mention_supervisor=False):
        """
        Adds sub log/step into log. 
        mention_supervisor is a special arugment that will ping defined in .env file supervisor in discord.
        color only affects console.
        """
        log_string = f"    - {value}"
        if color[0] != '':
            print(f"{color[0]}{log_string}{ConsoleColors.ENDC[0]}")
        else:
            print(log_string)
        if mention_supervisor:
            log_string += f'\nSUPERVISOR REQUESTED <@{error_supervisor}>'
        self.embed.description += f"{log_string}\n"

    # Use None for orange status (Lyrics error, not successful but intended behaviour)
    def change_log_success_status(self, value):
        """
        Sets color of embed in discord. Used as visual indicator of log "success" status.
        True - Green,
        False - Red,
        None - Orange
        """
        if value:
            self.embed.colour = 3066993 # Discord color format
        elif value is False:
            self.embed.colour = 15158332
        elif not value:
            self.embed.colour = 15105570

    async def send_webhook(self):
        """
        Sends log embed to discord via webhook if defined in .env file.
        """
        if webhook_url:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
                await webhook.send(embed=self.embed)
