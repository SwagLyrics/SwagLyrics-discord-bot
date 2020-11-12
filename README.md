[![inviteme](https://img.shields.io/static/v1?style=flat&logo=discord&logoColor=FFF&label=&message=invite%20me&color=7289DA)](https://top.gg/bot/660170175517032448)
[![Discord Server](https://badgen.net/badge/discord/join%20chat/7289DA?icon=discord)](https://discord.gg/DSUZGK4)
[![Discord Bots](https://top.gg/api/widget/status/660170175517032448.svg)](https://top.gg/bot/660170175517032448)
[![Discord Bots](https://top.gg/api/widget/servers/660170175517032448.svg)](https://top.gg/bot/660170175517032448)
[![Build Status](https://travis-ci.com/SwagLyrics/SwagLyrics-discord-bot.svg?branch=master)](https://travis-ci.com/SwagLyrics/SwagLyrics-discord-bot)
[![codecov](https://codecov.io/gh/SwagLyrics/SwagLyrics-discord-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/SwagLyrics/SwagLyrics-discord-bot)


# SwagLyrics-discord-bot
An implementation of swaglyrics into a discord bot. When you listen to music on spotify, this bot will print you the lyrics. All automatic!

# Usage

Simply type `$swaglyrics` and let the magic happen!

For specific lyrics, type `$swaglyrics song ,, artist`

<p align="center">
  <img src=https://raw.githubusercontent.com/SwagLyrics/SwagLyrics-discord-bot/master/swaglyrics_discord_mockup.png alt="SwagLyrics Bot in action">
</p>

# Commands

## SwagLyrics

Command: `$swaglyrics song ,, artist` where `song` and `artist` are optional arguments.

Aliases: `$sl`.

Action: Main command, gets lyrics for song you are listening to. 

Example: `$swaglyrics Round And Round ,, Imagine Dragons`

## Ping

Command: `$ping`.

Action: Pings bot, returns bot latency in `ms`.

## Stats

Command: `$stats`.

Action: Shows bot statistics and technical data.

# Requirements

Spotify needs to be connected with discord, status in "Settings -> Connections -> Spotify -> Display Spotify as your status" needs to be turned on.

# Building from source

Install requirements with `pip3 install -r requirements.txt` (use `pip` or `pip3`, depending on your setup).

`cd` to `SwagLyrics-discord-bot` directory.

Create `.env` file and fill it with token

`BOT_TOKEN=<your token>`

Congratulations! Bot is successfully configured. Now you can run directily with `python3 __main__.py` or install it with `python3 setup.py install` and run with `python3 -m SwagLyricsBot`. Remember to run it from directory where `.env` is located.

## Additional settings

If you want, you can setup logging directly to discord server using webhooks and upload stats to TopGG

`.env` entries:

`WEBHOOK_URL=<your discord webhook url>`

`WEBHOOK_ERROR_SUPERVISOR_ID=<discord user id>` Used for pinging user if error occures.

`DBL_TOKEN=<your TopGG token>`
