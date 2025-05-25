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
career_data["unk"] = {
    "career": "unknown",
    "hd": "1,1,1,1,1,1,1,1,1,1,1",
    "sd": "",
    "sp": "",
}

subcareers = {
    "ranger": "fighter",
    "barbarian": "fighter",
    "paladin": "fighter",
    "venturer": "rogue",
    "sorcerer": "mage",
    "bard": "cleric",
    "druid": "cleric",
    "warlock": "cleric",
}

spellcaster_careers = ["mage", "cleric", "spellthief", "swordmage"]


class Character:
    """
    Takes the character data and returns a Character object.
    """

    def __init__(self, data={}):
        self.key = data.get("key", "")
        self.name = data.get("name", "")
        self.career = data.get("career", "")
        self.level = data.get("level", 0)
        self.hd = data.get("hd", 1)
        self.hp = data.get("hp", 1)
        self.sd = data.get("sd", 0)
        self.sp = data.get("sp", 0)
        self.xp = data.get("xp", 0)
        self.hench_to = data.get("hench_to", "")
        self.alignment = data.get("alignment", "")
        self.aac = data.get("aac", "")
        self.enc = data.get("enc", "")
        self.stats = data.get("stats", "")
        self.feats = data.get("feats", "")
        self.skills = data.get("skills", "")
        self.weapons = data.get("weapons", "")
        self.armor = data.get("armor", "")
        self.gear = data.get("gear", "")
        self.silver = data.get("silver", 0)


# class CharacterBuilder:
#    """
#    Takes the data file and returns a collection of the character objects.
#    """
#
#    def build(data_file, ci):
#        if not data_file:
#            print("Must have a data file to create the characters.")
#            sys.exit(1)
#        try:
#            characters = {}
#            with open(data_file, "r", newline="") as f:
#                reader = csv.DictReader(f, delimiter=";")
#                for line in reader:
#                    c = Character(line)
#                    characters[c.key] = c
#                    career_info = ci.get_info(c.career, c.xp)
#                    c.set_info(career_info)
#
#        except FileNotFoundError:
#            print("Exception: No such file: {}".format(data_file))
#            sys.exit(1)
#
#        return characters


def build_party(character_file):
    """Takes the base character file and starts the characters."""
    if not character_file:
        print("Must have a data file to create the characters.")
        sys.exit(1)
    try:
        characters = {}
        with open(character_file, "r", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")
            for line in reader:
                c = Character(line)
                characters[c.key] = c
                # career_info = ci.get_info(c.career, c.xp)
                # c.set_info(career_info)

    except FileNotFoundError:
        print("Exception: No such file: {}".format(character_file))
        sys.exit(1)
    return characters


def key_to_string(string):
    """Makes the first item in the string the key, and the rest data."""
    line_data = string.split(":")
    key = line_data[0].strip()
    line_data[-1] = line_data[-1].strip()
    data = " ".join(line_data[1:])
    return key, data


def data_from_file(character_file):
    """
    Takes a data file and returns a character update dict.
    """
    data = dict()
    with open(character_file, "r") as in_f:
        data_lines = in_f.readlines()
        for line in data_lines:
            key, data_string = key_to_string(line)
            data[key.lower()] = data_string
    return data


def update_character(character, update_data):
    """
    Takes a data dict and returns an update character object.
    """
    for key, value in update_data.items():
        setattr(character, key, value)
    return character


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
        if self.career not in spellcaster_careers:
            return 0
        else:
            return int(self.sd[level])

    def get_sp(self, level):
        """Returns the spell dice (sd) based on the level and career."""
        if self.career not in spellcaster_careers:
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
        if career in subcareers:
            career = subcareers[career]

        if career not in self.careers:
            print("The career {} is not known.".format(career))
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
        "-c", "--chardir", default="characters", help="Character directory"
    )
    parser.add_argument(
        "-f",
        "--file",
        default=os.path.join("data", "adventure_party.csv"),
        help="Intake file",
    )
    parser.add_argument(
        "-o", "--output", default="output", help="Output directory"
    )
    args = parser.parse_args()

    return args


def format_character(character):
    template = "{}\n"
    template += "{} {} (HD {} HP {}"
    if hasattr(character, "sd"):
        template += "/sd {}/sp {})\n"
    else:
        template += ")\n"
    template += "Aligment: {}\n".format(character.alignment)
    template += "A&AC: {}\n".format(character.aac)
    template += "Encumberance: {}\n".format(character.enc)
    template += "Stats: {}\n".format(character.stats)
    template += "Feats: {}\n".format(character.feats)
    template += "Skills: {}\n".format(character.skills)
    template += "Weapons: {}\n".format(character.weapons)
    template += "Armor: {}\n".format(character.armor)
    template += "Gear: {}\n".format(character.gear)
    template += "Silver: {}\n".format(character.silver)

    return template.format(
        character.name.title(),
        character.career.title(),
        character.level,
        character.hd,
        character.hp,
        character.sd,
        character.sp,
        character.alignment.title(),
        character.aac,
        character.enc,
        character.stats,
        character.feats,
        character.skills,
        character.weapons,
        character.armor,
        character.gear,
        character.silver,
    )


if __name__ == "__main__":
    data_dir = os.path.join(os.getcwd(), "data")
    args = parse_args()

    output_dir = os.path.join(os.getcwd(), args.output)
    if os.path.exists(args.output) and not os.path.isdir(args.output):
        print("{} exists but is not a directory.".format(args.output))
        sys.exit(1)
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    output_text = os.path.join(output_dir, "characters.txt")

    empty_data = {"level": 1, "hd": 1, "hp": 1, "sd": 0, "sp": 0}

    characters = build_party(args.file)
    with open(output_text, "w") as text_out:
        for key, character in characters.items():
            print(key)
            character_filename = "{}.txt".format(key)
            character_filepath = os.path.join(args.chardir, character_filename)
            if os.path.exists(character_filepath):
                update_data = data_from_file(character_filepath)
                character = update_character(character, update_data)
                print("{}  Level {}".format(character.name, character.level))
            else:
                character = update_character(character, empty_data)
            text_out.write(format_character(character))
