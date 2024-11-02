import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('hello'):
            await message.channel.send(f'hi there {message.author}')
        
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run('MTMwMjM3MzM3ODg0NTQ0MjExOA.G0LYr9.-UBfTLHx2dOkPtgsmYtVxGECdEQg5MmOzUhoT0')        