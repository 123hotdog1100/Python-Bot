import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import random
client = commands.Bot(command_prefix = ".")


@client.event
async def on_ready():
    print('bot is Ready.')

@client.command()
async def ping(ctx):
    await ctx.send(f"pong! {round(client.latency *1000)} MS")


@client.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx,* , question):
    responses =["It is certain.",
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
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect(channel)
client.run('NzE0OTU3NDQ4NTUyNjQ0NjE4.Xs7omQ.Gl1S8bo_0rmNjdoY7iWgndwmpS4')
