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

async def generateURL(linkName: str, url: str) -> str:
    return f"{linkName}({url})"

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
    youtubeVideoLinks = []
    for x in result:
        youtubeVideoLinks.append(f"{os.getenv('YOUTUBE_VIDEO_LINK')}{x}")
    youtubeVideoLinks= tuple(youtubeVideoLinks)
    return youtubeVideoLinks

async def generatePlayerInfo(data: dict) -> map:
    playerInfo = []
    for player in data:
        info = f"{player['teamTricode']}/ {player['position']}/ {player['name']}: {player['points']}/ {player['rebounds']}/ {player['assists']}"
        playerInfo.append(info)
    return playerInfo

async def generateTeamNames(data: dict) -> str:
    return f"{data['wins']}-{data['losses']}", data["teamName"], int(data["score"])

async def generatePlayerOutput(playerData: str, teamName: str) -> str:
    data = playerData.split(": ")
    playerLink = await generateURL(data[0].split("/ ")[-1], os.getenv("TEAM_URL") + teamName)
    return f" - {'/ '.join(data[0].split('/ ')[:-1])} {playerLink} {data[1]}"

async def generateResult() -> list:
    result = []

    data = json.loads(getUrl(await generateURL()).html.find("#__NEXT_DATA__")[0].text)

    try:
        allGameResults = data['props']['pageProps']['gameCardFeed']['modules'][0]['cards']
    except Exception as e:
        print(e)
        return result

    for gameResults in allGameResults:
        homeTeamData = gameResults['cardData']['homeTeam'], gameResults['cardData']['awayTeam']
        awayTeamData = gameResults['cardData']['homeTeam'], gameResults['cardData']['awayTeam']
        
        homeTeamPlayerName = await generatePlayerInfo((homeTeamData['teamLeader'], awayTeamData['teamLeader']))
        awayTeamPlayerName = await generatePlayerInfo((homeTeamData['teamLeader'], awayTeamData['teamLeader']))
        
        homeTeamRecord, homeTeamName, homeTeamScore = await generateTeamNames(homeTeamData)
        homeTeamName = await generateTeamNames(homeTeamData)
        homeTeamScore = await generateTeamNames(homeTeamData)
        
        awayTeamRecord = await generateTeamNames(awayTeamData)
        awayTeamName = await generateTeamNames(awayTeamData)
        awayTeamScore = await generateTeamNames(awayTeamData)
        
        awayTeamPlayerName = await generatePlayerOutput(awayTeamPlayerName, awayTeamName.split()[-1])
        homeTeamPlayerName = await generatePlayerOutput(homeTeamPlayerName, homeTeamName.split()[-1])
        
        
        highlights = tuple(
            await generate_youtube_video_link(
                homeTeamName,
                awayTeamName,
                await date.get_current_date(),
            )
        )

        result.append(
            {
                f"Away": {
                    "Team": {
                        "name": awayTeamName,
                        "record": awayTeamRecord,
                        "score": int(awayTeamScore),
                    },
                    "Player": {"name": awayTeamPlayerName},
                },
                f"Home": {
                    "Team": {
                        "name": homeTeamName,
                        "record": homeTeamRecord,
                        "score": int(homeTeamScore),
                    },
                    "Player": {"name": homeTeamPlayerName},
                },
                "Highlights": highlights,
            }
        )

    return result

        

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
