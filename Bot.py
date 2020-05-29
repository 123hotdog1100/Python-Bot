import requests
import discord
from discord.ext import commands
import os
from configparser import ConfigParser

client = commands.Bot(command_prefix=".")
Voice = False
Fun = False
Key = ''
players = {}
config = ConfigParser()
config["Modules"] = {
    'Voice': 'True',
    'Fun': 'True'
}
parser = ConfigParser()

config["Bot"] = {
    'Key': 'NzE0OTU3NDQ4NTUyNjQ0NjE4.Xs7omQ.Gl1S8bo_0rmNjdoY7iWgndwmpS4'
}


def get_config():
    global Fun, Voice, parser, Key
    try:
        parser.read('config.ini')
        Voice = parser.get('Modules', 'Voice')
        Fun = parser.get('Modules', 'Fun')
        Key = parser.get('Bot', 'Key')
    except():
        print("sorry i have encounted an error laoding the config")
    for filename in os.listdir('./cogs'):
        if Voice == 'True':
            print("Loading Voice")
            client.load_extension("cogs.Voice")
        if Fun == 'True':
            print("Loading Fun")
            client.load_extension("cogs.Fun")
        break


##config startup check
def config_check():
    for filename in os.listdir('./'):
        if filename == "config.ini":
            return True
    else:
        return False


def startup():
    config_check()


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


@client.command()
async def test(ctx):
    r = requests.head('https://httpbin.org/get')
    await ctx.send(f'this is the response from google {r}')


startup()


client.run(Key)
