import os
import discord

from message import notify

class IsAlive(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_voice_state_update(self, member, before, after):
        name = member.nick or member.name
        playing = discord.utils.get(member.activities, type=discord.ActivityType.playing)
        game = f' e está jogando {playing.name}' if playing else ''
        game_details = f' - {playing.details}' if playing and playing.details else ''
        game_message = f'{game}{game_details}'
        channel = f'{after.channel.name}'

        if not before.channel and after.channel:
            notify(f'{name} entrou em {channel}{game_message}')
        elif not before.self_stream and after.self_stream:
            notify(f'🔴 {name} está ao vivo em {channel}{game_message}') 

    async def on_presence_update(self, before, after):
        before_playing = discord.utils.get(before.activities, type=discord.ActivityType.playing)
        after_playing = discord.utils.get(after.activities, type=discord.ActivityType.playing)
        if not before_playing and after_playing and after.channel:
            burgues = discord.utils.get(after.roles, name='Burguês')
            if burgues:
                game_details = f' - {after_playing.details}' if after_playing and after_playing.details else ''
                notify(f'{after.nick or after.name} começou a jogar {after_playing.name}{game_details}')

intents = discord.Intents(guilds=True, members=True, presences=True, voice_states=True)

client = IsAlive(intents=intents)
token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)
