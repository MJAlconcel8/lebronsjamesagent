import datetime

async def getGamesJustPlayed() -> str:
    return datetime.date.today() - datetime.timedelta(days=1) #Since bot updates at midnight it retrieves the games that had just been played a couple of min ago

async def getGamesPlayedTheDayBefore(currentDate: str) -> datetime: # Gets games that had been played the day before
    return currentDate - datetime.timedelta(days=1)

async def convertDateTime(dataToConvert: datetime) -> str:
    return f'{dataToConvert.strftime('$b')}+{dataToConvert.day}+{dataToConvert.year}'