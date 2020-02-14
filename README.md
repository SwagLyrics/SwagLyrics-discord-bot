[![inviteme](https://img.shields.io/static/v1?style=flat&logo=discord&logoColor=FFF&label=&message=invite%20me&color=7289DA)](https://top.gg/bot/660170175517032448)
[![Discord Server](https://badgen.net/badge/discord/join%20chat/7289DA?icon=discord)](https://discord.gg/DSUZGK4)
[![Discord Bots](https://top.gg/api/widget/status/660170175517032448.svg)](https://top.gg/bot/660170175517032448)
[![Discord Bots](https://top.gg/api/widget/servers/660170175517032448.svg)](https://top.gg/bot/660170175517032448)
[![Build Status](https://travis-ci.com/SwagLyrics/SwagLyrics-discord-bot.svg?branch=master)](https://travis-ci.com/SwagLyrics/SwagLyrics-discord-bot)
[![codecov](https://codecov.io/gh/SwagLyrics/Swaglyrics-discord-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/SwagLyrics/Swaglyrics-discord-bot)


# SwagLyrics-discord-bot
An implementation of swaglyrics into a discord bot. When you listen to music on spotify, this bot will print you the lyrics. All automatic!

# Usage

Simply type `$swaglyrics` and let the magic happen!

For specified lyrics, type `$swaglyrics <song> <artist>`

![Bot in action screenshot](https://raw.githubusercontent.com/SwagLyrics/SwagLyrics-discord-bot/master/Bot_in_action.png)

# Commands

## Swaglyrics

Command: `$swaglyrics [song] [artists]` where `song` and `artist` are optional arguments.

Aliases: `$sl`.

Action: Main command, gets lyrics for song you are listening to. 

Example: `$swaglyrics "Round And Round" "Imagine Dragons"`

## Ping

Command: `$ping`.

Action: Pings bot, returns bot delay in `ms`.

## Stats

Command: `$stats`.

Action: Shows bot statistics and technical data.

# Requirements

Spotify needs to be connected with discord, status in "Settings -> Connections -> Spotify -> Display Spotify as your status" needs to be turned on.
