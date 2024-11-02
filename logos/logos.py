
async def getLogos(ctx, logos:str) -> str: # fetch the logos from each respective team 
    for logo in ctx.guild.emojis:
        if logos.split()[-1] in logo.name: # index from -1, because the name of the team is the last word where the first one is the city they play in
            return str(logo)
    return ""