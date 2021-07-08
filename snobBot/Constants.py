# Server
LIVE_SERVER_ID = 812557591917887508
TEST_SERVER_ID = 829742012558475324

# Commands
PROFILE_PICTURE_COMMAND = "!snobpic"
COMMAND_GLASSES = "glasses"

# Errors
ERROR_ON_PROFILE_PICTURE ="""How to use snobBot for profile pictures:

1. Choose a HEX color or a RGB color in these formats: `#00FFFF`, `00FFFF`, `0 255 255` or `0,255,255`. [(color picker)](https://htmlcolorcodes.com/color-picker/)

2. Enter this command `!snobpic [color]` for only changing the color of fur,
   `!snobpic [color1] [color2]` for fur and eyes, add `glasses` to add some cool glasses!
   Any color can be replaced by `random` in order to have a random color selected

3. Save image + add as your Discord profile photo !"""


class Channels:
    def __init__(self, server_id, bot):
        if server_id == LIVE_SERVER_ID:
            server_nb = 0
        elif server_id == TEST_SERVER_ID:
            server_nb = 1
        else:
            raise Exception("Servers not found, pls check ids")

        self.__channel = {}
        for server in bot.guilds:
            if server.id == server_id:
                for channel in server.channels:
                    self.__channel[channel.id] = channel

        self.SNOBPIC_CHANNEL_ID = (862594643082215455, 842089026625470464)[server_nb]  # "👨🏻-profile-pictures"

    def get_channel(self, channel_id):
        return self.__channel[channel_id]


