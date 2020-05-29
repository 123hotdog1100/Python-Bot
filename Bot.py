import discord
from discord.ext import commands
import os
from configparser import ConfigParser
from discord.utils import get
import youtube_dl

Voice = False
Fun = False
Key = ''
Prefix = '.'
players = {}
config = ConfigParser()
config["Modules"] = {
    'Voice': 'True',
    'Fun': 'True'
}
parser = ConfigParser()

config["Bot"] = {
    'Key': '',
    'Prefix': '.'
}


##Reads the config.ini file for parameters
def get_config():
    global Fun, Voice, parser, Key, client, Prefix
    try:
        parser.read('config.ini')
        Voice = parser.get('Modules', 'Voice')
        Fun = parser.get('Modules', 'Fun')
        Key = parser.get('Bot', 'Key')
        print("Using Key from Config.ini", Key)
        Prefix = parser.get('Bot', 'Prefix')
    except():
        print("sorry i have encounted an error laoding the config")
    client = commands.Bot(command_prefix=Prefix)
    for filename in os.listdir('./cogs'):
        if Voice == 'True':
            print("Loading Voice")
            client.load_extension("cogs.Voice")
        if Voice == 'False':
            print("Not loading Voice")
        if Fun == 'False':
            print("Not loading Fun")
        if Fun == 'True':
            print("Loading Fun")
            client.load_extension("cogs.Fun")
        break


##Checks to see if the config file exists
def config_check():
    for filename in os.listdir('./'):
        if filename == "config.ini":
            return True
    else:
        return False


if config_check():
    get_config()
else:
    with open('config.ini', "w") as c:
        config.write(c)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('My prefix is' + '.'))
    print('bot is Ready.')


@client.command()
async def ping(ctx):
    await ctx.send(f"pong! {round(client.latency * 1000)} MS")


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
async def shutdown(ctx):
    await ctx.send("Shutting the bot down ")
    await client.close()


@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str,):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music playing")
            return

        await ctx.send("Getting everything ready now")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        }
        voice = get(client.voice_clients, guild=ctx.guild)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Rename file: {file}\n")
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        nname = name.rsplit("-", 2)
        await ctx.send(f"PlayingL {nname}")

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
     await ctx.send('Please let me join a Voice channel to play audio ')



config_check()
try:
    client.run(Key)
except RuntimeError:
    print("Runtime error please try again")
