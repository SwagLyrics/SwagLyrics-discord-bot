import setuptools
import SwagLyricsBot

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SwagLyricsBot",
    version=SwagLyricsBot.__version__,
    author="Krzysztof Krysiński",
    author_email="krysinskikrzysztof123@gmail.com",
    description="A automatic lyrics fetching discord bot.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flabbet/SwagLyrics-discord-bot",
    packages=['SwagLyricsBot'],
    install_requires=[
        'swaglyrics',
        'discord',
        'env_file'
    ],
    extras_require={
        'dev': [
            'pytest',
            'codecov',
            'pytest-cov'
        ]
    },
    keywords='discord bot swaglyrics lyrics',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
