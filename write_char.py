#!/usr/bin/env python

# name    :  write_char.py
# version :  0.0.1
# date    :  20240217
# author  :  Leam Hall
# desc    :  Convert character information to a set format.

import argparse
import csv
import os
import sys


class Character:
    """
    Takes the character data and returns a Character object.
    """

    def __init__(self, data={}):
        self.name = data.get("name", None)
        self.career = data.get("career", None)
        self.xp = int(data.get("xp", 0))


class CharacterBuilder:
    """
    Takes the data file and returns a collection of the character objects.
    """

    def build(data_file):
        if not data_file:
            print("Must have a data file to create the characters.")
            sys.exit(1)
        try:
            characters = {}
            with open(data_file, "r", newline="") as f:
                reader = csv.DictReader(f, delimiter=";")
                for line in reader:
                    c = Character(line)
                    characters[c.name] = c
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
        for v in input_list.split(","):
            result.append(v.strip())
        return result

    def get_hd(self, level):
        """Returns the hit dice (hd) based on level and class."""
        return int(self.hd[level])

    def get_sd(self, level):
        """Returns the spell dice (sd) based on the level and class."""
        if self.career == "fighter":
            return 0
        else:
            return int(self.sd[level])

    def get_level(self, xp):
        """Returns the character level based on xp given."""
        level = 0
        for level_index, xp_min in enumerate(self.xp_required):
            if xp >= xp_min:
                level = level_index
        return level

    def get_level_hd_sd(self, xp):
        """Returns a collection of level, hd, and sd based on xp given."""
        data = dict()
        data["level"] = self.get_level(xp)
        data["hd"] = self.get_hd(data["level"])
        data["sd"] = self.get_sd(data["level"])
        return data


class CareerInfo:
    def __init__(self, careers):
        self.careers = careers

    def get_info(self, career, level):
        """
        Returns the Hit Dice (hd) and Spell Dice (sd) for a specific class
        and level.
        """
        career = career.lower()
        if career not in self.careers:
            print("Sorry, you must use one of the established meta-careers:")
            output_line = "  "
            for c in self.careers.keys():
                output_line += "{}  ".format(c.title())
            print(output_line)
            sys.exit(0)
        level = self.min_max_level(career, level)
        hd = self.careers[career].get_hd(level)
        sd = self.careers[career].get_sd(level)
        return (int(hd), int(sd))

    def min_max_level(self, career, level):
        max_level = len(self.careers[career].hd)
        try:
            level = int(level)
        except ValueError:
            print("Sorry, levels are measured in integers from 0-14/15.")
            sys.exit(0)

        if level < 0:
            print("Setting the level to 0, since you messed up.")
            level = 0
        if level > max_level:
            print("Sorry, lowering your level so that it fits the game.")
            level = max_level
        return level


class CareerInfoBuilder:
    def __init__(self, data_file):
        self.careers = dict()
        self.data_file = data_file
        self.data_from_file()

    def data_from_file(self):
        """Sample file:
        career;hd;sd
        fighter;1,2,3,4,5,6,7,8,9,10,11,12,13,14,15;
        mage;1,1,2,2,3,3,4,4,5,5,6,6,7,7,8;0,1,1,2,2,3,3,4,4,5,5,6,6,7,7
        cleric;1,1,2,3,3,4,5,5,6,7,7,8,9,9,10;0,1,1,1,2,2,2,3,3,3,4,4,4,5,5
        """
        try:
            with open(self.data_file, "r", newline="") as f:
                reader = csv.DictReader(f, delimiter=";")
                for line in reader:
                    c = Career(line)
                    self.careers[c.career] = c
        except FileNotFoundError:
            print("Exception: No such file")
            sys.exit(1)

    def build(self):
        return CareerInfo(self.careers)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--datadir",
        default="data",
        help="Directory for data files",
    )
    parser.add_argument(
        "-f", "--file", default="data/adventure_party.csv", help="Intake file"
    )
    parser.add_argument("-c", "--career", default="fighter", help="Career")
    parser.add_argument(
        "-l", "--level", default="data/levels.csv", help="Level file", type=int
    )
    args = parser.parse_args()
    args.level_file = os.path.join(args.datadir, "levels.csv")

    return args


def write_character(character, args, ci_info):
    template = "Name  {} Class {} Level {} HD {}/SD {}"
    print(
        template.format(
            args.career.title(), args.level, ci_info[0], ci_info[1]
        )
    )


if __name__ == "__main__":
    args = parse_args()
    ci = CareerInfoBuilder(args.level_file).build()

    ci_info = ci.get_info(args.career, args.level)
