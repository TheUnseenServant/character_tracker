#!/usr/bin/env python

# name    :  write_char.py
# version :  0.0.1
# date    :  20240217
# author  :  Leam Hall
# desc    :  Convert character information to a set format.

import argparse
import csv
import os
from string import Template
import sys


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
        self.liege = data.get("liege", "")
        self.morale = data.get("morale", "")
        self.loyalty = data.get("loyalty", "")
        self.alignment = data.get("alignment", "")
        self.species = data.get("species", "")
        self.gender = data.get("gender", "")
        self.aac = data.get("aac", "")
        self.enc = data.get("enc", "")
        self.stats = data.get("stats", "")
        self.feats = data.get("feats", "")
        self.skills = data.get("skills", "")
        self.weapons = data.get("weapons", "")
        self.armor = data.get("armor", "")
        self.gear = data.get("gear", "")
        self.silver = data.get("silver", 0)
        self.spells = data.get("spells", [])
        self.npcs = data.get("npcs", [])
        self.notes = data.get("notes", [])


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
    parser.add_argument(
        "-t", "--template_dir", default="templates", help="Template directory"
    )
    args = parser.parse_args()

    return args


def render_template(template, character):
    """Takes a template and a character and returns the formatted data."""
    return Template(template).substitute(**character.__dict__)


def write_file(output_file, data):
    """Writes the data to the output file."""
    if len(data):
        with open(output_file, "w") as out_file:
            out_file.write(data)


if __name__ == "__main__":
    data_dir = os.path.join(os.getcwd(), "data")
    args = parse_args()

    output_dir = os.path.join(os.getcwd(), args.output)
    template_dir = os.path.join(os.getcwd(), args.template_dir)
    if os.path.exists(args.output) and not os.path.isdir(args.output):
        print("{} exists but is not a directory.".format(args.output))
        sys.exit(1)
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    if not os.path.exists(args.template_dir):
        print("Directory {} does not exist.".format(template_dir))
        sys.exit(1)

    text_template_file = os.path.join(template_dir, "text.tmpl")
    if os.path.isfile(text_template_file):
        with open(text_template_file, "r") as tt:
            text_template = tt.read()
    else:
        print(
            "Cannot find the text template file: {}".format(text_template_file)
        )
        sys.exit(1)

    bbcode_template_file = os.path.join(template_dir, "bbcode.tmpl")
    if os.path.isfile(bbcode_template_file):
        with open(bbcode_template_file, "r") as bt:
            bbcode_template = bt.read()
    else:
        bbcode_template = None

    csv_template_file = os.path.join(template_dir, "csv.tmpl")
    if os.path.isfile(csv_template_file):
        with open(csv_template_file, "r") as ct:
            csv_template = ct.read()
    else:
        csv_template = None

    output_text = ""
    output_text_file = os.path.join(output_dir, "characters.txt")
    output_bbcode = ""
    output_bbcode_file = os.path.join(output_dir, "characters.bbcode")
    output_csv = ""
    output_csv_file = os.path.join(output_dir, "characters.csv")

    characters = build_party(args.file)
    for key, character in characters.items():
        character_filename = "{}.txt".format(key)
        character_filepath = os.path.join(args.chardir, character_filename)
        if os.path.exists(character_filepath):
            update_data = data_from_file(character_filepath)
            character = update_character(character, update_data)
        output_text += render_template(text_template, character)
        output_text += "\n\n"
        if bbcode_template:
            output_bbcode += render_template(bbcode_template, character)
            output_bbcode += "\n\n"
        if csv_template:
            output_csv += render_template(csv_template, character)
            output_csv += "\n"

    write_file(output_text_file, output_text)
    write_file(output_bbcode_file, output_bbcode)
