import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
        
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('MTMwMjM3MzM3ODg0NTQ0MjExOA.G0LYr9.-UBfTLHx2dOkPtgsmYtVxGECdEQg5MmOzUhoT0')        