import discord
from discord.ext import commands

from snobBot import SnobPic, Constants


class SnobBot:
    snobPic_ = SnobPic.SnobPic()
    bot = commands.Bot
    channels = Constants.Channels
    # bank = {}

    def __init__(self, bot):
        self.bot = bot
        for server in self.bot.guilds:
            self.channels = Constants.Channels(server.id, bot)

    async def on_ready(self):
        """starts snobbot"""
        # msg = await self.channels.get_channel(self.channels.GUIDELINES_CHANNEL_ID).fetch_message(self.channels.GUIDELINES_MSG_ID)
        # await msg.add_reaction(Constants.EMOJI_ACCEPT_GUIDELINES)
        print('snobBot have logged in as {0.user}'.format(self.bot))

    async def snobpic(self, ctx):
        """command for personalised profile picture, input a color (RGB or HEX) output a reply with the profile picture"""
        if ctx.message.channel.id == self.channels.SNOBPIC_CHANNEL_ID:
            try:
                answer = self.snobPic_.do_profile_picture(ctx.message.content.replace(Constants.PROFILE_PICTURE_COMMAND, "")[1:])
                await ctx.reply(answer[0], file=answer[1])
            except ValueError:
                e = discord.Embed(title="Error on {} command !".format(Constants.PROFILE_PICTURE_COMMAND[1:]),
                                  description=Constants.ERROR_ON_PROFILE_PICTURE,
                                  color=0xF24E4D)
                await ctx.reply(embed=e)
        return

    async def on_command_error(self, ctx, error):
        if ctx.message.channel.id == self.channels.SNOBPIC_CHANNEL_ID and isinstance(error, commands.CommandNotFound):
            e = discord.Embed(title="Error on {} command !".format(Constants.PROFILE_PICTURE_COMMAND[1:]),
                              description=Constants.ERROR_ON_PROFILE_PICTURE,
                              color=0xF24E4D)
            await ctx.reply(embed=e)
            return
        raise error