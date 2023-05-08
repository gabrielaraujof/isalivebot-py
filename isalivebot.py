import os
import discord

from message import notify

class IsAlive(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_voice_state_update(self, member, before, after):
        if not before.self_stream and after.self_stream:
            activities = [activity for activity in member.activities if activity.type == discord.ActivityType.playing]
            game_message = f'de {activities[0].name}' if activities else ''
            notify(f'Oi pessoal, estou passando para avisar que {member.nick or member.name} acabou de abrir live {game_message} em {after.channel.name}') 
        
    async def on_presence_update(self, before, after):
        print(f'{after.activities}')

intents = discord.Intents(guilds=True, members=True, presences=True, voice_states=True)

client = IsAlive(intents=intents)
token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)
