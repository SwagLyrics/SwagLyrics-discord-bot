import asyncio
import unittest

from SwaglyricsBot.general_commands import GeneralCommands

from SwaglyricsBot import LyricsNotFound


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
    testing_lyrics_2 = """
    [Intro]
Father, I stretch
Stretch my hands to You

[Verse]
Lifelike, this is what your life like, try to live your life right
People really know you, push your buttons like typewrite
This is like a movie, but it's really very lifelike
Every single night, right, every single fight, right?
I was looking at the 'Gram and I don't even like likes
I was screamin' at my dad, he told me, "It ain't Christ-like"
I was screamin' at the referee just like Mike
Lookin' for a bright light, Sigel, what your life like
Riding on a white bike, feeling like Excitebike (Stretch my hands to You)
Pressin' on the gas, supernova for a night light
Screamin' at my dad and he told me, "It ain't Christ-like"
But nobody never tell you when you're being like Christ
Only ever seein' me only when they needin' me
Like if Tyler Perry made a movie for BET
Searchin' for a deity, now you wanna see it free
Now you wanna see if we, let's just see if three apiece
Tell me what your life like, turn it down, a bright light
Drivin' with my dad, and he told me, "It ain't Christ-like" (Stretch my hands to You)
I'm just tryna find, l've been lookin' for a new way
I'm just really tryin' not to really do the fool way
I don't have a cool way, bein' on my best, though
Block 'em on the text though, nothin' else next though
Not another word, letter, picture, or a decimal (Father, I stretch)
Wrestlin' with God, I don't really want to wrestle
Man, it's really lifelike, everything in my life (Stretch my hands to You)
Arguing with my dad, and he said, "It ain't Christ-like"
"""

    def test_that_lyrics_chunks_does_not_exceed_1024_chars(self):
        chunks = GeneralCommands.chop_string_into_chunks(self.testing_lyrics, 1024)
        for chunk in chunks:
            print(len(chunk))
            self.assertTrue(len(chunk) <= 1024)

    def test_that_chopped_lyrics_with_long_chunk_does_not_exceed_1024_chars(self):
        chunks = GeneralCommands.chop_string_into_chunks(self.testing_lyrics_2, 1024)
        for chunk in chunks:
            self.assertTrue(len(chunk) <= 1024)

    def test_01that_lyrics_is_correct(self):
        lyrics = GeneralCommands.get_lyrics("Wonderful", "Caravan Palace")
        self.assertEqual(lyrics, self.testing_lyrics)

    def test_that_artists_list_converts_to_string(self):
        self.assertEqual("Eminem", GeneralCommands.artists_to_string(["Eminem"]))
        self.assertEqual("Eminem, 50 Cent", GeneralCommands.artists_to_string(["Eminem", "50 Cent"]))
        self.assertEqual("", GeneralCommands.artists_to_string(""))

    async def test_that_raises_lyrics_not_found(self):
        with self.assertRaises(LyricsNotFound):
            asyncio.create_task(GeneralCommands.get_lyrics("(*&d78a kj"))


    def test_that_pack_into_messages_returns_empty_message(self):
        chunks = []
        messages = GeneralCommands.pack_into_messages(chunks)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], [])

    def test_that_pack_into_messages_packs_into_one(self):
        chunks = ["I am mr. robot", "or am I?", "hey vsauce, michael here"]
        messages = GeneralCommands.pack_into_messages(chunks)
        self.assertEqual(len(messages), 1)

    def test_that_pack_into_messages_packs_into_two(self):
        chunks = [self.testing_lyrics, self.testing_lyrics, self.testing_lyrics, self.testing_lyrics_2, self.testing_lyrics_2]
        messages = GeneralCommands.pack_into_messages(chunks)
        self.assertEqual(len(messages), 2)


if __name__ == '__main__':
    unittest.main()
