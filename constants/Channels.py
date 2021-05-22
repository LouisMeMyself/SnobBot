from constants import Constants


class Channels:
    def __init__(self, bot):
        self.reaction_channel = {server.id: channel for server in bot.guilds for channel in server.channels
                            if channel.name == Constants.SHERPAREACT_CHANNEL_NAME}

        self.suggestion_channel = {server.id: channel for server in bot.guilds for channel in server.channels
                              if channel.name == Constants.SHERPASUGGEST_CHANNEL_NAME}

        self.profile_picture = {server.id: channel for server in bot.guilds for channel in server.channels
                           if channel.name == Constants.SHERPAPIC_CHANNEL_NAME}
