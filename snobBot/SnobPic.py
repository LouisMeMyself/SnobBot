import re
import discord
import numpy as np
from cairosvg import svg2png
from constants import Constants


class SnobPic:
    def __init__(self):
        self.hex_regex = re.compile("^[0-9a-fA-F]{6}")
        with open("utils/Snob-logo.svg", "rb") as f:
            self.snobSVG = f.read().decode("utf-8")
        self.index = str(self.snobSVG).find("#F24E4D;}")
        self.snobSVG = list(self.snobSVG)

    def do_profile_picture(self, content):
        try:
            new_color = str(content.replace(Constants.PROFILE_PICTURE_COMMAND, "")[1:])
            if new_color.replace(" ", "").replace(",", "") == "":  # handles empty messages
                return """Please write a HEX color or a RGB color. in these formats: '#00FFFF', '00FFFF', '0 255 255' or '0,255,255\nThe command should look like this: `!snobpic [color]`"""
            if new_color[0] == "#" and self.hex_regex.match(new_color[1:]) is not None and len(new_color) == 7:  # handles the "#XXXXXX" hex colours
                new_color = new_color[1:]
            elif " " in new_color or "," in new_color:
                if " " in new_color and "," in new_color:  # handles the "R,        G,    B" colours
                    new_color = new_color.replace(" ", "")
                if "," in new_color:  # handles the "R,G,B" colours
                    new_color = np.array(new_color.split(","), dtype=int)
                elif " " in new_color:  # handles the "R G B" colours
                    new_color = np.array(new_color.split(" "), dtype=int)
                if isinstance(new_color, np.ndarray) and len(new_color) == 3 and np.any(new_color >= 0) and np.any(
                        new_color <= 255):
                    new_color = "%02x%02x%02x" % tuple(new_color)
                else:
                    return "RGB colours are between 0 and 255 and need 3 integers, like '127 255 212' or '127,255,212'"
            if self.hex_regex.match(new_color) is not None and len(new_color) == 6:
                self.snobSVG[self.index + 1: self.index + 7] = new_color
                svg2png("".join(self.snobSVG), write_to="utils/Snob-logo.png")
                return "Here is your personalized profile picture!", discord.File("utils/Snob-logo.png")
            return "Please write a HEX color or a RGB color. in these formats: '#00FFFF', '00FFFF', '0 255 255' or '0,255,255"
        except ValueError:
            return "Please write a HEX color or a RGB color. in these formats: '#00FFFF', '00FFFF', '0 255 255' or '0,255,255"
        except:
            return "Unexpected error..."
