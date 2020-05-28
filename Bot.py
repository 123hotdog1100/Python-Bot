import random
import requests
import discord
import yaml
from discord.ext import commands
import os

client = commands.Bot(command_prefix=".")
voice = False
fun = False
players = {}
config = [{"modules": ["voice", "fun"]}]


##checks for the file
def startup():
    config_check()


def config_check():
    for filename in os.listdir('./'):
        if filename == "config.yaml":
            return True
    else:
        return False


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('My prefix is' + '.'))
    print('bot is Ready.')


@client.command()
async def ping(ctx):
    await ctx.send(f"pong! {round(client.latency * 1000)} MS")


@client.command(aliases=['8ball', 'eightball', 'ball'])
async def _8ball(ctx, *, Question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f'Question: {Question}\nAnswer:{random.choice(responses)}')


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


for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')


def get_config():
    global fun, voice
    with open('config.yaml') as f:
        conf = yaml.full_load(f)
        print(conf)
        if "Voice" in conf:
            voice = True
        if "fun" in conf:
            fun = True
        print(voice, fun)
    f.close()
get_config()
if config_check():
    client.run('NzE0OTU3NDQ4NTUyNjQ0NjE4.Xs7omQ.Gl1S8bo_0rmNjdoY7iWgndwmpS4')
else:
    c = open("config.yaml", "w")
    f = yaml.dump(config, c)

startup()

