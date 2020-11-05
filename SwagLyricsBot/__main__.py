import asyncio
from SwagLyricsBot.swaglyrics_bot import run as main


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.close()
