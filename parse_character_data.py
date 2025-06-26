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
    "species": "",
    "gender": "",
    "aac": "",
    "enc": "",
    "stats": list(),
    "feats": list(),
    "skills": list(),
    "weapons": list(),
    "armor": list(),
    "gear": list(),
    "silver": 0,
    "liege": "",
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

def parse_career_line(line):
    """ Takes the career/class line and returns a dict to be merged. """
    updates = dict()
    line    = line.strip()
    line    = line.replace("(", "")
    line    = line.replace(")", "")
    line    = line.replace(",", "")
    line_data = line.split()
    updates["career"] = line_data[0].title()
    updates["level"] = line_data[1]
    updates["hd"] = line_data[3]
    updates["hp"] = line_data[5]
    if len(line_data) < 7:
        updates["sd"] = 0
        updates["sp"] = 0
    else:
        updates["sd"] = line_data[7]
        updates["sp"] = line_data[9]
    
    return updates

def parse_basic_line(line):
    """ Takes the alignment/species/gender line and returns a dict to be merged. """
    updates = dict()
    line    = line.strip()
    line_data = line.split()
    updates["alignment"] = line_data[0].title()
    updates["species"] = line_data[1].title()
    updates["gender"] = line_data[2].title()
    return updates
    
def parse_data(file, character):
    """ Parse the file and build the character. """
    character["key"] = basename(file)
    # Used for testing
    #print(character["key"])
    with open(file, "r") as in_f:
        has_name = False
        in_notes = False
        align    = False
        counter  = 0
        for line in in_f:
            line = line.strip()
            line = remove_cost(line)
            counter += 1
            if in_notes and len(line):
                character["notes"].append(line)
            if not has_name:
                character["name"] = line
                has_name = True
            elif counter == 2:
                character.update(parse_basic_line(line))
            elif counter == 3:
                character.update(parse_career_line(line))
            elif line.lower().startswith("notes"):
                in_notes = True
            elif line.lower().startswith("morale"):
                character["morale"] = line.split(":")[-1]
            elif line.lower().startswith("loyalty"):
                character["loyalty"] = line.split(":")[-1]
            elif line.lower().startswith("feats"):
                data = line.split(":")[-1].strip()
                for datum in data.split(","):
                    character["feats"].append(datum.strip())
            elif line.lower().startswith("skills"):
                data = line.split(":")[-1].strip()
                for datum in data.split(","):
                    character["skills"].append(datum.strip())
            elif line.lower().startswith("a&ac"):
                character["aac"] = line.split(":")[-1].strip()
            elif line.lower().startswith("combat"):
                character["combat"] = line.split(":")[-1].strip()
            elif line.lower().startswith("enc"):
                character["enc"] = line.split(":")[-1].strip()
            elif line.lower().startswith("ability scores"):
                data = line.split(":")[-1].strip()
                for datum in data.split(","):
                    character["stats"].append(datum.strip())
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

