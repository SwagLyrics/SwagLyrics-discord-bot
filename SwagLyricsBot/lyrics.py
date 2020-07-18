import re
import aiocfscrape
import aiohttp

from SwagLyricsBot import backend_url, LyricsNotFound

from bs4 import BeautifulSoup, UnicodeDammit
from swaglyrics.cli import stripper


async def fetch(session, url, **kwargs):
    """
    Uses aiohttp to make http GET requests
    """
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    async with aiocfscrape.CloudflareScraper(headers=headers) as session:
        async with session.get(url) as resp:
            return await resp.text()


async def get_lyrics(song, artist, session):
    """
    doc: https://github.com/SwagLyrics/SwagLyrics-For-Spotify/blob/master/swaglyrics/cli.py#L75
    Get lyrics from Genius given the song and artist.
    Formats the URL with the stripped url path to fetch the lyrics.
    :param session: the aiohttp session
    :param song: currently playing song
    :param artist: song artist
    :return: song lyrics or None if lyrics unavailable
    """
    url_data = stripper(song, artist)  # generate url path using stripper()
    if url_data.startswith('-') or url_data.endswith('-'):
        return None  # url path had either song in non-latin, artist in non-latin, or both
    url = f'https://genius.com/{url_data}-lyrics'  # format the url with the url path

    try:
        page = await fetch(session, url, raise_for_status=True)
    except aiohttp.ClientResponseError:
        url_data = await fetch(session, f'{backend_url}/stripper', data={'song': song, 'artist': artist})
        if not url_data:
            raise LyricsNotFound(f"Lyrics for {song} by {artist} not found on Genius.")
        url = f'https://genius.com/{url_data}-lyrics'
        page = await fetch(session, url)

    html = BeautifulSoup(page, "html.parser")
    lyrics_path = html.find("div", class_="lyrics")  # finding div on Genius containing the lyrics
    if lyrics_path:
        lyrics = UnicodeDammit(lyrics_path.get_text().strip()).unicode_markup
    else:
        # hotfix!
        lyrics_path = html.find_all("div", class_=re.compile("^Lyrics__Container"))
        lyrics_data = []
        for x in lyrics_path:
            lyrics_data.append(UnicodeDammit(re.sub("<.*?>", "", str(x).replace("<br/>", "\n"))).unicode_markup)

        lyrics = "\n".join(lyrics_data)
    return lyrics
