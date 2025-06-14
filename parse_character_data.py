#!/usr/bin/env python

# name    :  parse_character_data.py
# version :  0.0.1
# date    :  20250602
# author  :
# desc    :


import argparse
import copy
from os import listdir
from os.path import basename, isfile, join
from string import Template
import re

character_base = {
    "key": "",
    "name": "",
    "career": "",
    "level": 1,
    "hd": 1,
    "hp": 1,
    "sd": 0,
    "sp": 0,
    "xp": 0,
    "hench_to": "",
    "alignment": "",
    "aac": "",
    "enc": "",
    "stats": list(),
    "feats": list(),
    "skills": list(),
    "weapons": list(),
    "armor": list(),
    "gear": list(),
    "silver": 0,
    "morale": "",
    "loyalty": "",
    "combat": list(),
    "notes": list(),
}


def remove_cost(string):
    """Removes the (12p/mo) type annotation"""
    result = re.search("\(\s*\d+.*\)", string, re.IGNORECASE)
    if result is None:
        return string.strip()
    else:
        return string.replace(result.group(), "").strip()


def parse_data(file, character):
    #character["key"] = basename(args.file)
    character["key"] = basename(file)
    with open(file, "r") as in_f:
        has_name = False
        in_notes = False
        for line in in_f:
            line = line.strip()
            line = remove_cost(line)
            if in_notes and len(line):
                character["notes"].append(line)
            if not has_name:
                character["name"] = line
                has_name = True
            if line.lower().startswith("notes"):
                in_notes = True
            if line.lower().startswith("morale"):
                character["morale"] = line.split(":")[-1]
            if line.lower().startswith("loyalty"):
                character["loyalty"] = line.split(":")[-1]
            if line.lower().startswith("feats"):
                data = line.split(":")[-1].strip()
                for datum in data.split(","):
                    character["feats"].append(datum.strip())
                character["loyalty"] = line.split(":")[-1]
    return character

def render_template(template, character):
    """ Takes a template and a character DICT, returns text. """ 
    return Template(template).substitute(**character)

if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-f", "--file", help="file")
    #args = parser.parse_args()

    source_dir = "characters/base"
    output_dir = "characters"
    source_files = [f for f in listdir(source_dir) if isfile(join(source_dir, f))]

    template_dir = "templates"
    output_template_file = join(template_dir, "text.tmpl")
    if isfile(output_template_file):
        with open(output_template_file, "r") as tt:
            output_template = tt.read()

    for file in source_files:
        character = copy.deepcopy(character_base)
        filename = join(source_dir, file)
        output_filename = "{}.txt".format(file)
        output = join(output_dir, output_filename)
        c = parse_data(filename, character)
        with open(output, "w") as out:
            out.write(render_template(output_template, c))

