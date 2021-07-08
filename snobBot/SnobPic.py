import re
import discord
import numpy as np
from cairosvg import svg2png
from snobBot import Constants
from random import randint as ri


class SnobPic:
    def __init__(self):
        self.hex_regex = re.compile("^[0-9a-fA-F]{6}")
        with open("utils/sas.svg", "rb") as f:
            self.snobSVG = f.read().decode("utf-8")
        self.fur_index = str(self.snobSVG).find("#7D584B;}")
        self.eyes_index = str(self.snobSVG).find("#26C4B8;}")
        self.glasses1_index = str(self.snobSVG).find("0;fill:#FCFCFC;}")
        self.glasses2_index = str(self.snobSVG).find("0;fill:#040404;")
        self.snobSVG = list(self.snobSVG)


    def str2hex(self, new_color):
        if new_color.replace(" ", "").replace(",", "") == "":  # handles empty messages
            raise ValueError
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
                raise ValueError
        if self.hex_regex.match(new_color) is not None and len(new_color) == 6:
            return new_color
        raise ValueError
    
    def do_profile_picture(self, msg):
        try:
            if Constants.COMMAND_GLASSES in msg:
                msg = msg.replace(Constants.COMMAND_GLASSES, "")
                self.snobSVG[self.glasses1_index] = "1"
                self.snobSVG[self.glasses2_index] = "1"
            else:
                self.snobSVG[self.glasses1_index] = "0"
                self.snobSVG[self.glasses2_index] = "0"

            colors = msg.split()
            if len(colors) == 6:  # R G B and R G B
                colors = (",".join(colors[:3]), ",".join(colors[3:]))
            if len(colors) == 2:  # Hexa/Hexa or R,G,B/R,G,B or Hexa/R,G,B or R,G,B/Hexa
                colors = ["".join(colors[0]), "".join(colors[1])]
            elif len(colors) == 4:
                if len(colors[0]) >= 6:  # Hexa/R G B
                    colors = ("".join(colors[0]), ",".join(colors[1:]))
                elif len(colors[3]) >= 6:  # R G B/Hexa
                    colors = (",".join(colors[:3]), "".join(colors[3]))
            elif len(colors) == 3: #R G B
                colors = (",".join(colors[:3]),)
            elif len(colors) == 1: #Hexa
                colors = colors
            else:
                raise ValueError
            for i, c in enumerate(colors):
                if "random" in c:
                    colors[i] = '%02X%02X%02X' % (ri(0, 256), ri(0, 256), ri(0, 256))
            self.snobSVG[self.fur_index + 1: self.fur_index + 7] = self.str2hex(colors[0])
            if len(colors) == 2:
                self.snobSVG[self.eyes_index + 1: self.eyes_index + 7] = self.str2hex(colors[1])
            else:
                self.snobSVG[self.eyes_index + 1: self.eyes_index + 7] = "26C4B8"
            svg2png("".join(self.snobSVG), write_to="utils/snob-logo.png")
            return "Here is your personalized profile picture!", discord.File("utils/snob-logo.png")
        except ValueError:
            raise ValueError