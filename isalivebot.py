import os
import discord
import json

from message import notify

class IsAlive(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_voice_state_update(self, member, before, after):
        if not after.channel:
            return            
        
        name = member.nick or member.name
        channel = after.channel.name
        playing = discord.utils.get(member.activities, type=discord.ActivityType.playing)
        gaming_message = f' e está jogando {playing.name}' if playing else ''

        if not before.channel:
            notify(f'{name} entrou em {channel}{gaming_message}')
        elif not before.self_stream and after.self_stream:
            notify(f'🔴 {name} está ao vivo em {after.channel}{gaming_message}')

    async def on_presence_update(self, before, after):
        burgues = discord.utils.get(after.roles, name='Burguês')
        if not burgues or not after.voice.channel:
            return

        print(after.activities)

        name = after.nick or after.name
        before_playing = discord.utils.get(before.activities, type=discord.ActivityType.playing)
        after_playing = discord.utils.get(after.activities, type=discord.ActivityType.playing)
        before_streaming = discord.utils.get(before.activities, type=discord.ActivityType.streaming)
        after_streaming = discord.utils.get(after.activities, type=discord.ActivityType.streaming)
        
        if not before_streaming and after_streaming:
            # Started streaming
            gaming = f' jogando {after_playing.name}' if after_playing else ''
            streaming_details = f' - {after_streaming.details}' if after_streaming.details else ''
            notify(f'🔴 {name} está ao vivo em {after.voice.channel}{gaming}{streaming_details}')
        elif not before_playing and after_playing:
            # Started playing
            game_details = f' ({after_playing.details})' if hasattr(after_playing, 'details') and after_playing.details else ''
            notify(f'{name} começou a jogar {after_playing.name}!{game_details}')

intents = discord.Intents(guilds=True, members=True, presences=True, voice_states=True)

client = IsAlive(intents=intents)
token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)
