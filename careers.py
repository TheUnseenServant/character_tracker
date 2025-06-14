#!/usr/bin/env python

# name    :  careers.py
# version :  0.0.1
# date    :  20250614
# author  :  Leam Hall
# desc    :  Convert character xp to career info.

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
