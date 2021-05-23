from constants import Constants


class Channels:
    def __init__(self, bot):
        self.reaction_channel = {server.id: channel for server in bot.guilds for channel in server.channels
                            if channel.name == Constants.SNOBREACT_CHANNEL_NAME}

        self.suggestion_channel = {server.id: channel for server in bot.guilds for channel in server.channels
                              if channel.name == Constants.SNOBSUGGEST_CHANNEL_NAME}

        self.profile_picture = {server.id: channel for server in bot.guilds for channel in server.channels
                           if channel.name == Constants.SNOBPIC_CHANNEL_NAME}
