import os
import discord

from message import notify

class IsAlive(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_voice_state_update(self, member, before, after):
        if not before.self_stream and after.self_stream:
            playing = discord.utils.get(member.activities, type=discord.ActivityType.playing)
            game_message = f' de {playing.name}' if playing else ''
            game_details = f' - {playing.details}' if playing and playing.details else ''
            notify(f'Oi pessoal, estou passando para avisar que {member.nick or member.name} acabou de abrir live{game_message}{game_details} em {after.channel.name}') 

intents = discord.Intents(guilds=True, members=True, presences=True, voice_states=True)

client = IsAlive(intents=intents)
token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)
