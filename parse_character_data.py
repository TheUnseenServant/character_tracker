#!/usr/bin/env python

# name    :  parse_character_data.py
# version :  0.0.1
# date    :  20250602
# author  :  
# desc    :  


import argparse
from os.path import basename

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

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="file")

args = parser.parse_args()

character_base["key"] = basename(args.file)

with open(args.file, "r") as in_f:
    has_name = False
    in_notes = False
    for line in in_f:
        line = line.strip()
        if in_notes and len(line):
            character_base["notes"].append(line)
        if not has_name :
            character_base["name"] = line
            has_name = True
        if line.lower().startswith("notes"):
            in_notes = True
        if line.lower().startswith("morale"):
            character_base["morale"] = line.split(':')[-1]  
        if line.lower().startswith("loyalty"):
            character_base["loyalty"] = line.split(':')[-1]  
        if line.lower().startswith("feats"):
            data = line.split(':')[-1].strip()
            for datum in data.split(','):
                character_base["feats"].append(datum.strip())
            character_base["loyalty"] = line.split(':')[-1]  


print(character_base)


