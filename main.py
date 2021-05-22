import typing

import discord
from discord.ext import commands
from constants import Constants
from sherpaBot.SherpaBot import SherpaBot

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
# bot = commands.Bot(command_prefix='!')

sherpaBot = SherpaBot


@bot.event
async def on_ready():
    """starts sherpabot"""
    global sherpaBot
    sherpaBot = SherpaBot(bot)
    await sherpaBot.on_ready()


@bot.command()
async def sherpapic(ctx):
    """command for personalised profile picture, input a color (RGB or HEX) output a reply with the profile picture"""
    print("oui")
    await sherpaBot.sherpapic(ctx)


@bot.event
async def on_command_error(ctx, error):
    await sherpaBot.on_command_error(ctx, error)


@bot.command()
async def suggest(ctx):
    """command for suggestions"""
    await sherpaBot.suggest(ctx)


@bot.event
async def on_raw_reaction_add(payload):
    """Add sherpa role when a reaction is added on a particular message (not a message from sherpabot or a
    reaction of sherpabot) """
    await sherpaBot.on_raw_reaction_add(payload)


@bot.event
async def on_raw_reaction_remove(payload):
    """harder to remove than add a role, to do"""
    await sherpaBot.on_raw_reaction_remove(payload)


@bot.command(pass_context=True)
@commands.has_role(Constants.ROLE_FOR_CMD)
async def give_all(ctx, role):
    """Gives everyone in the server a given role
    Warning : It can be slow (10 members every 8 seconds) but the bot keeps working even if this command is proceeding"""
    await sherpaBot.give_all(ctx, role)


@bot.command(pass_context=True)
@commands.has_role(Constants.ROLE_FOR_CMD)
async def remove_all(ctx, role):
    """Removes a given role to everyone in the server
    Warning : It can be slow (10 members every 8 seconds) but the bot keeps working even if this command is proceeding"""
    await sherpaBot.remove_all(ctx, role)


@bot.command(pass_context=True)
@commands.has_role(Constants.ROLE_FOR_CMD)
async def save_server(ctx):
    await sherpaBot.save_server(ctx)


@bot.command(pass_context=True)
@commands.has_role(Constants.ROLE_FOR_CMD)
async def clear(ctx, number):
    await sherpaBot.clear(ctx, number)


@bot.command(pass_context=True)
@commands.has_role(Constants.ROLE_FOR_CMD)
async def ban(ctx, members: commands.Greedy[discord.Member],
              delete_days: typing.Optional[int] = 0, *,
              reason: str):
    await sherpaBot.ban(ctx, members, delete_days, reason=reason)


if __name__ == '__main__':
    with open(".key", "r") as f:
        key = f.read().replace("\n", "")
    bot.run(key)
