import datetime

import aiohttp
from discord import Webhook, AsyncWebhookAdapter, Embed

from SwaglyricsBot import ConsoleColors

webhook_url = ''


class Log:

    embed = Embed()

    async def add_log(self, value):
        log_string = value
        print(log_string)
        self.embed.title = log_string
        self.embed.timestamp = datetime.datetime.now()
        self.embed.description = ""

    async def add_sub_log(self, value, color=ConsoleColors.EMPTY):
        log_string = "    - {}".format(value)
        if color[0] != '':
            print("{}{}{}".format(color[0], log_string, ConsoleColors.ENDC[0]))
        else:
            print(log_string)
        self.embed.description += f"{log_string}\n"

    # Use None for orange status (Lyrics error, not successful but intended behaviour)
    def change_log_success_status(self, value):
        if value:
            self.embed.colour = 3066993
        elif value is False:
            self.embed.colour = 15158332
        elif not value:
            self.embed.colour = 15105570

    async def send_webhook(self):
        if webhook_url:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
                await webhook.send(embed=self.embed)
