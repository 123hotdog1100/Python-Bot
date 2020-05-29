import discord
from discord.ext import commands
import os
from configparser import ConfigParser

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


config_check()
try:
    client.run(Key)
except RuntimeError:
    print("Runtime error please try again")
