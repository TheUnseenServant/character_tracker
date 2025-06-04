#!/usr/bin/env python

# name    :  parse_character_data.py
# version :  0.0.1
# date    :  20250602
# author  :  
# desc    :  


import argparse
from os.path import basename
import re

character_base = {
    "key": "",
    "name":     "",
    "career":   "",
    "level":    1,
    "hd":       1,
    "hp":       1,
    "sd":       0,
    "sp":       0,
    "xp":       0,
    "hench_to": "",
    "alignment":    "",
    "aac":          "",
    "enc":          "",
    "stats":        list(),
    "feats":        list(),
    "skills":       list(),
    "weapons":      list(),
    "armor":        list(),
    "gear":         list(),
    "silver":       0,
    "morale":       "",
    "loyalty":      "",
    "combat":       list(),
    "notes":        list(),
}

def remove_cost(string):
    """ Removes the (12sp/mo) type annotation """
    result = re.search("\(\s*\d+.*\)", string, re.IGNORECASE)
    if result is None:
        return string.strip()
    else:
        return string.replace(result.group(), "").strip()

def parse_data(file, character):
    character["key"] = basename(args.file)
    with open(file, "r") as in_f:
        has_name = False
        in_notes = False
        for line in in_f:
            line = line.strip()
            if in_notes and len(line):
                character["notes"].append(line)
            if not has_name:
                character["name"] = line
                has_name = True
            if line.lower().startswith("notes"):
                in_notes = True
            if line.lower().startswith("morale"):
                character["morale"] = line.split(':')[-1]  
            if line.lower().startswith("loyalty"):
                character["loyalty"] = line.split(':')[-1]  
            if line.lower().startswith("feats"):
                data = line.split(':')[-1].strip()
                for datum in data.split(','):
                    character["feats"].append(datum.strip())
                character["loyalty"] = line.split(':')[-1]  
    return character

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="file")

    args = parser.parse_args()

    character = character_base.copy()
    c = parse_data(args.file, character)
    print(c)


