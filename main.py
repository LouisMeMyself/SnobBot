import typing

import discord
from discord.ext import commands
from constants import Constants
from snobBot.SnobBot import SnobBot

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
# bot = commands.Bot(command_prefix='!')

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
    print("oui")
    await snobBot.snobpic(ctx)


@bot.event
async def on_command_error(ctx, error):
    await snobBot.on_command_error(ctx, error)


@bot.command()
async def suggest(ctx):
    """command for suggestions"""
    await snobBot.suggest(ctx)


@bot.event
async def on_raw_reaction_add(payload):
    """Add snob role when a reaction is added on a particular message (not a message from snobbot or a
    reaction of snobbot) """
    await snobBot.on_raw_reaction_add(payload)


@bot.event
async def on_raw_reaction_remove(payload):
    """harder to remove than add a role, to do"""
    await snobBot.on_raw_reaction_remove(payload)


@bot.command(pass_context=True)
@commands.has_role(Constants.ROLE_FOR_CMD)
async def give_all(ctx, role):
    """Gives everyone in the server a given role
    Warning : It can be slow (10 members every 8 seconds) but the bot keeps working even if this command is proceeding"""
    await snobBot.give_all(ctx, role)


@bot.command(pass_context=True)
@commands.has_role(Constants.ROLE_FOR_CMD)
async def remove_all(ctx, role):
    """Removes a given role to everyone in the server
    Warning : It can be slow (10 members every 8 seconds) but the bot keeps working even if this command is proceeding"""
    await snobBot.remove_all(ctx, role)


@bot.command(pass_context=True)
@commands.has_role(Constants.ROLE_FOR_CMD)
async def save_server(ctx):
    await snobBot.save_server(ctx)


@bot.command(pass_context=True)
@commands.has_role(Constants.ROLE_FOR_CMD)
async def clear(ctx, number):
    await snobBot.clear(ctx, number)


@bot.command(pass_context=True)
@commands.has_role(Constants.ROLE_FOR_CMD)
async def ban(ctx, members: commands.Greedy[discord.Member],
              delete_days: typing.Optional[int] = 0, *,
              reason: str):
    await snobBot.ban(ctx, members, delete_days, reason=reason)


if __name__ == '__main__':
    with open(".key", "r") as f:
        key = f.read().replace("\n", "")
    bot.run(key)
