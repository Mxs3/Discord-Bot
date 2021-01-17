import os
import sys
import time
import errno
import datetime
import random
import ffmpeg
import discord
import configparser as cp
import colorama as color
import youtube_dl as yt
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import MissingPermissions
from colorama import Fore, Style

TOKEN = #token goes here
cmd_prefix = '!'
client = commands.Bot(command_prefix=cmd_prefix)
general_chat_id = 787473942348693547
spam_chat_id = 798618318659518475
client_version = '1.1.3'
color.init(autoreset=True)
current_time = datetime.datetime.now()
TEMP_audio_file = 'test.mp3'

@client.event
async def on_ready():
    print(f'{Fore.GREEN}Bot logged in as: ')
    print(f'{Fore.BLUE}' + client.user.name + '\n')
    channel = client.get_channel(spam_chat_id)
    await channel.send("Type '!help' for a list of commands")

'''@client.event
async def on_disconnect():
    print(f'{Fore.RED}Bot has disconnected from server.\n')
    return'''

'''@client.event
async def on_message(msg):
    try:
        os.mkdir('TEMP')
        with open('./TEMP/chat_log.txt', 'a+') as log:
            log.write(msg.content + '\n')
            print(f'{Fore.GREEN}CHAT LOG UPDATED\n')
    except OSError as e:
        if e.errno == errno.EEXIST:
            print(f'{Fore.RED}Directory already exists.\n')
            with open('./TEMP/chat_log.txt', 'a+') as log:
                log.write(msg.content + '\n')
                print(f'{Fore.GREEN}CHAT LOG UPDATED\n')
        else:
            with open('./TEMP/chat_log.txt', 'a+') as log:
                log.write(msg.content + '\n')
                print(f'{Fore.GREEN}CHAT LOG UPDATED\n')
            raise
    print(f'{Fore.GREEN}message recieved: ' + msg.content + '\n')'''

@client.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(context, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await context.send('User ' + member.display_name + ' has been KICKED.')
    print(f'{Fore.RED}KICKED user: ' + member.display_name + '\n')

@client.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(context, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await context.send('User ' + member.display_name + ' has been BANNED.')
    print(f'{Fore.RED}BANNED user: ' + member.display_name + '\n')

@client.command(name='join')
async def join(context):
    voice_channel = context.author.voice.channel
    await voice_channel.connect()
    print(f'{Fore.GREEN}Bot joined voice channel\n')

@client.command(name='play')
async def play(context, url: str):
    audio_file = './test.mp3'
    file_exists = os.path.isfile(audio_file)
    try:
        if file_exists:
            os.remove(audio_file)
            print('Removing old file...\n')
    except PermissionError as pe:
        print("Can't delete file\n")
        await context.send('ERROR: ' + pe)
        return

    await context.send('Trying to download audio file to client...')
    voice_channel = get(client.voice_clients, guild=context.guild)

    ydl_options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    with yt.YoutubeDL(ydl_options) as ydl:
        print(f'{Fore.GREEN}Downloading audio file...\n')
        await context.send('Downloading audio file...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            file_name = file
            print(f'Renamed file: {file}\n')
            os.rename(file, 'song.mp3')

    voice_channel.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda x: print(f'{Fore.GREEN}File: {file_name} has finished playing\n'))
    
    nname = file_name.rsplit('-', 2)
    embed = discord.Embed(title='Playing Audio', inline=True, color=0x9A00FF)
    embed.add_field(name='SOURCE', value=nname, inline=True)
    embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Icons8_flat_audio_file.svg/512px-Icons8_flat_audio_file.svg.png')
    await context.send(embed=embed)
    print(f'{Fore.GREEN}Playing audio...\n')

@client.command(name='leave')
async def leave(context):
    await context.voice_client.disconnect()
    print(f'{Fore.GREEN}Bot left voice channel\n')

'''@client.command(name='dc')
async def dc(context):
    await on_disconnect()
    await context.send('Bot ' + client.user.name + ' disconnected from server.')'''

@client.command(name='ping')
async def ping(context):
    ping_var = (f'{round(client.latency * 1000)}')
    await context.send('Latency: ' + ping_var)
    print(f'{Fore.GREEN}LATENCY: ' + ping_var + '\n') 

@client.command(name='version')
async def version(context):
    await context.send('Bot version: ' + client_version)
    print(f'{Fore.BLUE}CLIENT VERSION: ' + client_version + '\n')

@client.command(name='repo')
async def repo(context):
    embed = discord.Embed(title="Github Repository", url="https://github.com/Mxsen-sys/Discord_Bot", inline=True, color=0x9A00FF)
    embed.set_image(url='https://github.githubassets.com/images/modules/logos_page/Octocat.png')
    await context.send(embed=embed)

print(f"{Fore.GREEN}Bot is running...\n")
print(f'{Fore.BLUE}BOT TOKEN: ' + TOKEN + '\n')
client.run(TOKEN)
