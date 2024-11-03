import re
import json
import asyncio
import os
from lxml.html.clean import Cleaner

from dotenv import load_dotenv
from requests_html import HTMLSession

load_dotenv()
session = HTMLSession()

def getUrl(url: str) -> HTMLSession:
    return session.get(url)

async def generateYoutubeURL(homeTeam: str, awayTeam: str, GamesJustPlayed: str) -> tuple:
    result = set()
    listOfVideos = []
    for channel in os.getenv("VIDEO_CHANNELS").split(", "):
        matchUps = f"{channel}+Highlights+full+game+{homeTeam}+vs+{awayTeam}".replace(" ", "+") # gets the team matchups
        YoutubeURL = getUrl(f"{os.getenv('YOUTUBE_SEARCH_LINK')}{matchUps}{os.getenv('CRITERIA')}") # gets a youtube url with the game matchup
        listOfVideos += re.findall(r"watch\?v=(\S{11})", YoutubeURL.text) # uses a regex to find games with the game matchups and adds to video list
        
    for videos in listOfVideos:
        result.add(videos)
        if len(result) == 5: # only returns upto find game highlights
            break
    return tuple(f"{os.getenv('YOUTUBE_VIDEO_LINK')}{x}" for x in result)

async def test_generateYoutubeURL():
    # Define environment variables for testing
    os.environ["VIDEO_CHANNELS"] = "NBA,NBA Highlights"
    os.environ["YOUTUBE_SEARCH_LINK"] = "https://www.youtube.com/results?search_query="
    os.environ["CRITERIA"] = "&sp=EgIQAQ%253D%253D"  # Example YouTube filter for "Today" videos
    os.environ["YOUTUBE_VIDEO_LINK"] = "https://www.youtube.com/watch?v="

    # Define test parameters
    homeTeam = "Rockets"
    awayTeam = "Warriors"
    GamesJustPlayed = "2024-11-03"  # Unused, but added for completeness

    # Call the function and print results
    result = await generateYoutubeURL(homeTeam, awayTeam, GamesJustPlayed)
    print("Generated YouTube URLs:", list(result))

# Run the test
asyncio.run(test_generateYoutubeURL())
