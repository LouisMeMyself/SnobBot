# import typing
# import discord
# from snobBot import Constants
from discord.ext import commands
from snobBot.SnobBot import SnobBot

# intents = discord.Intents.all()
# intents.members = True
#
# bot = commands.Bot(command_prefix='!', intents=intents)
bot = commands.Bot(command_prefix='!')

snobBot = SnobBot


@bot.event
async def on_ready():
    """starts snobbot"""
    global snobBot
    snobBot = SnobBot(bot)
    await snobBot.on_ready()


@bot.command()
async def snobpic(ctx):
    """command for personalised profile picture, input a color (RGB or HEX) output a reply with the profile picture"""
    await snobBot.snobpic(ctx)


@bot.event
async def on_command_error(ctx, error):
    await snobBot.on_command_error(ctx, error)


if __name__ == '__main__':
    with open(".key", "r") as f:
        key = f.read().replace("\n", "")
    bot.run(key)
