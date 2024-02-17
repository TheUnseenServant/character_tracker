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


class Career:
    """
    Tracks the current classes, how many Hit Dice (hd) and Spell Dice (sd)
    that class gets.
    """

    def __init__(self, data):
        self.career = data.get("career", None)
        self.hd = self.set_values(data.get("hd", None))
        self.sd = self.set_values(data.get("sd", None))

    def set_values(self, input_list):
        result = []
        for v in input_list.split(","):
            result.append(v.strip())
        return result

    def get_hd(self, level):
        return self.hd[level]

    def get_sd(self, level):
        if self.career == "fighter":
            return 0
        else:
            return self.sd[level]


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
    parser.add_argument("-l", "--level", default=0, help="Level", type=int)
    args = parser.parse_args()
    args.level_file = os.path.join(args.datadir, "levels.csv")

    return args


if __name__ == "__main__":
    args = parse_args()
    ci = CareerInfoBuilder(args.level_file).build()

    ci_info = ci.get_info(args.career, args.level)
    template = "Name  {} Level {} HD {}/SD {}"
    print(
        template.format(
            args.career.title(), args.level, ci_info[0], ci_info[1]
        )
    )
