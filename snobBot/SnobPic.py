import re
import discord
import numpy as np
from cairosvg import svg2png
from constants import Constants


class SnobPic:
    def __init__(self):
        self.hex_regex = re.compile("^[0-9a-fA-F]{6}")
        with open("utils/snob-logo.svg", "rb") as f:
            self.snobSVG = f.read().decode("utf-8")
        self.fur_index = str(self.snobSVG).find("#5E6061;}")
        self.eyes_index = str(self.snobSVG).find("#FFFFFF;}")
        self.snobSVG = list(self.snobSVG)


    def str2hex(self, new_color):
        if new_color.replace(" ", "").replace(",", "") == "":  # handles empty messages
            return """Please write a HEX color or a RGB color. in these formats: '#00FFFF', '00FFFF', '0 255 255' or '0,255,255\nThe command should look like this: `!snobpic [color]`"""
        if new_color[0] == "#" and self.hex_regex.match(new_color[1:]) is not None and len(
                new_color) == 7:  # handles the "#XXXXXX" hex colours
            new_color = new_color[1:]
        elif " " in new_color or "," in new_color:
            if " " in new_color and "," in new_color:  # handles the "R,        G,    B" colours
                new_color = new_color.replace(" ", "")
            elif "," in new_color:  # handles the "R,G,B" colours
                new_color = np.array(new_color.split(","), dtype=int)
            elif " " in new_color:  # handles the "R G B" colours
                new_color = np.array(new_color.split(" "), dtype=int)
            if isinstance(new_color, np.ndarray) and len(new_color) == 3 and np.any(new_color >= 0) and np.any(
                    new_color <= 255):
                new_color = "%02x%02x%02x" % tuple(new_color)
            else:
                return "RGB colours are between 0 and 255 and need 3 integers, like '127 255 212' or '127,255,212'"
        if self.hex_regex.match(new_color) is not None and len(new_color) == 6:
            return new_color
        raise ValueError

    def do_profile_picture(self, content):
        try:
            if Constants.PROFILE_PICTURE_FULL in content:
                colors = str(content.replace(Constants.PROFILE_PICTURE_FULL, "")[1:])
                colors = colors.split(" ")
                if len(colors) == 6:  # R G B and R G B
                    colors = (",".join(colors[:3]), ",".join(colors[3:]))
                if len(colors) == 2:  # Hexa/Hexa or R,G,B/R,G,B or Hexa/R,G,B or R,G,B/Hexa
                    colors = ("".join(colors[0]), "".join(colors[1]))
                elif len(colors) == 4:
                    if len(colors[0]) >= 6:  # Hexa/R G B
                        colors = ("".join(colors[0]), "".join(colors[:1]))
                    elif len(colors[3]) >= 6:  # R G B/Hexa
                        colors = (",".join(colors[:3]), "".join(colors[3]))
                else:
                    raise ValueError
                self.snobSVG[self.fur_index + 1: self.fur_index + 7] = self.str2hex(colors[0])
                self.snobSVG[self.eyes_index + 1: self.eyes_index + 7] = self.str2hex(colors[1])

            elif Constants.PROFILE_PICTURE_COMMAND in content:
                new_color = str(content.replace(Constants.PROFILE_PICTURE_COMMAND, "")[1:])
                self.snobSVG[self.fur_index + 1: self.fur_index + 7] = self.str2hex(new_color)
            elif Constants.PROFILE_PICTURE_EYES in content:
                new_color = str(content.replace(Constants.PROFILE_PICTURE_EYES, "")[1:])
                self.snobSVG[self.eyes_index + 1: self.eyes_index + 7] = self.str2hex(new_color)
            svg2png("".join(self.snobSVG), write_to="utils/snob-logo.png")
            return "Here is your personalized profile picture!", discord.File("utils/snob-logo.png")
        except ValueError:
            return "Please write a HEX color or a RGB color. in these formats: '#00FFFF', '00FFFF', '0 255 255' or '0,255,255"
        except:
            return "Unexpected error..."