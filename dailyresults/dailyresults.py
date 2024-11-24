import discord
from logos.logos import getLogos
from generateresults.generateresults import generateLink

def generateResults(dateToday, logoUrl):
    results = discord.Embed(
        title=f"NBA Results for {dateToday}",
        color=discord.Color.blue()
    )
    results.set_thumbnail(url=logoUrl)
    return results

async def generateResultField(ctx, show, embed):

    homeTeam, awayTeam = (
        ("", await getLogos(ctx, "9410pinkarrowL"))
        if show["Home"]["Team"]["score"] > show["Away"]["Team"]["score"]
        else (await getLogos(ctx, "9410pinkarrowR"), "")
    )

    embed.add_field(
        name=f"{await getLogos(ctx, show['Away']['Team']['name'])} "
        f"({show['Away']['Team']['record']}) "
        f"{show['Away']['Team']['name'].upper()}{homeTeam} {show['Away']['Team']['score']} @ "
        f"{show['Home']['Team']['score']} "
        f"{awayTeam}{show['Home']['Team']['name'].upper()}"
        f" ({show['Home']['Team']['record']}) "
        f"{await getLogos(ctx, show['Home']['Team']['name'])} ",
        value=f"**Game Leaders**\n{show['Away']['Player']['name']}\n"
        f"{show['Home']['Player']['name']}\n"
        f"{await getLogos(ctx, 'youtube')} **Highlights** {', '.join([await generateLink(f'Link {pos}', link) for pos, link in enumerate(show['Highlights'], 1)])}",
        inline=False,
    )