name = "SwagLyricsBot"
__version__ = "0.0.1"
backend_url = "https://api.swaglyrics.dev"


class LyricsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class LyricsNotFound(LyricsError):
    def __init__(self, message):
        super().__init__(message)


class SpotifyClosed(LyricsError):
    def __init__(
        self,
        message="You are not listening to anything or Spotify is not connected to Discord! \n "
        "Make sure you have enabled status in Settings -> Connections -> Spotify -> Display "
        "Spotify as your status or use `$sl [song] ,, [artist]`\nExample: `$sl "
        '"Bad Guy" "Billie Eilish"`.',
    ):
        super().__init__(message)


class NoActivityAccess(LyricsError):
    def __init__(self, message="Can't access your Spotify data."):
        super().__init__(message)


class NotEnoughArguments(LyricsError):
    def __init__(self, message):
        super().__init__(message)


class ConsoleColors:
    EMPTY = ["", ""]
    ENDC = ["\033[0m", ""]
    OKGREEN = ["\033[92m", "CSS"]
    FAIL = ["\033[91m", ""]
