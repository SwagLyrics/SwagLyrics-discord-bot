import asyncio
import unittest

from SwaglyricsBot import swaglyrics_bot, LyricsNotFound
from SwaglyricsBot.swaglyrics_bot import get_lyrics


class BotTests(unittest.TestCase):

    testing_lyrics = """[Intro: Sample]
Just imagine a trip to a wonderful land
Of candy, and jam, and ice cream

[Verse 1: Zoé Colotis]
I gotta hit that street, you better watch it
With a gat that I cock, with a full clip
I got the whip, got the pitch, gotta keep it undercover
All up in the club, just to live it up
See the stone cold face, try to knock it
I can't be trapped, never walk, I'm a rocket
I got a beat in it, I got a breath in it
I got a beat, got a beat, got a beat, a beat, a beat, a beat

[Verse 2: Zoé Colotis]
See the big gold chain that I'm rockin'?
I got the ring for the bling, not a problem
I got a stash full of cash that I owe to my brother
All up in the club, just to live it up
Look how the streets turn cold when I walk it
It's my rules, no man can stop it
I throw a kick so quick that'll leave you in the gutter
Leave you in the gutter, gutter, gutter, gutter...
(See the big gold chain that I'm)

[Chorus 1: Zoé Colotis]
All up in the gut-, all up in the gut-
I got all up in, all up in, all up in, all up in the gutter
All up in the gut-, all up in the gut-
I got all up in, all up in, all up in, all up in the gutter

[Chorus 2: Zoé Colotis]
All up in the gut-, all up in the gut-
All up in, all up in, all up in, all up in the gutter
All up in the gut-, all up in the gut-
I got all up in in the gutter

[Chorus 3: Zoé Colotis]
All up in the gut-, all up in the ooh!
I got all up in, all up in, all up in, all up in the gutter
All up in the gut-, all up in the gut-
All up in the gutter

[Interlude: Sample]
Just imagine, a wonderful land

[Bridge: Zoé Colotis]
I know all these things never happened
I'm just a random girl with gentle manners
In my dreams I rock and I rule the wonderland
Rule the wonderland, rule the wonderland
Rule the wonderland, wonderland, wonderland, wonderland, land, land, land, land...

[Chorus 4: Zoé Colotis]
All up in the gut-, all up in the gut-
I got all up in, all up in, all up in, all up in the gutter
All up in the gut-, all up in the gut-
I got, ooh, all up in the gutter

[Chorus 5: Zoé Colotis]
All up in the gut-, all up in the gut-
I got all up in, all up in, all up in, all up in the gutter
All up in the gut-, all up in the gut-
All up in the gutter"""

    def test_that_lyrics_chunks_does_not_exceed_1024_chars(self):
        chunks = swaglyrics_bot.chop_string_into_chunks(self.testing_lyrics, 1024)
        for chunk in chunks:
            self.assertTrue(len(chunk) <= 1024)

    async def test_01that_lyrics_is_correct(self):
        lyrics = swaglyrics_bot.get_lyrics("Wonderful", "Caravan Palace")
        self.assertEqual(lyrics, self.testing_lyrics)

    def test_that_artists_list_converts_to_string(self):
        self.assertEqual("Eminem", swaglyrics_bot.artists_to_string(["Eminem"]))
        self.assertEqual("Eminem, 50 Cent", swaglyrics_bot.artists_to_string(["Eminem", "50 Cent"]))
        self.assertEqual("", swaglyrics_bot.artists_to_string(""))

    async def test_that_raises_lyrics_not_found(self):
        with self.assertRaises(LyricsNotFound):
            asyncio.create_task(get_lyrics("!@#52sdakjc", "(*&d78a kj"))


if __name__ == '__main__':
    unittest.main()
