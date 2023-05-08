import os
import discord

class IsAlive(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_voice_state_update(self, member, before, after):
        if not before.self_stream and after.self_stream:
            print(f'Oi pessoal, estou passando para avisar que {member.nick} acabou de abrir live em {after.channel.name}') 
        
    async def on_presence_update(self, before, after):
        print(f'{after.activities}')

intents = discord.Intents(guilds=True, members=True, presences=True, voice_states=True)

client = IsAlive(intents=intents)
token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)
