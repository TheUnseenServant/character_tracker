#!/usr/bin/env python

# name    :  write_char.py
# version :  0.0.1
# date    :  20240217
# author  :  Leam Hall
# desc    :  Convert character information to a set format.

import argparse
import csv
import sys


career_data = dict()
career_data["fighter"] = {
    "career": "fighter",
    "hd": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15",
    "sd": "",
    "sp": "",
}
career_data["mage"] = {
    "career": "mage",
    "hd": "1,1,2,2,3,3,4,4,5,5,6,6,7,7,8",
    "sd": "0,1,1,2,2,3,3,4,4,5,5,6,6,7,7",
    "sp": "0,2,3,5,6,8,9,11,12,14,15,17,18,20,21",
}
career_data["cleric"] = {
    "career": "cleric",
    "hd": "1,1,2,3,3,4,5,5,6,7,7,8,9,9,10",
    "sd": "0,1,1,1,2,2,2,3,3,3,4,4,4,5,5",
    "sp": "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14",
}
career_data["rogue"] = {
    "career": "rogue",
    "hd": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15",
    "sd": "",
    "sp": "",
}
career_data["swordmage"] = {
    "career": "swordmage",
    "hd": "1,2,3,4,5,6,7,8,9,10,11",
    "sd": "0,1,1,2,2,3,3,4,4,5,5",
    "sp": "0,2,3,5,6,8,9,11,12,14,15",
}
career_data["spellthief"] = {
    "career": "spellthief",
    "hd": "1,1,2,3,4,5,6,7,8,9,10",
    "sd": "0,1,1,2,2,3,3,4,4,5,5",
    "sp": "0,2,3,5,6,8,9,11,12,14,15",
}


class Character:
    """
    Takes the character data and returns a Character object.
    """

    def __init__(self, data={}):
        self.key = data.get("key", "")
        self.name = data.get("name", "")
        self.career = data.get("career", "")
        self.xp = int(data.get("xp", 0))

    def set_info(self, ci_info):
        self.level = ci_info["level"]
        self.hd = ci_info["hd"]
        self.sd = ci_info["sd"]
        self.sp = ci_info["sp"]


class CharacterBuilder:
    """
    Takes the data file and returns a collection of the character objects.
    """

    def build(data_file, ci):
        if not data_file:
            print("Must have a data file to create the characters.")
            sys.exit(1)
        try:
            characters = {}
            with open(data_file, "r", newline="") as f:
                reader = csv.DictReader(f, delimiter=";")
                for line in reader:
                    c = Character(line)
                    characters[c.key] = c
                    career_info = ci.get_info(c.career, c.xp)
                    c.set_info(career_info)

        except FileNotFoundError:
            print("Exception: No such file: {}".format(data_file))
            sys.exit(1)

        return characters


class Career:
    """
    Tracks the current careers, how many Hit Dice (hd) and Spell Dice (sd)
    that career gets.
    """

    def __init__(self, data):
        self.career = data.get("career", None)
        self.hd = self.set_values(data.get("hd", None))
        self.sd = self.set_values(data.get("sd", None))
        self.sp = self.set_values(data.get("sp", None))
        self.xp_required = [
            -1000,
            0,
            2000,
            4000,
            8000,
            16_000,
            32_000,
            64_000,
            128_000,
        ]

    def set_values(self, input_list):
        """Builds the data lists based on class data provided."""
        result = []
        if not input_list:
            return None
        for v in input_list.split(","):
            result.append(v.strip())
        return result

    def get_hd(self, level):
        """Returns the hit dice (hd) based on level and career."""
        return int(self.hd[level])

    def get_sd(self, level):
        """Returns the spell dice (sd) based on the level and career."""
        if self.career == "fighter" or self.career == "rogue":
            return 0
        else:
            return int(self.sd[level])

    def get_sp(self, level):
        """Returns the spell dice (sd) based on the level and career."""
        if self.career == "fighter" or self.career == "rogue":
            return 0
        else:
            return int(self.sp[level])

    def get_level(self, xp):
        """Returns the character level based on xp given."""
        level = 0
        for level_index, xp_min in enumerate(self.xp_required):
            if xp >= xp_min:
                level = level_index
        if self.career in ["swordmage", "spellthief"]:
            level -= 1
        return level

    def get_info(self, xp):
        """Returns a collection of level, hd, sd and sp based on xp given."""
        data = dict()
        data["level"] = self.get_level(xp)
        data["hd"] = self.get_hd(data["level"])
        data["sd"] = self.get_sd(data["level"])
        data["sp"] = self.get_sp(data["level"])
        return data


class CareerInfo:
    def __init__(self, career_data):
        self.careers = self.make_careers(career_data)

    def make_careers(self, career_data):
        careers = dict()
        for career, data in career_data.items():
            careers[career] = Career(data)

        return careers

    def get_info(self, career, xp):
        """
        Returns the Level, Hit Dice (hd), Spell Dice (sd) and
        Spell Points (sp) for a specific career and xp amount.
        """
        career = career.lower()
        if career not in self.careers:
            print("Sorry, you must use one of the established meta-careers:")
            output_line = "  "
            for c in self.careers.keys():
                output_line += "{}  ".format(c.title())
            print(output_line)
            sys.exit(0)
        return self.careers[career].get_info(xp)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", default="adventure_party.csv", help="Intake file"
    )
    args = parser.parse_args()

    return args


def write_character(character):
    template = "{}\n"
    template += "{} Level {} (hd {}/sd {}/sp {})\n"
    print(
        template.format(
            character.name.title(),
            character.career.title(),
            character.level,
            character.hd,
            character.sd,
            character.sp,
        ),
        "\n",
    )


if __name__ == "__main__":
    args = parse_args()
    career_info = CareerInfo(career_data)
    characters = CharacterBuilder.build(args.file, career_info)
    for character in characters.values():
        write_character(character)
